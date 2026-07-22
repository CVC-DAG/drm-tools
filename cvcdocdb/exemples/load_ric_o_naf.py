"""Load RiC-O data from the National Archives of France into Neo4j.

Downloads RDF/XML files from the National Archives of France RiC-O examples
and imports them into Neo4j using Cypher MERGE commands.

The loader:

1. Downloads RDF files from GitHub (agents, recordResources, relations, vocabularies)
2. Parses them with ``rdflib``
3. Extracts nodes and relationships
4. Uses Cypher MERGE to insert nodes and relationships into Neo4j
5. Returns load statistics

Usage::

    from cvcdocdb.exemples.load_ric_o_naf import load_ric_o_naf

    stats = load_ric_o_naf(graph, limit=50, max_agents=10, max_records=3)
    print(f"Total entities: {stats['total']}")
"""

from __future__ import annotations

import os
import urllib.request
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import rdflib
    from rdflib import RDF, RDFS, OWL, Graph, URIRef, Literal, Namespace
except ImportError:  # pragma: no cover
    raise ImportError(
        "rdflib is required for RiC-O loading. "
        "Install it with: pip install rdflib"
    )

# ---------------------------------------------------------------------------
# URLs for the National Archives of France RiC-O examples
# ---------------------------------------------------------------------------

BASE_URL = "https://raw.githubusercontent.com/ICA-EGAD/RiC-O/master/examples/examples_v1-1/NationalArchivesOfFrance/rdf-xml"

AGENT_URL = f"{BASE_URL}/agents"
RECORD_URL = f"{BASE_URL}/recordResources"
RELATION_URL = f"{BASE_URL}/relations"
VOCAB_URL = f"{BASE_URL}/vocabularies"

# Namespace for the RiC-O ontology
ONTO_NS = "https://www.ica.org/standards/RiC/ontology#"
ONTO = Namespace(ONTO_NS)

# ---------------------------------------------------------------------------
# RDF → DRM label mapping
# ---------------------------------------------------------------------------

RDF_TO_LABEL: Dict[str, str] = {
    str(ONTO.Record): "Thing",
    str(ONTO.Agent): "Agent",
    str(ONTO.CorporateBody): "CorporateBody",
    str(ONTO.Individual): "Person",
    str(ONTO.AgentName): "AgentName",
    str(ONTO.RecordResource): "RecordResource",
    str(ONTO.RecordSet): "RecordResource",
    str(ONTO.Instantiation): "Instantiation",
    str(ONTO.Activity): "Activity",
    str(ONTO.ActivityType): "ActivityType",
    str(ONTO.DocumentaryFormType): "DocumentaryFormType",
    str(ONTO.Language): "Language",
    str(ONTO.CorporateBodyType): "CorporateBodyType",
    str(ONTO.Place): "Place",
    str(ONTO.PlaceName): "PlaceName",
    str(ONTO.PhysicalLocation): "PhysicalLocation",
    str(ONTO.Identifier): "Identifier",
    str(ONTO.Date): "Date",
    str(ONTO.Title): "Title",
    str(ONTO.Appellation): "Appellation",
    str(ONTO.Mechanism): "Mechanism",
    str(ONTO.RoleType): "RoleType",
    str(ONTO.Rule): "Rule",
    str(ONTO.Position): "Position",
    str(ONTO.Group): "Group",
    str(ONTO.Family): "Family",
    str(ONTO.FamilyType): "FamilyType",
    str(ONTO.Event): "Event",
    str(ONTO.EventType): "EventType",
    str(ONTO.RecordState): "RecordState",
    str(ONTO.Extent): "Extent",
    str(ONTO.ExtentType): "ExtentType",
    str(ONTO.UnitOfMeasurement): "UnitOfMeasurement",
    str(ONTO.DemographicGroup): "DemographicGroup",
    str(ONTO.LegalStatus): "LegalStatus",
    str(ONTO.Mandate): "Mandate",
    str(ONTO.MandateType): "MandateType",
}

# ---------------------------------------------------------------------------
# Helper: download a directory listing from GitHub
# ---------------------------------------------------------------------------


