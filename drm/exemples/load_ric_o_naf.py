"""Load RiC-O data from the National Archives of France example.

Downloads RDF/XML files from the ICA-EGAD/RiC-O repository
and converts them into DRM graph entities (Thing, Agent,
RecordResource, Instantiation, etc.).

Usage::

    from drm.exemples import load_ric_o_naf
    load_ric_o_naf(graph, limit=5)
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

import requests

from drm.base import Node, WeakNode

# ── Namespace map ────────────────────────────────────────────────────
_NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "rico": "https://www.ica.org/standards/RiC/ontology#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "html": "http://www.w3.org/1999/xhtml#",
}
_R = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
_RI = "https://www.ica.org/standards/RiC/ontology#"

_RI_CO_BASE = (
    "https://raw.githubusercontent.com/ICA-EGAD/RiC-O/"
    "master/examples/examples_v1-1/NationalArchivesOfFrance/rdf-xml"
)


def _url(cat: str, fname: str) -> str:
    """Return download URL for an RDF file."""
    return f"{_RI_CO_BASE}/{cat}/{fname}"


def _local(uri: str) -> str:
    """Convert a RiC-O URI to a short local identifier.

    Examples:
        agent/000005 → agent-000005
        recordResource/top-003500 → recordResource-top-003500
    """
    if "#" in uri:
        uri = uri.split("#")[-1]
    uri = uri.replace("/", "-")
    return uri[:80] if len(uri) > 80 else uri


def _text(elem: ET.Element, tag: str) -> Optional[str]:
    """Extract text from a rico:tag or rdfs:label element."""
    c = elem.find(f"{{{_RI}}}{tag}")
    if c is not None and c.text:
        return c.text.strip()
    if tag == "label":
        c = elem.find("rdfs:label", _NS)
        if c is not None and c.text:
            return c.text.strip()
    return None


def _uri(elem: ET.Element, tag: str) -> Optional[str]:
    """Get rdf:resource attribute from a rico:tag element."""
    c = elem.find(f"{{{_RI}}}{tag}")
    if c is not None:
        r = c.get(f"{{{_R}}}resource")
        return _local(r) if r else None
    return None


def _uri_list(elem: ET.Element, tag: str) -> List[str]:
    """Get all rdf:resource values from rico:tag elements."""
    result = []
    for c in elem.findall(f"{{{_RI}}}{tag}"):
        r = c.get(f"{{{_R}}}resource")
        if r:
            result.append(_local(r))
    return result


def _short_type(uri: str) -> str:
    """Extract short type name from a URI."""
    if not uri:
        return ""
    return uri.split("#")[-1] if "#" in uri else uri.split("/")[-1]


# ── Entity extraction ──────────────────────────────────────────────

class _Entity:
    """Internal representation of a parsed RDF entity."""

    def __init__(self) -> None:
        self.id: str = ""
        self.type: str = ""
        self.label: str = ""
        self.props: Dict[str, Any] = {}
        self.names: List[Dict[str, Any]] = []
        self.children: List["_Entity"] = []
        self.relations: List[Tuple[str, str]] = []  # (target_id, rel_type)


def _parse_agent_name(elem: ET.Element) -> Optional[Dict[str, Any]]:
    """Parse a hasOrHadAgentName element.

    Structure: hasOrHadAgentName > AgentName > label/textualValue
    """
    # Look for nested AgentName element
    agent_name_elem = elem.find(f"{{{_RI}}}AgentName")
    if agent_name_elem is not None:
        # Check rdfs:label first
        rlabel = agent_name_elem.find("rdfs:label", _NS)
        if rlabel is not None and rlabel.text:
            label = rlabel.text.strip()
        else:
            # Fall back to textualValue
            tv = agent_name_elem.find(f"{{{_RI}}}textualValue")
            if tv is not None and tv.text:
                label = tv.text.strip()
            else:
                label = None
    else:
        # Direct label/textualValue on hasOrHadAgentName
        rlabel = elem.find("rdfs:label", _NS)
        if rlabel is not None and rlabel.text:
            label = rlabel.text.strip()
        else:
            tv = elem.find(f"{{{_RI}}}textualValue")
            if tv is not None and tv.text:
                label = tv.text.strip()
            else:
                label = None

    if not label:
        return None

    name: Dict[str, Any] = {"label": label}

    # textualValue (either on AgentName or directly on hasOrHadAgentName)
    textual = agent_name_elem if agent_name_elem is not None else elem
    tv = textual.find(f"{{{_RI}}}textualValue")
    if tv is not None and tv.text:
        name["textualValue"] = tv.text.strip()

    # usedFromDate / usedToDate
    uf = textual.find(f"{{{_RI}}}usedFromDate")
    if uf is not None and uf.text:
        name["usedFromDate"] = uf.text.strip()
    ut = textual.find(f"{{{_RI}}}usedToDate")
    if ut is not None and ut.text:
        name["usedToDate"] = ut.text.strip()

    # type
    nt = textual.find(f"{{{_RI}}}type")
    if nt is not None and nt.text:
        name["type"] = nt.text.strip()

    return name


def _parse_agent(elem: ET.Element, about: str) -> _Entity:
    """Parse a rico:Agent element."""
    ent = _Entity()
    ent.id = _local(f"agent/{about}")

    # Determine subtype
    type_elem = elem.find(f"{{{_RI}}}type")
    if type_elem is not None:
        ent.type = _short_type(type_elem.get(f"{{{_R}}}resource", ""))
    else:
        ent.type = "Agent"
    ent.label = ent.type

    # Label
    label = _text(elem, "label")
    if label:
        ent.props["label"] = label

    # Agent names (inline)
    for ne in elem.findall(f"{{{_RI}}}hasOrHadAgentName"):
        parsed = _parse_agent_name(ne)
        if parsed:
            ent.names.append(parsed)

    # Dates
    bd = _text(elem, "beginningDate")
    if bd:
        ent.props["beginningDate"] = bd
    ed = _text(elem, "endDate")
    if ed:
        ent.props["endDate"] = ed

    # Subdivisions (organizational hierarchy)
    for sub in _uri_list(elem, "hasDirectSubdivision"):
        ent.relations.append((sub, "hasDirectSubdivision"))
    for sub in _uri_list(elem, "hadSubdivision"):
        ent.relations.append((sub, "hadSubdivision"))
    for sub in _uri_list(elem, "hasDirectSubordinate"):
        ent.relations.append((sub, "hasDirectSubordinate"))

    # Described by Record
    desc = _uri(elem, "isOrWasDescribedBy")
    if desc:
        ent.props["describedBy"] = desc

    # Instantiations
    for ie in elem.findall(f"{{{_RI}}}hasOrHadDigitalInstantiation"):
        inst = _parse_instantiation(ie)
        if inst:
            ent.children.append(inst)

    return ent


def _parse_instantiation(elem: ET.Element) -> Optional[_Entity]:
    """Parse a rico:Instantiation element."""
    about = elem.get(f"{_R}about", "")
    ent = _Entity()
    ent.id = _local(f"instantiation/{about}") if about else f"instantiation-{id(elem)}"
    ent.type = "Instantiation"
    ent.label = "Instantiation"

    ident = elem.find(f"{{{_RI}}}identifier")
    if ident is not None and ident.text:
        ent.props["identifier"] = ident.text.strip()
    title = _text(elem, "title")
    if title:
        ent.props["title"] = title
    fmt = _text(elem, "format")
    if fmt:
        ent.props["format"] = fmt
    loc = _uri(elem, "hasOrHadLocation")
    if loc:
        ent.relations.append((loc, "hasLocation"))
    return ent


def _parse_record_resource(elem: ET.Element, about: str) -> _Entity:
    """Parse a rico:RecordResource element."""
    ent = _Entity()
    ent.id = _local(f"recordResource/{about}")

    # Determine subtype
    type_elem = elem.find(f"{{{_RI}}}type")
    if type_elem is not None:
        ent.type = _short_type(type_elem.get(f"{{{_R}}}resource", ""))
    else:
        ent.type = "RecordResource"
    ent.label = ent.type

    # Title
    title = _text(elem, "title")
    if title:
        ent.props["title"] = title
    rlabel = _text(elem, "label")
    if rlabel:
        ent.props["rdfsLabel"] = rlabel

    # Dates
    bd = _text(elem, "beginningDate")
    if bd:
        ent.props["beginningDate"] = bd
    ed = _text(elem, "endDate")
    if ed:
        ent.props["endDate"] = ed
    dt = _text(elem, "date")
    if dt:
        ent.props["date"] = dt

    # Record set type
    rst = _uri(elem, "hasRecordSetType")
    if rst:
        ent.props["recordSetType"] = _short_type(rst)

    # Provenance
    for prov in _uri_list(elem, "hasOrganicProvenance"):
        ent.relations.append((prov, "hasOrganicProvenance"))

    # Holder
    holder = _uri(elem, "hasOrHadHolder")
    if holder:
        ent.relations.append((holder, "hasHolder"))

    # Instantiations
    for ie in elem.findall(f"{{{_RI}}}hasOrHadInstantiation"):
        inst = _parse_instantiation(ie)
        if inst:
            ent.children.append(inst)

    # Hierarchical containment
    for inc in _uri_list(elem, "directlyIncludes"):
        ent.relations.append((inc, "directlyIncludes"))
    for inc in _uri_list(elem, "isDirectlyIncludedIn"):
        ent.relations.append((inc, "isDirectlyIncludedIn"))
    for part in _uri_list(elem, "hasDirectPart"):
        ent.relations.append((part, "hasDirectPart"))

    # Sequence ordering
    for nxt in _uri_list(elem, "directlyFollowsInSequence"):
        ent.relations.append((nxt, "directlyFollowsInSequence"))
    for prev in _uri_list(elem, "directlyPrecedesInSequence"):
        ent.relations.append((prev, "directlyPrecedesInSequence"))

    return ent


def _parse_record(elem: ET.Element) -> Optional[_Entity]:
    """Parse a rico:Record element (metadata envelope)."""
    about = elem.get(f"{{{_R}}}about", "")
    if not about:
        return None

    rec = _Entity()
    rec.id = _local(about)
    rec.type = "Record"
    rec.label = "Record"

    # Title
    title = _text(elem, "title")
    if title:
        rec.props["title"] = title

    # Documentary form type
    dft = _uri(elem, "hasDocumentaryFormType")
    if dft:
        rec.props["documentaryFormType"] = _short_type(dft)

    # Dates
    cd = _text(elem, "creationDate")
    if cd:
        rec.props["creationDate"] = cd
    md = _text(elem, "lastModificationDate")
    if md:
        rec.props["lastModificationDate"] = md

    # Describes agent or record resource
    desc = _uri(elem, "describesOrDescribed")
    if desc:
        rec.relations.append((desc, "describes"))

    # Has creator
    creator = _uri(elem, "hasCreator")
    if creator:
        rec.relations.append((creator, "hasCreator"))

    # Affected by (Activity)
    for ae in elem.findall(f"{{{_RI}}}isOrWasAffectedBy"):
        act = _Entity()
        act.type = "Activity"
        act.label = "Activity"
        name_elem = ae.find(f"{{{_RI}}}name")
        if name_elem is not None and name_elem.text:
            act.props["name"] = name_elem.text.strip()
        date_elem = ae.find(f"{{{_RI}}}date")
        if date_elem is not None and date_elem.text:
            act.props["date"] = date_elem.text.strip()
        rec.children.append(act)

    return rec


# ── File parser ────────────────────────────────────────────────────

def _parse_rdf_file(xml_text: str) -> List[Tuple[str, _Entity]]:
    """Parse an RDF/XML file and return list of (type, Entity)."""
    entities: List[Tuple[str, _Entity]] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return entities

    for child in root:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        about = child.get(f"{{{_R}}}about", "")

        if tag == "Record" and about:
            rec = _parse_record(child)
            if rec:
                entities.append(("Record", rec))

        elif tag in ("Agent", "CorporateBody", "Individual", "Family"):
            if not about:
                continue
            ent = _parse_agent(child, about)
            entities.append((ent.type, ent))

        elif tag == "RecordResource":
            if not about:
                continue
            ent = _parse_record_resource(child, about)
            entities.append((ent.type, ent))

        elif tag == "Instantiation":
            inst = _parse_instantiation(child)
            if inst:
                entities.append(("Instantiation", inst))

    return entities


# ── Public loader ──────────────────────────────────────────────────

def load_ric_o_naf(
    graph: Any,
    limit: int = 10,
    max_agents: int = 10,
    max_records: int = 3,
) -> Dict[str, int]:
    """Load RiC-O data from the National Archives of France example.

    Downloads RDF/XML files from the ICA-EGAD/RiC-O GitHub repository
    and converts them into DRM graph entities.

    **Mapping:**

    .. code-block:: text

        rico:Record          → Thing (strong node)
        rico:Agent           → Agent (WeakNode of Thing)
        rico:CorporateBody   → CorporateBody (WeakNode of Agent)
        rico:Individual      → Person (WeakNode of Agent)
        rico:Family          → Family (WeakNode of Agent)
        rico:AgentName       → AgentName (WeakNode of Agent/Person)
        rico:RecordResource  → RecordResource (WeakNode of Thing)
        rico:Instantiation   → Instantiation (WeakNode of Thing/RecordResource)
        rico:Activity        → Activity (WeakNode)

    **Hierarchy examples:**

    .. code-block:: text

        Record (Thing)
        └── Agent (WeakNode)
            ├── AgentName (WeakNode of Agent)
            └── Instantiation (WeakNode of Agent)

        Record (Thing)
        └── RecordResource (WeakNode)
            ├── Instantiation (WeakNode of RecordResource)
            └── RecordResource (WeakNode, via directlyIncludes)

    Args:
        graph: A GraphStore instance (Neo4jGraph or NetworkXGraph).
        limit: Total number of RDF entities to load (soft limit).
        max_agents: Maximum number of agent files to load.
        max_records: Maximum number of record resource files to load.

    Returns:
        A dict with counts: ``{"agents": N, "records": N, "things": N, "total": N}``.
    """
    from drm.rico_entities import (
        Thing,
        Agent,
        CorporateBody,
        Person,
        Family,
        AgentName,
        RecordResource,
        Instantiation,
        Activity,
    )

    stats: Dict[str, int] = {"agents": 0, "records": 0, "things": 0, "total": 0}
    entity_map: Dict[str, Node] = {}
    strong_nodes: List[Node] = []
    weak_nodes: List[Node] = []
    total_loaded = 0

    def _make_thing(eid: str, name: str) -> Thing:
        t = Thing(pk={"identifier": eid}, identifier=eid)
        entity_map[eid] = t
        strong_nodes.append(t)
        stats["things"] += 1
        return t

    def _make_agent(props: dict, parent: Thing) -> Node:
        label = props.get("label", props["id"])
        agent_id = props["id"]
        if agent_id not in entity_map:
            node: Node
            if props.get("_type") == "CorporateBody":
                node = CorporateBody(
                    parent=parent,
                    pk={"agentId": agent_id},
                    beginningDate=props.get("beginningDate"),
                    endDate=props.get("endDate"),
                )
            elif props.get("_type") == "Individual":
                node = Person(
                    parent=parent,
                    pk={"agentId": agent_id},
                    beginningDate=props.get("beginningDate"),
                    endDate=props.get("endDate"),
                )
            elif props.get("_type") == "Family":
                node = Family(
                    parent=parent,
                    pk={"agentId": agent_id},
                    beginningDate=props.get("beginningDate"),
                    endDate=props.get("endDate"),
                )
            else:
                node = Agent(
                    parent=parent,
                    pk={"agentId": agent_id},
                    beginningDate=props.get("beginningDate"),
                    endDate=props.get("endDate"),
                )
            entity_map[agent_id] = node
            stats["agents"] += 1
            weak_nodes.append(node)

            # Attach agent names as WeakNodes
            for i, name_data in enumerate(props.get("names", [])):
                name_id = f"{agent_id}-name-{i}"
                an = AgentName(
                    parent=node,
                    pk={"nameId": name_id},
                    fullName=name_data.get("label", ""),
                    usedFromDate=name_data.get("usedFromDate"),
                    usedToDate=name_data.get("usedToDate"),
                )
                entity_map[name_id] = an
                weak_nodes.append(an)

            # Attach instantiations as WeakNodes
            for i, inst_data in enumerate(props.get("instantiations", [])):
                inst_id = inst_data.get("id", f"inst-{agent_id}-{i}")
                inst_node = Instantiation(
                    parent=node,
                    pk={"instantiationId": inst_data.get("identifier") or inst_id},
                    identifier=inst_data.get("identifier") or None,
                    title=inst_data.get("title") or None,
                    format=inst_data.get("format") or None,
                )
                entity_map[inst_id] = inst_node
                weak_nodes.append(inst_node)

        return entity_map[agent_id]

    def _make_record_resource(props: dict, parent: Thing) -> Node:
        rr_id = props["id"]
        if rr_id not in entity_map:
            rr = RecordResource(
                parent=parent,
                pk={"recordResourceId": rr_id},
                title=props.get("title", ""),
                beginningDate=props.get("beginningDate"),
                endDate=props.get("endDate"),
                date=props.get("date"),
                recordSetType=props.get("recordSetType"),
            )
            entity_map[rr_id] = rr
            stats["records"] += 1
            weak_nodes.append(rr)

            # Attach instantiations
            for inst_data in props.get("instantiations", []):
                inst_id = inst_data.get("id", f"inst-{rr_id}-{len(props.get('instantiations', []))}")
                inst_node = Instantiation(
                    parent=rr,
                    pk={"instantiationId": inst_data.get("identifier") or inst_id},
                    identifier=inst_data.get("identifier") or None,
                    title=inst_data.get("title") or None,
                    format=inst_data.get("format") or None,
                )
                entity_map[inst_id] = inst_node
                weak_nodes.append(inst_node)

        return entity_map[rr_id]

    # ── 1. Load agent files ───────────────────────────────────────
    try:
        resp = requests.get(
            "https://api.github.com/repos/ICA-EGAD/RiC-O/contents/examples/examples_v1-1/NationalArchivesOfFrance/rdf-xml/agents",
            timeout=30,
        )
        resp.raise_for_status()
        agent_files = [f["name"] for f in resp.json() if f["name"].endswith(".rdf")]
    except Exception:
        agent_files = []
    agent_files = agent_files[:max_agents]

    for fname in agent_files:
        if total_loaded >= limit:
            break
        try:
            resp = requests.get(_url("agents", fname), timeout=30)
            resp.raise_for_status()
        except Exception:
            continue

        entities = _parse_rdf_file(resp.text)
        for etype, ent in entities:
            if total_loaded >= limit:
                break

            if etype == "Record":
                # Create Thing from Record
                rec_name = ent.props.get("title", ent.id)
                thing = _make_thing(ent.id, rec_name)
                total_loaded += 1

            elif etype in ("Agent", "CorporateBody", "Individual", "Family"):
                # Create Agent with parent Thing
                # Find or create parent Thing
                parent = None
                # Try to find parent from describedBy relationship
                described_by = ent.props.get("describedBy")
                if described_by and described_by in entity_map:
                    parent = entity_map[described_by]
                if parent is None:
                    # Create a standalone Thing
                    agent_name = ent.props.get("label", ent.id)
                    parent = _make_thing(f"thing-agent-{ent.id}", agent_name)

                agent_node = _make_agent(
                    {
                        "id": ent.id,
                        "label": ent.props.get("label", ent.id),
                        "beginningDate": ent.props.get("beginningDate"),
                        "endDate": ent.props.get("endDate"),
                        "_type": ent.type,
                        "names": ent.names,
                        "instantiations": [
                            {"id": c.id, "identifier": c.props.get("identifier", ""),
                             "title": c.props.get("title", ""), "format": c.props.get("format", "")}
                            for c in ent.children if c.type == "Instantiation"
                        ],
                    },
                    parent,
                )
                total_loaded += 1

            elif etype == "RecordResource":
                # Create RecordResource with parent Thing
                parent = None
                # Try to find parent from relations
                for rel_target, rel_type in ent.relations:
                    if rel_type == "isDirectlyIncludedIn" and rel_target in entity_map:
                        parent = entity_map[rel_target]
                        break
                if parent is None:
                    rr_name = ent.props.get("title", ent.id)
                    parent = _make_thing(f"thing-rr-{ent.id}", rr_name)

                rr_node = _make_record_resource(
                    {
                        "id": ent.id,
                        "title": ent.props.get("title", ""),
                        "beginningDate": ent.props.get("beginningDate"),
                        "endDate": ent.props.get("endDate"),
                        "date": ent.props.get("date"),
                        "recordSetType": ent.props.get("recordSetType"),
                        "instantiations": [
                            {"id": c.id, "identifier": c.props.get("identifier", ""),
                             "title": c.props.get("title", ""), "format": c.props.get("format", "")}
                            for c in ent.children if c.type == "Instantiation"
                        ],
                    },
                    parent,
                )
                total_loaded += 1

            elif etype == "Instantiation":
                # Find parent (RecordResource or Agent)
                parent = None
                for nid, nnode in entity_map.items():
                    if nnode.main_label in ("RecordResource", "Agent", "CorporateBody", "Person", "Family"):
                        parent = nnode
                        break
                if parent is None:
                    parent = strong_nodes[-1] if strong_nodes else None
                if parent is None:
                    parent = _make_thing(f"thing-inst-{ent.id}", "Instantiation")

                inst_node = Instantiation(
                    parent=parent,
                    pk={"instantiationId": ent.props.get("identifier") or ent.id},
                    identifier=ent.props.get("identifier") or None,
                    title=ent.props.get("title") or None,
                    format=ent.props.get("format") or None,
                )
                entity_map[ent.id] = inst_node
                weak_nodes.append(inst_node)
                total_loaded += 1

    # ── 2. Load record resource files ─────────────────────────────
    try:
        resp = requests.get(
            "https://api.github.com/repos/ICA-EGAD/RiC-O/contents/examples/examples_v1-1/NationalArchivesOfFrance/rdf-xml/recordResources",
            timeout=30,
        )
        resp.raise_for_status()
        rr_files = [f["name"] for f in resp.json() if f["name"].endswith(".rdf")]
    except Exception:
        rr_files = []
    rr_files = rr_files[:max_records]

    for fname in rr_files:
        if total_loaded >= limit:
            break
        try:
            resp = requests.get(_url("recordResources", fname), timeout=30)
            resp.raise_for_status()
        except Exception:
            continue

        entities = _parse_rdf_file(resp.text)
        for etype, ent in entities:
            if total_loaded >= limit:
                break

            if etype == "Record":
                rec_name = ent.props.get("title", ent.id)
                thing = _make_thing(ent.id, rec_name)
                total_loaded += 1

            elif etype == "RecordResource":
                parent = None
                for rel_target, rel_type in ent.relations:
                    if rel_type == "isDirectlyIncludedIn" and rel_target in entity_map:
                        parent = entity_map[rel_target]
                        break
                if parent is None:
                    rr_name = ent.props.get("title", ent.id)
                    parent = _make_thing(f"thing-rr-{ent.id}", rr_name)

                rr_node = _make_record_resource(
                    {
                        "id": ent.id,
                        "title": ent.props.get("title", ""),
                        "beginningDate": ent.props.get("beginningDate"),
                        "endDate": ent.props.get("endDate"),
                        "date": ent.props.get("date"),
                        "recordSetType": ent.props.get("recordSetType"),
                        "instantiations": [
                            {"id": c.id, "identifier": c.props.get("identifier", ""),
                             "title": c.props.get("title", ""), "format": c.props.get("format", "")}
                            for c in ent.children if c.type == "Instantiation"
                        ],
                    },
                    parent,
                )
                total_loaded += 1

            elif etype == "Instantiation":
                parent = None
                for nid, nnode in entity_map.items():
                    if nnode.main_label in ("RecordResource", "Agent", "CorporateBody", "Person", "Family"):
                        parent = nnode
                        break
                if parent is None:
                    parent = strong_nodes[-1] if strong_nodes else None
                if parent is None:
                    parent = _make_thing(f"thing-inst-{ent.id}", "Instantiation")

                inst_id = ent.props.get("identifier", ent.id) or None
                inst_node = Instantiation(
                    parent=parent,
                    pk={"instantiationId": inst_id},
                    identifier=ent.props.get("identifier") or None,
                    title=ent.props.get("title") or None,
                )
                entity_map[ent.id] = inst_node
                weak_nodes.append(inst_node)
                total_loaded += 1

    # ── 3. Insert into graph ──────────────────────────────────────
    # Insert strong nodes first
    for node in strong_nodes:
        graph.insertNode(node, replace=True)

    # Insert weak nodes with parents
    for node in weak_nodes:
        if hasattr(node, "_parent") and node._parent is not None:
            graph.insertNode(node, insert_parent=True)

    # ── 4. Compute final stats from entity_map ────────────────────
    agent_labels = {"Agent", "CorporateBody", "Person", "Family"}
    stats["things"] = sum(1 for n in entity_map.values() if n.main_label == "Thing")
    stats["agents"] = sum(1 for n in entity_map.values() if n.main_label in agent_labels)
    stats["records"] = sum(1 for n in entity_map.values() if n.main_label == "RecordResource")
    stats["children"] = sum(1 for n in entity_map.values() if n.main_label not in {"Thing", *agent_labels, "RecordResource"})
    stats["total"] = stats["things"] + stats["agents"] + stats["records"] + stats["children"]

    return stats
