"""Load RiC-O data from the National Archives of France into Neo4j.

Downloads RDF/XML files from the National Archives of France RiC-O examples
and imports them into Neo4j using Neo4j's native ``LOAD CSV`` bulk import.

The loader:

1. Downloads RDF files from GitHub (agents, recordResources, relations, vocabularies)
2. Parses them with ``rdflib``
3. Extracts nodes and relationships
4. Writes temporary CSV files
5. Uses ``LOAD CSV`` Cypher commands to bulk-import into Neo4j
6. Returns load statistics

Usage::

    from drm.exemples.load_ric_o_naf import load_ric_o_naf

    stats = load_ric_o_naf(graph, limit=50, max_agents=10, max_records=3)
    print(f"Total entities: {stats['total']}")
"""

from __future__ import annotations

import csv
import io
import os
import tempfile
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
    str(ONTO.RecordSet): "RecordResource",  # RecordSet is a subtype of RecordResource
    str(ONTO.Instantiation): "Instantiation",
    str(ONTO.Activity): "Activity",
    str(ONTO.ActivityType): "ActivityType",
    str(ONTO.DocumentaryFormType): "DocumentaryFormType",
    str(ONTO.Language): "Language",
    str(ONTO.CorporateBodyType): "CorporateBodyType",
    str(ONTO.occupationTypes): "OccupationType",
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
    str(ONTO.Contenttype): "ContentType",
    str(ONTO.Extent): "Extent",
    str(ONTO.ExtentType): "ExtentType",
    str(ONTO.UnitOfMeasurement): "UnitOfMeasurement",
    str(ONTO.DemographicGroup): "DemographicGroup",
    str(ONTO.LegalStatus): "LegalStatus",
    str(ONTO.Mandate): "Mandate",
    str(ONTO.MandateType): "MandateType",
    str(ONTO.Mechanism): "Mechanism",
    str(ONTO.OrganicOrFunctionalProvenanceRelation): "OrganicOrFunctionalProvenanceRelation",
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
    req = urllib.request.Request(url, headers={"User-Agent": "drm-tools-rico/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")

    # GitHub returns a simple list of filenames, one per line
    return [line.strip() for line in data.splitlines() if line.strip().endswith(".rdf")]


def _download_file(url: str) -> bytes:
    """Download a file from a URL.

    Args:
        url: The URL to download.

    Returns:
        The file content as bytes.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "drm-tools-rico/1.0"})
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
        return uri_str[len(base_uri) :]
    # Fallback: extract last path segment
    for sep in ("#", "/"):
        if sep in uri_str:
            return uri_str.rsplit(sep, 1)[-1]
    return str(uri)


def _parse_rdf_file(
    url: str,
    limit: Optional[int] = None,
    category: str = "",
) -> Tuple[Graph, str]:
    """Parse a single RDF file and return the graph and its base URI.

    Args:
        url: The URL of the RDF file.
        limit: Not used for parsing (applied at the loader level).
        category: Category name for logging.

    Returns:
        Tuple of (parsed graph, base URI).
    """
    data = _download_file(url)
    g = _parse_rdf(data)

    # Extract base URI
    base_uri = str(g.namespace_manager.normalizeUri(g.identifier)) if g.identifier else ""
    # Try to find xml:base from the graph
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

    for s, p, o in g:
        # Only process subjects that are resources (not literals)
        if not isinstance(s, URIRef):
            continue

        # Check if this subject is an instance of a known class
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
            # Merge labels
            if label not in nodes[node_id]["labels"]:
                nodes[node_id]["labels"].append(label)
            continue

        node_id = _extract_node_id(s, base_uri)
        nodes[node_id] = {
            "id": node_id,
            "labels": [label],
            "properties": {},
        }

    # Now extract properties for each node
    for s in list(nodes.keys()):
        node_id = s
        uri = URIRef(base_uri + node_id) if base_uri else URIRef(node_id)

        for prop_uri, prop in g.predicate_objects(uri):
            prop_str = str(prop_uri)
            prop_name = _local_name(prop_str)

            # Skip RDF type and known relation properties (handled separately)
            if prop_str == str(RDF.type):
                continue
            if prop_str == str(RDFS.subClassOf):
                continue

            if isinstance(prop, Literal):
                val = str(prop)
                if prop.language:
                    val = f"{val}@{prop.language}"
                nodes[node_id]["properties"][prop_name] = val
            elif isinstance(prop, URIRef):
                # Store as a reference (relationship)
                ref_id = _extract_node_id(prop, base_uri)
                prop_key = f"_ref_{_local_name(prop_str)}"
                if prop_key not in nodes[node_id]["properties"]:
                    nodes[node_id]["properties"][prop_key] = []
                nodes[node_id]["properties"][prop_key].append(ref_id)

    return list(nodes.values())


# ---------------------------------------------------------------------------
# Relationship extraction
# ---------------------------------------------------------------------------

# Map of RiC-O properties → (source_node_prop, target_node_prop, rel_type)
RELATION_MAP: Dict[str, Tuple[str, str, str]] = {
    str(ONTO.hasOrganicProvenance): ("recordResourceId", "agentId", "HAS_ORGANIC_PROVENANCE"),
    str(ONTO.isOrWasOrganicProvenanceOf): ("agentId", "recordResourceId", "IS_ORGANIC_PROVENANCE_OF"),
    str(ONTO.directlyIncludes): ("recordResourceId", "recordResourceId", "DIRECTLY_INCLUDES"),
    str(ONTO.isDirectlyIncludedIn): ("recordResourceId", "recordResourceId", "IS_DIRECTLY_INCLUDED_IN"),
    str(ONTO.hasOrHadInstantiation): ("recordResourceId", "instantiationId", "HAS_INSTANTIATION"),
    str(ONTO.isOrWasInstantiationOf): ("instantiationId", "recordResourceId", "IS_INSTANTIATION_OF"),
    str(ONTO.hasOrHadHolder): ("instantiationId", "agentId", "HAS_HOLDER"),
    str(ONTO.hasOrHadLocation): ("instantiationId", "placeId", "HAS_LOCATION"),
    str(ONTO.hasOrHadAgentName): ("agentId", "agentNameId", "HAS_AGENT_NAME"),
    str(ONTO.isOrWasAgentNameOf): ("agentNameId", "agentId", "IS_AGENT_NAME_OF"),
    str(ONTO.hasOrHadCreator): ("recordId", "agentId", "HAS_CREATOR"),
    str(ONTO.hasCreator): ("recordId", "agentId", "HAS_CREATOR"),
    str(ONTO.hasPublisher): ("recordId", "agentId", "HAS_PUBLISHER"),
    str(ONTO.isOrWasDescribedBy): ("agentId", "recordId", "IS_DESCRIBED_BY"),
    str(ONTO.describesOrDescribed): ("recordId", "agentId", "DESCRIBES_OR_DESCRIBED"),
    str(ONTO.hasOrHadController): ("agentId", "agentId", "HAS_CONTROLLER"),
    str(ONTO.hasOrHadEmployer): ("agentId", "agentId", "HAS_EMPLOYER"),
    str(ONTO.hasOrHadMember): ("groupOrFamilyId", "agentId", "HAS_MEMBER"),
    str(ONTO.hasOrHadSpouse): ("agentId", "agentId", "HAS_SPOUSE"),
    str(ONTO.hasOrHadStudent): ("agentId", "agentId", "HAS_STUDENT"),
    str(ONTO.hasOrHadTeacher): ("agentId", "agentId", "HAS_TEACHER"),
    str(ONTO.hasOrHadChild): ("agentId", "agentId", "HAS_CHILD"),
    str(ONTO.hasOrHadParent): ("agentId", "agentId", "HAS_PARENT"),
    str(ONTO.hasOrHadHierarchicalRelation): ("agentId", "agentId", "HAS_HIERARCHICAL_RELATION"),
    str(ONTO.hasOrHadTemporalRelation): ("agentId", "agentId", "HAS_TEMPORAL_RELATION"),
    str(ONTO.hasOrHadAgentToAgentRelation): ("agentId", "agentId", "HAS_AGENT_TO_AGENT_RELATION"),
    str(ONTO.hasOrHadSubject): ("recordResourceId", "thingId", "HAS_SUBJECT"),
    str(ONTO.hasOrHadMainsubject): ("recordResourceId", "thingId", "HAS_MAIN_SUBJECT"),
    str(ONTO.hasOrHadLanguage): ("recordId", "languageId", "HAS_LANGUAGE"),
    str(ONTO.hasOrHadDocumentaryFormType): ("recordId", "documentaryFormTypeId", "HAS_DOCUMENTARY_FORM_TYPE"),
    str(ONTO.hasOrHadCorporateBodyType): ("corporateBodyId", "corporateBodyTypeId", "HAS_CORPORATE_BODY_TYPE"),
    str(ONTO.hasOrHadIdentifier): ("agentId", "identifierId", "HAS_IDENTIFIER"),
    str(ONTO.hasOrHadBirthDate): ("agentId", "dateId", "HAS_BIRTH_DATE"),
    str(ONTO.hasOrHadDeathDate): ("agentId", "dateId", "HAS_DEATH_DATE"),
    str(ONTO.hasOrHadBirthPlace): ("agentId", "placeId", "HAS_BIRTH_PLACE"),
    str(ONTO.hasOrHadDeathPlace): ("agentId", "placeId", "HAS_DEATH_PLACE"),
    str(ONTO.hasOrHadOccupation): ("agentId", "occupationId", "HAS_OCCUPATION"),
    str(ONTO.hasOrHadPosition): ("agentId", "positionId", "HAS_POSITION"),
    str(ONTO.hasOrHadRole): ("agentId", "roleTypeId", "HAS_ROLE"),
    str(ONTO.hasOrHadDate): ("recordResourceId", "dateId", "HAS_DATE"),
    str(ONTO.hasOrHadTitle): ("recordResourceId", "titleId", "HAS_TITLE"),
    str(ONTO.hasOrHadExtent): ("recordResourceId", "extentId", "HAS_EXTENT"),
    str(ONTO.hasOrHadContentType): ("recordResourceId", "contentType", "HAS_CONTENT_TYPE"),
    str(ONTO.hasOrHadRecordState): ("recordResourceId", "recordStateId", "HAS_RECORD_STATE"),
    str(ONTO.hasOrHadLegalStatus): ("recordResourceId", "legalStatusId", "HAS_LEGAL_STATUS"),
    str(ONTO.hasOrHadCreationDate): ("recordResourceId", "dateId", "HAS_CREATION_DATE"),
    str(ONTO.hasOrHadPublicationDate): ("recordResourceId", "dateId", "HAS_PUBLICATION_DATE"),
    str(ONTO.hasOrHadModificationDate): ("recordResourceId", "dateId", "HAS_MODIFICATION_DATE"),
    str(ONTO.hasOrHadMigrationDate): ("recordResourceId", "dateId", "HAS_MIGRATION_DATE"),
    str(ONTO.hasOrHadDerivationRelation): ("instantiationId", "instantiationId", "HAS_DERIVATION_RELATION"),
    str(ONTO.hasOrHadAnalogueInstantiation): ("instantiationId", "instantiationId", "HAS_ANALOGUE_INSTANTIATION"),
    str(ONTO.hasOrHadDigitalInstantiation): ("recordId", "instantiationId", "HAS_DIGITAL_INSTANTIATION"),
    str(ONTO.hasOrHadDirectPart): ("recordResourceId", "recordResourceId", "HAS_DIRECT_PART"),
    str(ONTO.isOrWasPartOf): ("recordResourceId", "recordResourceId", "IS_PART_OF"),
    str(ONTO.directlyPrecedesInSequence): ("recordResourceId", "recordResourceId", "DIRECTLY_PRECEDES"),
    str(ONTO.isOrWasAffectedBy): ("recordId", "activityId", "IS_AFFECTED_BY"),
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
        List of relationship dicts with keys: src_id, dst_id, type, properties.
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

        src_key, dst_key, rel_type = mapping

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
            "properties": {},
        })

    return rels


# ---------------------------------------------------------------------------
# CSV generation
# ---------------------------------------------------------------------------


def _write_nodes_csv(
    nodes: List[Dict[str, Any]],
    path: str,
) -> int:
    """Write nodes to a CSV file for Neo4j LOAD CSV.

    Format:
        :ID,label,property1,property2,...

    Args:
        nodes: List of node dicts.
        path: Output CSV file path.

    Returns:
        Number of nodes written.
    """
    if not nodes:
        return 0

    # Collect all property keys
    all_props: Set[str] = set()
    for node in nodes:
        all_props.update(node["properties"].keys())

    fieldnames = [":ID", "label"] + sorted(all_props)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for node in nodes:
            row: Dict[str, Any] = {
                ":ID": node["id"],
                "label": "|".join(node["labels"]),
            }
            for prop_name, prop_val in node["properties"].items():
                if isinstance(prop_val, list):
                    row[prop_name] = "|".join(prop_val)
                else:
                    row[prop_name] = prop_val
            writer.writerow(row)

    return len(nodes)


def _write_rels_csv(
    rels: List[Dict[str, Any]],
    path: str,
) -> int:
    """Write relationships to a CSV file for Neo4j LOAD CSV.

    Format:
        :START_ID,:END_ID,:TYPE,property1,...

    Args:
        rels: List of relationship dicts.
        path: Output CSV file path.

    Returns:
        Number of relationships written.
    """
    if not rels:
        return 0

    # Collect all property keys
    all_props: Set[str] = set()
    for rel in rels:
        all_props.update(rel["properties"].keys())

    fieldnames = [":START_ID", ":END_ID", ":TYPE"] + sorted(all_props)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for rel in rels:
            row: Dict[str, Any] = {
                ":START_ID": rel["src_id"],
                ":END_ID": rel["dst_id"],
                ":TYPE": rel["type"],
            }
            for prop_name, prop_val in rel["properties"].items():
                row[prop_name] = prop_val
            writer.writerow(row)

    return len(rels)


# ---------------------------------------------------------------------------
# Neo4j LOAD CSV import
# ---------------------------------------------------------------------------


def _load_csv_to_neo4j(
    graph: Any,
    nodes_csv: str,
    rels_csv: str,
) -> Dict[str, int]:
    """Import CSV files into Neo4j using LOAD Cypher commands.

    Args:
        graph: Neo4jGraph instance.
        nodes_csv: Path to nodes CSV file.
        rels_csv: Path to relationships CSV file.

    Returns:
        Dict with import statistics.
    """
    stats: Dict[str, int] = {"nodes": 0, "relationships": 0}

    # Import nodes
    nodes_query = (
        "LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row "
        "FIELDTERMINATOR ',' "
        "MERGE (n {id: row.id}) "
        "SET n += row"
    )

    # We need to set the file directory for Neo4j
    # Use the neo4j-admin import approach or set the import directory
    # For simplicity, we use the file:// protocol with the Neo4j import directory

    # Alternative: use the graph's query method with the import directory
    try:
        # Try to find the Neo4j import directory
        import_dir = _get_neo4j_import_dir()

        # Copy CSV files to Neo4j import directory
        if import_dir:
            import shutil
            nodes_dest = os.path.join(import_dir, "nodes.csv")
            rels_dest = os.path.join(import_dir, "relationships.csv")

            shutil.copy2(nodes_csv, nodes_dest)
            shutil.copy2(rels_csv, rels_dest)

            # Import nodes
            result = graph.query(
                "LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row "
                "FIELDTERMINATOR ',' "
                "MERGE (n {id: row.id}) "
                "SET n += row"
            )
            stats["nodes"] = len(result) if result else 0

            # Import relationships
            result = graph.query(
                "LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row "
                "FIELDTERMINATOR ',' "
                "MATCH (a {id: row.`:START_ID`}) "
                "MATCH (b {id: row.`:END_ID`}) "
                "CALL apoc.create.relationship(a, row.`:TYPE`, row, b) YIELD rel "
                "RETURN count(rel) AS count"
            )
            stats["relationships"] = result[0]["count"] if result and len(result) > 0 else 0
        else:
            # Fallback: use createNode/createRelationship directly
            stats = _fallback_import(graph, nodes_csv, rels_csv)
    except Exception as exc:
        # Fallback to direct insertion
        stats = _fallback_import(graph, nodes_csv, rels_csv)

    return stats


def _get_neo4j_import_dir() -> Optional[str]:
    """Detect the Neo4j import directory.

    Returns:
        Path to the import directory, or None if not found.
    """
    candidates = [
        "/var/lib/neo4j/import",
        "/usr/local/neo4j/import",
        os.path.expanduser("~/.neo4j/import"),
    ]

    # Try to get from Neo4j configuration
    import subprocess

    try:
        result = subprocess.run(
            ["neo4j", "config", "settings", "server.directories.import"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            candidates.insert(0, result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    for candidate in candidates:
        if os.path.isdir(candidate):
            return candidate

    return None


def _fallback_import(
    graph: Any,
    nodes_csv: str,
    rels_csv: str,
) -> Dict[str, int]:
    """Fallback import using direct Node/Relation insertion.

    Reads CSV files and inserts nodes/relations one by one using
    the Neo4jGraph API.

    Args:
        graph: Neo4jGraph instance.
        nodes_csv: Path to nodes CSV file.
        rels_csv: Path to relationships CSV file.

    Returns:
        Dict with import statistics.
    """
    from drm.base import Node, Relation

    stats: Dict[str, int] = {"nodes": 0, "relationships": 0}

    # Import nodes from CSV
    with open(nodes_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            node_id = row.pop(":ID", None)
            label = row.pop("label", "Node")
            if not node_id:
                continue

            node = Node(
                pk={"id": node_id},
                main_label=label,
                **{k: v for k, v in row.items() if v},
            )
            graph.insertNode(node, replace=True)
            stats["nodes"] += 1

    # Import relationships from CSV
    with open(rels_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src_id = row.pop(":START_ID", None)
            dst_id = row.pop(":END_ID", None)
            rel_type = row.pop(":TYPE", None)
            if not src_id or not dst_id or not rel_type:
                continue

            src = Node(pk={"id": src_id}, main_label="Node")
            dst = Node(pk={"id": dst_id}, main_label="Node")
            graph.insertRelation(
                Relation(src, dst, rel_type),
                update=True,
            )
            stats["relationships"] += 1

    return stats


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
    examples and imports them into Neo4j using Neo4j's native
    ``LOAD CSV`` bulk import.

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

    # Temporary directory for CSV files
    tmpdir = tempfile.mkdtemp(prefix="ric_o_")

    try:
        # ── 1. Download and parse agent files ─────────────────────────
        agent_files = _list_github_dir(AGENT_URL)[:max_agents]
        for fname in agent_files:
            url = f"{AGENT_URL}/{fname}"
            g, base_uri = _parse_rdf_file(url, category="agents")

            nodes = _extract_nodes(g, base_uri, "agents")
            rels = _extract_relationships(g, base_uri, "agents")

            for node in nodes:
                if node["id"] not in all_nodes:
                    all_nodes[node["id"]] = node
                    # Count by label
                    if "Agent" in node["labels"] or "CorporateBody" in node["labels"] or "Person" in node["labels"]:
                        counters["agents"] += 1
                    elif "Thing" in node["labels"]:
                        counters["things"] += 1
                    else:
                        counters["children"] += 1

            all_rels.extend(rels)

        # ── 2. Download and parse record resource files ───────────────
        record_files = _list_github_dir(RECORD_URL)[:max_records]
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

        # ── 4. Write CSV files ───────────────────────────────────────
        nodes_csv = os.path.join(tmpdir, "nodes.csv")
        rels_csv = os.path.join(tmpdir, "relationships.csv")

        node_count = _write_nodes_csv(list(all_nodes.values()), nodes_csv)
        rel_count = _write_rels_csv(all_rels, rels_csv)

        # ── 5. Import into Neo4j ─────────────────────────────────────
        import_stats = _load_csv_to_neo4j(graph, nodes_csv, rels_csv)

        counters["relationships"] = import_stats.get("relationships", 0)
        counters["total"] = import_stats.get("nodes", 0)

    finally:
        # Clean up temporary files
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    return counters