def _list_github_dir(url: str) -> List[str]:
    """List files in a GitHub raw directory URL.

    Args:
        url: The GitHub raw URL of the directory.

    Returns:
        List of filenames.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "cvcdocdb-rico/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")

    return [line.strip() for line in data.splitlines() if line.strip().endswith(".rdf")]


def _download_file(url: str) -> bytes:
    """Download a file from a URL.

    Args:
        url: The URL to download.

    Returns:
        The file content as bytes.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "cvcdocdb-rico/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


# ---------------------------------------------------------------------------
# RDF parsing
# ---------------------------------------------------------------------------


def _parse_rdf(data: bytes) -> Graph:
    """Parse RDF/XML bytes into an rdflib Graph.

    Args:
        data: RDF/XML content as bytes.

    Returns:
        Parsed rdflib Graph.
    """
    g = Graph()
    g.parse(data=data, format="xml")
    return g


def _extract_node_id(uri: URIRef, base_uri: str) -> str:
    """Extract a stable node ID from a URI.

    Converts ``https://rdf.archives-nationales.culture.gouv.fr/agent/000005``
    to ``agent/000005``.

    Args:
        uri: The RDF URI.
        base_uri: The xml:base of the document.

    Returns:
        A stable node ID string.
    """
    uri_str = str(uri)
    if base_uri and uri_str.startswith(base_uri):
        return uri_str[len(base_uri):]
    # Fallback: extract last path segment
    for sep in ("#", "/"):
        if sep in uri_str:
            return uri_str.rsplit(sep, 1)[-1]
    return str(uri)


def _local_name(uri: str) -> str:
    """Extract a local name from a URI."""
    if "#" in uri:
        return uri.rsplit("#", 1)[-1]
    if "/" in uri:
        return uri.rsplit("/", 1)[-1]
    if ":" in uri:
        return uri.rsplit(":", 1)[-1]
    return uri


def _parse_rdf_file(
    url: str,
    category: str = "",
) -> Tuple[Graph, str]:
    """Parse a single RDF file and return the graph and its base URI.

    Args:
        url: The URL of the RDF file.
        category: Category name for logging.

    Returns:
        Tuple of (parsed graph, base URI).
    """
    data = _download_file(url)
    g = _parse_rdf(data)

    # Try to find xml:base from the graph
    base_uri = ""
    for s, p, o in g:
        if str(p) == "http://www.w3.org/XML/1998/namespace#base":
            base_uri = str(o)
            break

    return g, base_uri


# ---------------------------------------------------------------------------
# Node extraction
# ---------------------------------------------------------------------------


def _extract_nodes(
    g: Graph,
    base_uri: str,
    category: str,
) -> List[Dict[str, Any]]:
    """Extract nodes from an RDF graph.

    Args:
        g: The parsed RDF graph.
        base_uri: The base URI of the document.
        category: Category name (agents, recordResources, etc.).

    Returns:
        List of node dicts with keys: id, labels, properties.
    """
    nodes: Dict[str, Dict[str, Any]] = {}

    # First pass: find all subjects with known RDF types
    for s, p, o in g:
        if not isinstance(s, URIRef):
            continue
        if not isinstance(p, URIRef) or str(p) != str(RDF.type):
            continue
        if not isinstance(o, URIRef):
            continue

        obj_str = str(o)
        label = RDF_TO_LABEL.get(obj_str)
        if label is None:
            continue

        node_id = _extract_node_id(s, base_uri)
        if node_id in nodes:
            if label not in nodes[node_id]["labels"]:
                nodes[node_id]["labels"].append(label)
            continue

        nodes[node_id] = {
            "id": node_id,
            "labels": [label],
            "properties": {},
        }

    # Second pass: extract properties for each node
    for node_id in list(nodes.keys()):
        uri = URIRef(base_uri + node_id) if base_uri else URIRef(node_id)

        for prop_uri, prop in g.predicate_objects(uri):
            prop_str = str(prop_uri)
            prop_name = _local_name(prop_str)

            # Skip RDF type and subClassOf
            if prop_str == str(RDF.type):
                continue
            if prop_str == str(RDFS.subClassOf):
                continue

            if isinstance(prop, Literal):
                val = str(prop)
                if prop.language:
                    val = f"{val}@{prop.language}"
                # Avoid overwriting with empty values
                if prop_name not in nodes[node_id]["properties"] or not nodes[node_id]["properties"][prop_name]:
                    nodes[node_id]["properties"][prop_name] = val
            elif isinstance(prop, URIRef):
                ref_id = _extract_node_id(prop, base_uri)
                prop_key = f"_ref_{_local_name(prop_str)}"
                if prop_key not in nodes[node_id]["properties"]:
                    nodes[node_id]["properties"][prop_key] = []
                if ref_id not in nodes[node_id]["properties"][prop_key]:
                    nodes[node_id]["properties"][prop_key].append(ref_id)

    return list(nodes.values())


# ---------------------------------------------------------------------------
# Relationship extraction
# ---------------------------------------------------------------------------

# Map of RiC-O properties → (rel_type, src_label, dst_label)
# Used to generate Cypher MERGE for relationships
RELATION_MAP: Dict[str, Tuple[str, str, str]] = {
    str(ONTO.hasOrganicProvenance): ("HAS_ORGANIC_PROVENANCE", "RecordResource", "Agent"),
    str(ONTO.isOrWasOrganicProvenanceOf): ("IS_ORGANIC_PROVENANCE_OF", "Agent", "RecordResource"),
    str(ONTO.directlyIncludes): ("DIRECTLY_INCLUDES", "RecordResource", "RecordResource"),
    str(ONTO.isDirectlyIncludedIn): ("IS_DIRECTLY_INCLUDED_IN", "RecordResource", "RecordResource"),
    str(ONTO.hasOrHadInstantiation): ("HAS_INSTANTIATION", "RecordResource", "Instantiation"),
    str(ONTO.isOrWasInstantiationOf): ("IS_INSTANTIATION_OF", "Instantiation", "RecordResource"),
    str(ONTO.hasOrHadHolder): ("HAS_HOLDER", "Instantiation", "Agent"),
    str(ONTO.hasOrHadLocation): ("HAS_LOCATION", "Instantiation", "PhysicalLocation"),
    str(ONTO.hasOrHadAgentName): ("HAS_AGENT_NAME", "Agent", "AgentName"),
    str(ONTO.isOrWasAgentNameOf): ("IS_AGENT_NAME_OF", "AgentName", "Agent"),
    str(ONTO.hasOrHadCreator): ("HAS_CREATOR", "Thing", "Agent"),
    str(ONTO.hasCreator): ("HAS_CREATOR", "Thing", "Agent"),
    str(ONTO.hasPublisher): ("HAS_PUBLISHER", "Thing", "Agent"),
    str(ONTO.isOrWasDescribedBy): ("IS_DESCRIBED_BY", "Agent", "Thing"),
    str(ONTO.describesOrDescribed): ("DESCRIBES_OR_DESCRIBED", "Thing", "Agent"),
    str(ONTO.hasOrHadController): ("HAS_CONTROLLER", "Agent", "Agent"),
    str(ONTO.hasOrHadEmployer): ("HAS_EMPLOYER", "Agent", "Agent"),
    str(ONTO.hasOrHadMember): ("HAS_MEMBER", "Group", "Agent"),
    str(ONTO.hasOrHadSpouse): ("HAS_SPOUSE", "Agent", "Agent"),
    str(ONTO.hasOrHadStudent): ("HAS_STUDENT", "Agent", "Agent"),
    str(ONTO.hasOrHadTeacher): ("HAS_TEACHER", "Agent", "Agent"),
    str(ONTO.hasOrHadChild): ("HAS_CHILD", "Agent", "Agent"),
    str(ONTO.hasOrHadParent): ("HAS_PARENT", "Agent", "Agent"),
    str(ONTO.hasOrHadHierarchicalRelation): ("HAS_HIERARCHICAL_RELATION", "Agent", "Agent"),
    str(ONTO.hasOrHadTemporalRelation): ("HAS_TEMPORAL_RELATION", "Agent", "Agent"),
    str(ONTO.hasOrHadAgentToAgentRelation): ("HAS_AGENT_TO_AGENT_RELATION", "Agent", "Agent"),
    str(ONTO.hasOrHadSubject): ("HAS_SUBJECT", "RecordResource", "Thing"),
    str(ONTO.hasOrHadMainsubject): ("HAS_MAIN_SUBJECT", "RecordResource", "Thing"),
    str(ONTO.hasOrHadLanguage): ("HAS_LANGUAGE", "Thing", "Language"),
    str(ONTO.hasOrHadDocumentaryFormType): ("HAS_DOCUMENTARY_FORM_TYPE", "Thing", "DocumentaryFormType"),
    str(ONTO.hasOrHadCorporateBodyType): ("HAS_CORPORATE_BODY_TYPE", "CorporateBody", "CorporateBodyType"),
    str(ONTO.hasOrHadIdentifier): ("HAS_IDENTIFIER", "Agent", "Identifier"),
    str(ONTO.hasOrHadBirthDate): ("HAS_BIRTH_DATE", "Agent", "Date"),
    str(ONTO.hasOrHadDeathDate): ("HAS_DEATH_DATE", "Agent", "Date"),
    str(ONTO.hasOrHadBirthPlace): ("HAS_BIRTH_PLACE", "Agent", "PhysicalLocation"),
    str(ONTO.hasOrHadDeathPlace): ("HAS_DEATH_PLACE", "Agent", "PhysicalLocation"),
    str(ONTO.hasOrHadOccupation): ("HAS_OCCUPATION", "Agent", "OccupationType"),
    str(ONTO.hasOrHadPosition): ("HAS_POSITION", "Agent", "Position"),
    str(ONTO.hasOrHadRole): ("HAS_ROLE", "Agent", "RoleType"),
    str(ONTO.hasOrHadDate): ("HAS_DATE", "RecordResource", "Date"),
    str(ONTO.hasOrHadTitle): ("HAS_TITLE", "RecordResource", "Title"),
    str(ONTO.hasOrHadExtent): ("HAS_EXTENT", "RecordResource", "Extent"),
    str(ONTO.hasOrHadContentType): ("HAS_CONTENT_TYPE", "RecordResource", "ContentType"),
    str(ONTO.hasOrHadRecordState): ("HAS_RECORD_STATE", "RecordResource", "RecordState"),
    str(ONTO.hasOrHadLegalStatus): ("HAS_LEGAL_STATUS", "RecordResource", "LegalStatus"),
    str(ONTO.hasOrHadCreationDate): ("HAS_CREATION_DATE", "RecordResource", "Date"),
    str(ONTO.hasOrHadPublicationDate): ("HAS_PUBLICATION_DATE", "RecordResource", "Date"),
    str(ONTO.hasOrHadModificationDate): ("HAS_MODIFICATION_DATE", "RecordResource", "Date"),
    str(ONTO.hasOrHadMigrationDate): ("HAS_MIGRATION_DATE", "RecordResource", "Date"),
    str(ONTO.hasOrHadDerivationRelation): ("HAS_DERIVATION_RELATION", "Instantiation", "Instantiation"),
    str(ONTO.hasOrHadAnalogueInstantiation): ("HAS_ANALOGUE_INSTANTIATION", "Instantiation", "Instantiation"),
    str(ONTO.hasOrHadDigitalInstantiation): ("HAS_DIGITAL_INSTANTIATION", "Thing", "Instantiation"),
    str(ONTO.hasOrHadDirectPart): ("HAS_DIRECT_PART", "RecordResource", "RecordResource"),
    str(ONTO.isOrWasPartOf): ("IS_PART_OF", "RecordResource", "RecordResource"),
    str(ONTO.directlyPrecedesInSequence): ("DIRECTLY_PRECEDES", "RecordResource", "RecordResource"),
    str(ONTO.isOrWasAffectedBy): ("IS_AFFECTED_BY", "Thing", "Activity"),
}


def _extract_relationships(
    g: Graph,
    base_uri: str,
    category: str,
) -> List[Dict[str, Any]]:
    """Extract relationships from an RDF graph.

    Args:
        g: The parsed RDF graph.
        base_uri: The base URI of the document.
        category: Category name.

    Returns:
        List of relationship dicts with keys: src_id, dst_id, type, src_label, dst_label.
    """
    rels: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str, str]] = set()

    for s, p, o in g:
        if not isinstance(s, URIRef) or not isinstance(o, URIRef):
            continue

        prop_str = str(p)
        mapping = RELATION_MAP.get(prop_str)
        if mapping is None:
            continue

        rel_type, src_label, dst_label = mapping

        src_id = _extract_node_id(s, base_uri)
        dst_id = _extract_node_id(o, base_uri)

        # Deduplicate
        key = (src_id, dst_id, rel_type)
        if key in seen:
            continue
        seen.add(key)

        rels.append({
            "src_id": src_id,
            "dst_id": dst_id,
            "type": rel_type,
            "src_label": src_label,
            "dst_label": dst_label,
        })

    return rels


# ---------------------------------------------------------------------------
# Neo4j import via Cypher MERGE
# ---------------------------------------------------------------------------


def _import_nodes_via_cypher(
    graph: Any,
    nodes: List[Dict[str, Any]],
) -> int:
    """Import nodes into Neo4j using Cypher MERGE commands.

    For each node, generates a MERGE query that:
    - Matches or creates the node by its unique ID
    - Sets all properties

    Args:
        graph: Neo4jGraph instance.
        nodes: List of node dicts.

    Returns:
        Number of nodes imported.
    """
    if not nodes:
        return 0

    count = 0
    for node in nodes:
        node_id = node["id"]
        labels = ":".join(node["labels"])

        # Build SET clause from properties
        set_parts = []
        for prop_name, prop_val in node["properties"].items():
            if isinstance(prop_val, list):
                # List values: set as array
                items = ", ".join(f'"{v}"' for v in prop_val)
                set_parts.append(f'n.`{prop_name}` = [{items}]')
            else:
                escaped = prop_val.replace('"', '\\"')
                set_parts.append(f'n.`{prop_name}` = "{escaped}"')

        if set_parts:
            set_clause = " SET " + " ".join(set_parts)
        else:
            set_clause = ""

        query = f"MERGE (n:{labels} {{id: \"{node_id}\"}}){set_clause}"

        try:
            graph.query(query)
            count += 1
        except Exception:
            # Skip nodes that fail (e.g., constraint violations)
            pass

    return count


def _import_rels_via_cypher(
    graph: Any,
    rels: List[Dict[str, Any]],
) -> int:
    """Import relationships into Neo4j using Cypher MATCH + CREATE commands.

    For each relationship:
    - MATCHes the source and target nodes by ID
    - Creates the relationship with the specified type

    Args:
        graph: Neo4jGraph instance.
        rels: List of relationship dicts.

    Returns:
        Number of relationships imported.
    """
    if not rels:
        return 0

    count = 0
    for rel in rels:
        src_id = rel["src_id"]
        dst_id = rel["dst_id"]
        rel_type = rel["type"]
        src_label = rel.get("src_label", "Node")
        dst_label = rel.get("dst_label", "Node")

        query = (
            f"MATCH (a:{src_label} {{id: \"{src_id}\"}}) "
            f"MATCH (b:{dst_label} {{id: \"{dst_id}\"}}) "
            f"MERGE (a)-[r:{rel_type}]->(b)"
        )

        try:
            graph.query(query)
            count += 1
        except Exception:
            # Skip relationships that fail (e.g., nodes not yet found)
            pass

    return count


# ---------------------------------------------------------------------------
# Main loader
# ---------------------------------------------------------------------------


def load_ric_o_naf(
    graph: Any,
    limit: int = 50,
    max_agents: int = 10,
    max_records: int = 3,
) -> Dict[str, int]:
    """Load RiC-O data from the National Archives of France into Neo4j.

    Downloads RDF/XML files from the National Archives of France RiC-O
    examples and imports them into Neo4j using Cypher MERGE commands.

    Args:
        graph: Neo4jGraph instance.
        limit: Total entities to load (soft limit).
        max_agents: Number of agent files to load.
        max_records: Number of record resource files to load.

    Returns:
        Dict with load statistics:
            - agents: number of agent nodes
            - records: number of record resource nodes
            - things: number of thing nodes
            - children: number of child entity nodes
            - relationships: number of relationships
            - total: total entities loaded
    """
    all_nodes: Dict[str, Dict[str, Any]] = {}
    all_rels: List[Dict[str, Any]] = []
    counters: Dict[str, int] = {
        "agents": 0,
        "records": 0,
        "things": 0,
        "children": 0,
        "relationships": 0,
        "total": 0,
    }

    try:
        # ── 1. Download and parse agent files ─────────────────────────
        agent_files = _list_github_dir(AGENT_URL)[:max_agents]
        print(f"  Downloading {len(agent_files)} agent files...")
        for fname in agent_files:
            url = f"{AGENT_URL}/{fname}"
            g, base_uri = _parse_rdf_file(url, category="agents")

            nodes = _extract_nodes(g, base_uri, "agents")
            rels = _extract_relationships(g, base_uri, "agents")

            for node in nodes:
                if node["id"] not in all_nodes:
                    all_nodes[node["id"]] = node
                    if "Agent" in node["labels"] or "CorporateBody" in node["labels"] or "Person" in node["labels"]:
                        counters["agents"] += 1
                    elif "Thing" in node["labels"]:
                        counters["things"] += 1
                    else:
                        counters["children"] += 1

            all_rels.extend(rels)

        # ── 2. Download and parse record resource files ───────────────
        record_files = _list_github_dir(RECORD_URL)[:max_records]
        print(f"  Downloading {len(record_files)} record resource files...")
        for fname in record_files:
            url = f"{RECORD_URL}/{fname}"
            g, base_uri = _parse_rdf_file(url, category="recordResources")

            nodes = _extract_nodes(g, base_uri, "recordResources")
            rels = _extract_relationships(g, base_uri, "recordResources")

            for node in nodes:
                if node["id"] not in all_nodes:
                    all_nodes[node["id"]] = node
                    if "RecordResource" in node["labels"] or "RecordSet" in node["labels"]:
                        counters["records"] += 1
                    elif "Thing" in node["labels"]:
                        counters["things"] += 1
                    elif "Instantiation" in node["labels"]:
                        counters["children"] += 1
                    else:
                        counters["children"] += 1

            all_rels.extend(rels)

        # ── 3. Download and parse relation files ──────────────────────
        relation_files = _list_github_dir(RELATION_URL)
        print(f"  Downloading {len(relation_files)} relation files...")
        for fname in relation_files[:5]:  # Limit relation files
            url = f"{RELATION_URL}/{fname}"
            g, base_uri = _parse_rdf_file(url, category="relations")

            nodes = _extract_nodes(g, base_uri, "relations")
            rels = _extract_relationships(g, base_uri, "relations")

            for node in nodes:
                if node["id"] not in all_nodes:
                    all_nodes[node["id"]] = node
                    counters["children"] += 1

            all_rels.extend(rels)

        # ── 4. Import nodes into Neo4j ────────────────────────────────
        print(f"  Importing {len(all_nodes)} nodes...")
        node_count = _import_nodes_via_cypher(graph, list(all_nodes.values()))
        print(f"  Imported {node_count} nodes.")

        # ── 5. Import relationships into Neo4j ────────────────────────
        print(f"  Importing {len(all_rels)} relationships...")
        rel_count = _import_rels_via_cypher(graph, all_rels)
        print(f"  Imported {rel_count} relationships.")

        counters["relationships"] = rel_count
        counters["total"] = node_count

    except Exception as exc:
        print(f"  Error loading data: {exc}")
        raise

    return counters
