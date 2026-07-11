"""Neo4jGraph — Full Neo4j driver integration layer for the DRM graph model.

Provides graph operations (insert, update, delete nodes and relations)
with FK validation, cascade delete, and WeakNode parent propagation.
"""

from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError, TransactionError
from . import Node, Relation, WeakRelation
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from tqdm import tqdm
import warnings


class Neo4jGraph:
    """Neo4j-backed graph store for the DRM document representation model.

    This class wraps the Neo4j Python driver and provides high-level
    operations for managing graph nodes and relations with foreign key
    validation, cascade delete strategies (CASCADE, RESTRICT, SET NULL),
    and WeakNode parent-child propagation.

    Example:
        >>> graph = Neo4jGraph(
        ...     url="bolt://localhost:7687",
        ...     user="neo4j",
        ...     password="secret",
        ...     database="mydb",
        ... )
        >>> doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
        >>> graph.insertNode(doc, replace=True)
        >>> graph.close()

    Args:
        url: Neo4j connection URL (e.g. ``bolt://localhost:7687``).
        user: Authentication username.
        password: Authentication password.
        database: Target database name. Defaults to the Neo4j default.
    """

    def __init__(
        self,
        url: str,
        user: str,
        password: str,
        database: Optional[str] = None,
    ) -> None:
        self._driver = GraphDatabase.driver(url, auth=(user, password))
        self._tx = None
        self._closed = False
        # Internal tracking: neo4j_id -> pk dict (for get_node_pks)
        self._node_pks: Dict[int, Dict[str, Any]] = {}
        if database is None:
            self._session = self._driver.session()
        else:
            self._session = self._driver.session(database=database)
        # self._version = list(list(self._session._pool.connections.values())[0])[
        #    0
        # ].PROTOCOL_VERSION[0]
        self._version = self._driver.get_server_info().protocol_version[0]
        # FK index: neo4j_id → set of (other_id, rel_type, direction)
        # direction: "out" = edge starts here, "in" = edge ends here
        self._fk_index: Dict[int, Set[Tuple[int, str, str]]] = {}

    # ------------------------------------------------------------------
    # Public API: CRUD operations
    # ------------------------------------------------------------------

    def insertNode(
        self,
        node: Node,
        insert_parent: bool = True,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> int:
        """Insert a node into the Neo4j database.

        For WeakNode instances, the parent node is inserted first if
        ``insert_parent=True``.  String dependencies (``dependencies``
        attribute) are automatically materialised as ``Valor`` nodes
        connected by typed edges.

        Args:
            node: The node to insert.
            insert_parent: If the node is a WeakNode, insert its parent
                first. Defaults to True.
            update: If True, MERGE the node and update attributes without
                deleting it. Use when adding new attributes to an existing
                node. Defaults to False.
            replace: If True and the node already exists, delete it
                (with detach) and create a fresh one. The caller must
                recreate relations. Defaults to False.

        Returns:
            The Neo4j internal node id of the inserted node.
        """

        has_parent = insert_parent if node["is_weak"] else False
        has_dependencies = True if node["dependencies"] else False

        # Allow recursion on parent node insertion but without replacing "parent nodes" if already exists
        inici = False

        # self._session.write_transaction(self._create_constraint, node.main_label, list(node['pk']['pk'].keys()))
        if self._tx is None:
            self._tx = self._session.begin_transaction()
            inici = True

        try:
            if has_parent:
                self.insertNode(
                    node["parent"],
                    insert_parent=insert_parent,
                    update=True,
                    replace=False,
                )

            id = self._insertNode(node, update=update, replace=replace)

            if has_dependencies:
                deps = node["dependencies"]
                for k in deps.keys():
                    v = deps[k]
                    id_v = self._insertNode(v,update=True, replace=False)
                    rel = Relation(node, deps[k], k.upper())
                    self.insertRelation(rel, update=True)
                    # print(k,deps[k])

            if inici:
                # print(node)
                self._tx.commit()
        except ConstraintError as err:
            try:
                self._tx.rollback()
            except Exception:
                pass
            try:
                self._tx.close()
            except Exception:
                pass
            self._tx = None
            raise RuntimeError("Duplicate key: " + err.message) from err
        except TransactionError as err:
            msg = str(err)
            if "Duplicate key" in msg or "NODE KEY" in msg or "Transaction failed" in msg or "ConstraintValidationFailed" in msg:
                try:
                    self._tx.rollback()
                except Exception:
                    pass
                try:
                    self._tx.close()
                except Exception:
                    pass
                self._tx = None
                raise RuntimeError("Duplicate key: " + msg) from err
            print(err)
            try:
                self._tx.rollback()
            except Exception:
                pass
            try:
                self._tx.close()
            except Exception:
                pass
            self._tx = None
            raise
        finally:
            if inici and self._tx is not None:
                try:
                    self._tx.close()
                except Exception:
                    pass
                self._tx = None
        return id  # only reached if no exception was raised above

    def deleteNode(
        self,
        node: Node,
        propagation: bool = False,
        detach: bool = False,
        on_delete: str = "cascade",
    ) -> bool:
        """Delete a node and optionally its connected subgraph.

        Handles ON DELETE strategies, WeakNode cascade propagation,
        and FK index cleanup.

        Args:
            node: The node to delete.
            propagation: If True, recursively delete child nodes linked
                via edges with ``_propagate=TRUE`` (used by WeakNode).
            detach: If True, use Neo4j ``DETACH DELETE`` to remove
                the node and all connected edges.
            on_delete: Deletion strategy — ``"cascade"`` (default),
                ``"restrict"``, or ``"set_null"``.

        Returns:
            True if the node was deleted, False if deletion was refused
            (e.g. RESTRICT with existing edges) or the node was not found.
        """
        node.version = self._version

        inici = False

        if self._tx is None:
            self._tx = self._session.begin_transaction()
            inici = True

        try:
            if propagation:
                # Get the list of nodes to be deleted before
                nodeList = self._get_propagated_nodes(self._tx, node)
                for child in nodeList:
                    self.deleteNode(
                        Node(
                            neo4j_id=child[0]._id,
                            alternative_labels=list(child[0]._labels),
                            **child[0]._properties,
                        ),
                        propagation=propagation,
                        detach=True,
                    )
                # After deleting children, remove any remaining outgoing edges
                if node.neo4j_id is not None:
                    self._tx.run(
                        "MATCH (a)-[r]->(b) WHERE id(a)="
                        + str(node.neo4j_id) + " DELETE r"
                    )

            if on_delete == "set_null":
                # ON DELETE SET NULL: delete node, remove edges, keep neighbors
                if node.neo4j_id is not None:
                    self._remove_from_fk_index(node.neo4j_id)
                    # Remove all edges before the node (Neo4j won't allow deleting
                    # a node that still has relationships with a plain DELETE)
                    self._tx.run(
                        "MATCH (a) WHERE id(a) = "
                        + str(node.neo4j_id)
                        + " DETACH DELETE a"
                    )
                    res = True
                else:
                    res = False
            elif detach:
                # ON DELETE CASCADE: recursively delete connected nodes first
                if node.neo4j_id is not None:
                    self._cascade_delete(self._tx, node)
                    self._remove_from_fk_index(node.neo4j_id)
                res = self._delete_node(self._tx, node, detach=detach)
            else:
                # ON DELETE RESTRICT: check if node has children (WeakNode) before deleting
                # propagation=False means we refuse to delete if the node has children
                if propagation is False and node.neo4j_id is not None:
                    children = self._get_propagated_nodes(self._tx, node)
                    if children:
                        raise RuntimeError(
                            "ON DELETE RESTRICT: node has child WeakNode(s) — "
                            "use propagation=True or detach=True to delete."
                        )
                # Also check for any edges (FK violations) — refuse to delete
                if not self._has_no_edges(self._tx, node):
                    raise RuntimeError(
                        "ON DELETE RESTRICT: node has connected edges — "
                        "use detach=True or delete edges first."
                    )
                # Clean FK index before regular delete
                if node.neo4j_id is not None:
                    self._remove_from_fk_index(node.neo4j_id)
                res = self._delete_node(self._tx, node, detach=False)
        except ConstraintError as err:
            print(f"[XPP Message]: {err.message}")
            return False
        except TransactionError as err:
            msg = str(err)
            if "Duplicate key" in msg or "NODE KEY" in msg or "Transaction failed" in msg or "ConstraintValidationFailed" in msg:
                try:
                    self._tx.rollback()
                except Exception:
                    pass
                try:
                    self._tx.close()
                except Exception:
                    pass
                raise RuntimeError("Duplicate key: " + msg) from err
            print(err)
            self._tx.rollback()
            self._tx.close()
            raise
        else:
            if inici:
                self._tx.commit()
                self._tx.close()
                self._tx = None
            return res
        finally:
            # Ensure transaction is closed even on early return (e.g. RESTRICT).
            # Only close if we opened it (inici=True); recursive calls must not
            # close the parent transaction.
            if inici and self._tx is not None:
                if not self._tx.closed():
                    self._tx.rollback()
                self._tx.close()
                self._tx = None

    def checkNode(self, node: Node, **kwargs: Any) -> Optional[int]:
        """Check if a node exists in the database.

        Looks up the node by its ``neo4j_id`` if set, otherwise searches
        by ``main_label`` and primary key.

        Args:
            node: The node to look up.

        Returns:
            The Neo4j internal node id if found, None otherwise.
        """
        inici = False
        if node is not None:
            # If neo4j_id is already known, return it directly
            if node.neo4j_id is not None:
                return node.neo4j_id
            if self._tx is None:
                self._tx = self._session.begin_transaction()
                inici = True
            try:
                # return self._session.read_transaction(self._check_node, node['main_label'], node['pk_attributes'])
                res = self._check_node(
                    self._tx, node["main_label"], node["pk_attributes"]
                )
            except TransactionError as err:
                print(err)
                self._tx.rollback()
                self._tx.close()
                self._tx = None
                raise
            else:
                if inici:
                    self._tx.commit()
                    self._tx.close()
                    self._tx = None

                return res
            finally:
                if inici and self._tx is not None:
                    if not self._tx.closed():
                        self._tx.rollback()
                    self._tx.close()
                    self._tx = None
        else:
            return False

    def insertRelation(
        self,
        rel: Relation,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> int:
        """Insert a directed relation (edge) between two nodes.

        Validates that both source and destination nodes exist before
        creating the edge (FK constraint).

        Args:
            rel: The relation to insert, containing source node,
                destination node, and relation type.
            update: If True, MERGE the relation and update attributes
                without deleting it. Defaults to False.
            replace: If True and the relation already exists, delete it
                and create a fresh one. Defaults to False.

        Returns:
            The Neo4j internal relation id of the inserted relation.

        Raises:
            RuntimeError: If the source or destination node does not exist
                in the database (FK violation).
        """
        inici = False

        if self._tx is None:
            self._tx = self._session.begin_transaction()
            inici = True

        try:
            # FK validation: both endpoints must exist before creating the edge
            src_exists = self._validate_fk(self._tx, rel["src"], "src")
            dst_exists = self._validate_fk(self._tx, rel["dst"], "dst")
            if not src_exists:
                raise RuntimeError(
                    f"FK violation: src node with pk={rel['src'].get('pk')} "
                    f"and main_label={rel['src'].get('main_label')} does not exist."
                )
            if not dst_exists:
                raise RuntimeError(
                    f"FK violation: dst node with pk={rel['dst'].get('pk')} "
                    f"and main_label={rel['dst'].get('main_label')} does not exist."
                )
            if update:
                # return self._session.write_transaction(self._update_relation,rel )
                id = self._update_relation(self._tx, rel)
                # Update FK index after upsert
                self._update_fk_index_for_relation(self._tx, rel)
            else:
                # id = self._session.read_transaction(self._check_relation, rel['src'],rel['dst'],rel['type'])
                id = self._check_relation(self._tx, rel["src"], rel["dst"], rel["type"])
                if isinstance(id, int) and not isinstance(id, bool):
                    if replace:
                        # Remove old FK index entries before deleting
                        self._remove_from_fk_index_for_relation(self._tx, rel)
                        # self._session.write_transaction(self._delete_relation,rel)
                        self._delete_relation(self._tx, rel)
                # return self._session.write_transaction(self._create_relation,rel )
                id = self._create_relation(self._tx, rel)
                # Add FK index entries after create
                self._update_fk_index_for_relation(self._tx, rel)
        except ConstraintError as err:
            print("[XPP Message]: " + err.message)
            raise
        except TransactionError as err:
            print(err)
            self._tx.rollback()
            self._tx.close()
            self._tx = None
            raise
        else:
            if inici:
                self._tx.commit()
                self._tx.close()
                self._tx = None

            return id
        finally:
            if inici and self._tx is not None:
                if not self._tx.closed():
                    self._tx.rollback()
                self._tx.close()
                self._tx = None

    def create(
        self,
        migration: Tuple[List[Node], List[Relation]],
        update: bool = False,
        replace: bool = False,
    ) -> None:
        """Bulk import nodes and relations from a migration plan.

        Iterates over the node and relation lists, inserting each with
        a progress bar.  Uses ``insertNode`` and ``insertRelation``
        internally.

        Args:
            migration: A tuple ``(node_list, relation_list)`` where each
                list contains ``Node`` or ``Relation`` instances.
            update: Passed to ``insertNode`` / ``insertRelation``.
            replace: Passed to ``insertNode`` / ``insertRelation``.
        """
        NodeInformation, RelationInformation = migration
        if len(NodeInformation) > 0:
            for node in tqdm(NodeInformation, desc="Importing nodes"):
                id = self.insertNode(node, update=update, replace=replace)

        if len(RelationInformation) > 0:
            for relation in tqdm(RelationInformation, desc="Creating node links"):
                self.insertRelation(relation, update=update, replace=replace)

    # ------------------------------------------------------------------
    # Public API: query operations
    # ------------------------------------------------------------------

    def get_node_ids(self) -> List[int]:
        """Return all internal node ids in the graph."""
        if self._closed:
            return []
        result = self._session.run("MATCH (n) RETURN id(n) AS nid")
        return [record["nid"] for record in result]

    def get_nodes(self) -> List[int]:
        """Alias for :meth:`get_node_ids` for backward compatibility."""
        return self.get_node_ids()

    def get_node_pks(self) -> List[Dict[str, Any]]:
        """Return all primary keys of nodes in the graph."""
        result = []
        for nid, pk in self._node_pks.items():
            r = self._session.run(
                "MATCH (n) WHERE id(n) = $nid RETURN labels(n)[0] AS label",
                nid=nid
            ).single()
            label = r["label"] if r else ""
            result.append({"main_label": label, "pk": pk})
        return result

    def get_edges(self) -> List[Tuple[int, int, str]]:
        """Return all edges as ``(src_id, dst_id, rel_type)`` tuples."""
        result = self._session.run(
            "MATCH (a)-[r]->(b) RETURN id(a) AS src, id(b) AS dst, type(r) AS rel_type"
        )
        return [
            (record["src"], record["dst"], record["rel_type"])
            for record in result
        ]

    def get_edge_attrs(self, u: int, v: int, key: str) -> Optional[Dict[str, Any]]:
        """Return attributes stored for an edge."""
        result = self._session.run(
            "MATCH (a)-[r:" + key + "]->(b) "
            "WHERE id(a) = $src AND id(b) = $dst "
            "RETURN r",
            src=u, dst=v
        )
        single = result.single()
        if single is None:
            return None
        return dict(single["r"])

    # ------------------------------------------------------------------
    # Public API: lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        if self._tx is not None:
            if not self._tx.closed():
                self._tx.close()
            self._tx = None
        self._closed = True
        self._fk_index.clear()
        self._driver.close()

    def enable_vector_index(
        self, name: str, dimensions: int, space: str = "cosine", **kwargs
    ) -> None:
        """Neo4j backend does not support vector indexes."""
        raise NotImplementedError(
            "Vector indexes are not supported by Neo4jGraph. "
            "Use NetworkXGraph for vector search."
        )

    def query_vector_index(
        self, name: str, vector: List[float], top_k: int = 5
    ) -> List[int]:
        """Neo4j backend does not support vector queries."""
        raise NotImplementedError(
            "Vector queries are not supported by Neo4jGraph. "
            "Use NetworkXGraph for vector search."
        )

    # ------------------------------------------------------------------
    # Protected helpers: node operations
    # ------------------------------------------------------------------

    def _insertNode(
        self,
        node: Node,
        update: bool = False,
        replace: bool = False,
    ) -> int:
        node.version = self._version

        # check if node is weak if so, check if  its  parent node is already inserted. If no, raise an exception and cancel the transaction
        # try:
        if node["is_weak"]:
            if not self.checkNode(node["parent"]):
                raise Exception(
                    "ADGT Exception: missing parent node  "
                    + str(node["parent"])
                    + ". Insert it before "
                    + str(node)
                    + ". Node is weak:"
                    + str(node["is_weak"])
                    + ". Parent relation:"
                    + str(node["parent_relation"])
                )

        # pk, attributes = node.attributes
        # Check if node already exists
        _trasa = ""
        try:
            # Add constraints

            # self._create_constraint(self._tx, node.main_label, list(pk.keys()))
            # self._session.write_transaction(self._create_constraint, node.main_label, list(pk.keys()))

            if update:
                # id = self._session.write_transaction(self._update_node, node)
                # print("update node")
                id = self._update_node(self._tx, node)
                _trasa += "(1) Actualitza el node "
            else:
                id = self.checkNode(node)
                if isinstance(id, int) and not isinstance(id, bool):
                    if replace:
                        # ON UPDATE CASCADE: in Neo4j, edges reference nodes
                        # by internal ID which never changes.  replace=True
                        # deletes the node (with detach, cascading edges) and
                        # creates a fresh one — the caller must recreate
                        # relations if needed.
                        self.deleteNode(node, detach=True, propagation=True)
                        _trasa += "(1) esborra el node "
                # id = self._session.write_transaction(self._create_node, node)
                # print("create node")
                id = self._create_node(self._tx, node)
                _trasa += "(2) crea  el node "

            node["neo4j_id"] = id

            # Si el node tenia pk=None explícit, assignem l'ID generat com a PK
            if node._primary_key is None:
                node._primary_key = {"id": id}

            # Track neo4j_id -> pk mapping for get_node_pks()
            if node._primary_key is not None:
                self._node_pks[id] = dict(node._primary_key)

            # if is a weak entity the edge linking the parent node must be created
            if node["is_weak"]:
                # print("node", node.main_label, node.neo4j_id, "is weak")
                for ppk in node["parent"]["pk"]["pk"]:
                    if not node["parent"]["pk"]["pk"][ppk] == node["pk"]["pk"][ppk]:
                        raise RuntimeError(
                            "ADGT Exception: Integrity Constraint Violated. Child node keys does not reference proper parent keys"
                        )

                self.insertRelation(
                    WeakRelation(
                        node["parent"],
                        node,
                        node["parent_relation"],
                        propagate=True,
                    ),
                    update=True,
                    replace=False,
                )

        except ConstraintError as err:
            warnings.warn(f"[XPP Message]: {err.message}")
            id = self.checkNode(node)
            return id
            # raise RuntimeError("ADGT Exception: " + err.message + " " + _trasa) from err

        return id

    def _resolve_neo4j_id(
        self,
        tx: Any,
        node_data: Dict[str, Any],
    ) -> Optional[int]:
        """Look up the Neo4j internal id for a node by its label and primary key."""
        pk = node_data.get("pk")
        label = node_data.get("main_label")
        if pk is None or label is None:
            return None
        result = tx.run(
            "MATCH (n:"
            + label
            + ") WHERE "
            + _generate_where_cond("n", pk)
            + " RETURN id(n) AS nid"
        ).single()
        return result["nid"] if result else None

    # ------------------------------------------------------------------
    # Protected helpers: FK index operations
    # ------------------------------------------------------------------

    def _add_to_fk_index(
        self, src_id: int, dst_id: int, rel_type: str
    ) -> None:
        """Add a relation to the FK index."""
        self._fk_index.setdefault(src_id, set()).add((dst_id, rel_type, "out"))
        self._fk_index.setdefault(dst_id, set()).add((src_id, rel_type, "in"))

    def _remove_from_fk_index(self, node_id: int) -> None:
        """Remove all FK index entries for a given node."""
        self._fk_index.pop(node_id, None)
        for other_id in list(self._fk_index):
            self._fk_index[other_id] = {
                entry for entry in self._fk_index[other_id] if entry[0] != node_id
            }
            if not self._fk_index[other_id]:
                del self._fk_index[other_id]

    def _cascade_delete(self, tx: Any, node: Node) -> None:
        """ON DELETE CASCADE: delete all edges connected to the node.

        Uses the FK index to find all edges connected to the node and removes them.
        Neighbor nodes are left as standalone entities.
        """
        node_id = node.neo4j_id
        if node_id is None:
            return

        # Find all connected nodes via the FK index
        entries = self._fk_index.get(node_id, set()).copy()
        for neighbor_id, rel_type, direction in entries:
            # Delete the edge
            if direction == "out":
                edge_query = (
                    "MATCH (a)-[r:" + rel_type + "]->(b) "
                    "WHERE id(a) = " + str(node_id) + " AND id(b) = " + str(neighbor_id)
                    + " DELETE r"
                )
            else:
                edge_query = (
                    "MATCH (a)-[r:" + rel_type + "]->(b) "
                    "WHERE id(b) = " + str(node_id) + " AND id(a) = " + str(neighbor_id)
                    + " DELETE r"
                )
            tx.run(edge_query)

            # Clean FK index for neighbor
            if neighbor_id in self._fk_index:
                self._fk_index[neighbor_id] = {
                    e for e in self._fk_index[neighbor_id]
                    if e != (node_id, rel_type, "in" if direction == "out" else "out")
                }
                if not self._fk_index[neighbor_id]:
                    del self._fk_index[neighbor_id]
        self._fk_index.pop(node_id, None)

    def _remove_from_fk_index_for_relation(
        self, tx: Any, rel: Relation
    ) -> None:
        """Remove FK index entries for a specific relation."""
        src_id = self._resolve_neo4j_id(tx, rel["src"])
        dst_id = self._resolve_neo4j_id(tx, rel["dst"])
        rel_type = rel["type"]
        if src_id is not None:
            self._fk_index[src_id] = {
                entry for entry in self._fk_index.get(src_id, set())
                if entry != (dst_id, rel_type, "out")
            }
            if not self._fk_index[src_id]:
                del self._fk_index[src_id]
        if dst_id is not None:
            self._fk_index[dst_id] = {
                entry for entry in self._fk_index.get(dst_id, set())
                if entry != (src_id, rel_type, "in")
            }
            if not self._fk_index[dst_id]:
                del self._fk_index[dst_id]

    def _update_fk_index_for_relation(
        self, tx: Any, rel: Relation
    ) -> None:
        """Look up node IDs and add the relation to the FK index."""
        src_id = self._resolve_neo4j_id(tx, rel["src"])
        dst_id = self._resolve_neo4j_id(tx, rel["dst"])
        if src_id is not None:
            self._add_to_fk_index(src_id, dst_id or 0, rel["type"])
        if dst_id is not None:
            self._add_to_fk_index(src_id or 0, dst_id, rel["type"])

    # ------------------------------------------------------------------
    # Static helpers: node operations
    # ------------------------------------------------------------------

    @staticmethod
    def _create_node(tx: Any, node: Node) -> Optional[int]:
        pk, attributes = node.attributes
        props = attributes if pk is None else {**pk, **attributes}

        labels = "" if node.labels == "" else ":" + ":".join(node.labels)

        try:
            result = tx.run(
                "CREATE (a" + labels + ") SET a = $prop_dict RETURN id(a) AS id",
                prop_dict=props,
            ).value("id")[0]
            return result
        except ConstraintError as err:
            print("[ADGT Message]: " + err.message)
            print("node already inserted")
            return None

    @staticmethod
    def _update_node(tx: Any, node: Node) -> int:
        pk, attributes = node.attributes
        # print("(_update_node) pk:", pk)
        # print("(_update_node) attributes:", attributes)

        main_label = "" if node.main_label == "" else ":" + node.main_label
        labels = "" if node.labels == "" else ":" + ":".join(node.labels)

        try:
            query = (
                "MERGE (a"
                + main_label
                + " { "
                + _generate_where_cond("a", pk, type="merge")
                + " })"
            )
        except:
            pass
        # TODO: Fix lines below
        # if labels != '':
        #    query += " SET a" + labels + " "

        a = {**pk, **attributes} if len(attributes) > 0 else pk
        # print("(_update_node) a:", a)
        query += (
            " ON CREATE SET a"
            + labels
            + ", a = $prop_dict"
            + " ON MATCH SET a"
            + labels
            + ", a += $prop_dict"
            + " RETURN id(a) AS id"
        )
        # print("(_update_node) query:", query, "a:", a)
        try:
            result = tx.run(query, prop_dict=a).value("id")[0]
        except Exception as err:
            print(query)
            print(a)
            raise
        # print("(_update_node) result:", result)
        return result

    @staticmethod
    def _delete_node(tx: Any, node: Node, detach: bool = False) -> bool:
        neo4j_id = node.neo4j_id
        detach_text = " detach " if detach else ""
        if neo4j_id is None:
            pk, attributes = node.attributes
            main_label = "" if node.main_label == "" else ":" + node.main_label

            query = (
                "MATCH (a"
                + main_label
                + ") WHERE "
                + _generate_where_cond("a", pk)
                + " "
                + detach_text
                + "DELETE a"
            )
        else:
            query = (
                "MATCH (a) WHERE id(a) = " + str(neo4j_id) + " " + detach_text + "DELETE a"
            )

        result = tx.run(query).values()
        return result == []

    @staticmethod
    def _check_node(
        tx: Any, main_label: str, id: Dict[str, str]
    ) -> Optional[int]:
        if id is None:
            return None

        try:
            idnode = tx.run(
                "MATCH (a:"
                + main_label
                + ") WHERE "
                + _generate_where_cond("a", id)
                + " RETURN id(a)"
            ).single()
        except:
            return None

        if idnode is not None:
            return idnode.value()

        return None

    @staticmethod
    def _check_node_by_id(
        tx: Any, main_label: str, node_id: int
    ) -> Optional[int]:
        try:
            idnode = tx.run(
                "MATCH (a:"
                + main_label
                + ") WHERE id(a) = $nid RETURN id(a)",
                nid=node_id,
            ).single()
        except Exception:
            return None

        if idnode is not None:
            return idnode.value()

        return None

    # ------------------------------------------------------------------
    # Static helpers: relation operations
    # ------------------------------------------------------------------

    @staticmethod
    def _create_relation(tx: Any, rel: Relation) -> int:
        rel_type = rel["type"]
        src = rel["src"]
        dst = rel["dst"]

        attributes = rel["attributes"]

        query = (
            "MATCH (a:"
            + src["main_label"]
            + ") WHERE "
            + _generate_where_cond("a", src["pk"])
            + "MATCH (b:"
            + dst["main_label"]
            + ") WHERE  "
            + _generate_where_cond("b", dst["pk"])
            + "CREATE (a)-[r:"
            + rel_type
            + "]->(b)"
        )

        if attributes is not None:
            result = tx.run(
                query + " SET r = $prop_dict RETURN id(r) AS id",
                prop_dict=attributes,
            ).value("id")[0]
        else:
            try:
                result = tx.run(query + " RETURN id(r) AS id").value("id")[0]
            except Exception as err:
                a = tx.run("PROFILE " + query + " return id(r) as id")
                print(a.consume().profile["args"]["string-representation"])
                print(type(a))
                print(err)
                print(query)
                print(src)
                print(dst)
                print(rel_type)
                raise

        return result

    @staticmethod
    def _update_relation(tx: Any, rel: Relation) -> int:
        src, dst, type = rel["src"], rel["dst"], rel["type"]
        attributes = rel["attributes"]

        query = (
            "MATCH (a:"
            + src["main_label"]
            + " {"
            + _generate_where_cond("a", src["pk"], type="merge")
            + " }) "
            + "MERGE (b:"
            + dst["main_label"]
            + " {"
            + _generate_where_cond("b", dst["pk"], type="merge")
            + " }) "
            "MERGE (a)-[r:" + type + "]-> (b)"
        )
        if attributes:
            try:
                result = tx.run(
                    query
                    + " ON CREATE SET r += $prop_dict"
                    + " ON MATCH SET r += $prop_dict"
                    + " RETURN id(r) AS id",
                    prop_dict=attributes,
                ).value("id")[0]
            except Exception as err:
                print(err)
                print(query)
                print(attributes)
                print(src)
                print(dst)
                print(type)
                raise
        else:
            try:
                result = tx.run(query + " RETURN id(r) AS id").value("id")[0]
            except Exception as err:
                print(err)
                print(query)
                print(src)
                print(dst)
                print(type)
                raise

        return result

    @staticmethod
    def _delete_relation(tx: Any, rel: Relation) -> Optional[bool]:
        src, dst, type = rel["src"], rel["dst"], rel["type"]

        query = (
            "MATCH (a:"
            + src["main_label"]
            + " {"
            + _generate_where_cond("a", src["pk"], type="merge")
            + " })"
            + "-[r:"
            + type
            + "]->"
            + "(b:"
            + dst["main_label"]
            + " {"
            + _generate_where_cond("b", dst["pk"], type="merge")
            + " })"
            + "DELETE r"
        )

        result = tx.run(query).single()
        if result is None:
            return False
        else:
            return result.value()

    @staticmethod
    def _check_relation(
        tx: Any,
        src: Dict[str, Union[str, int, Dict[str, Union[str, int]]]],
        dst: Dict[str, Union[str, int, Dict[str, Union[str, int]]]],
        rel_type: str = "None",
    ) -> Optional[int]:
        if src.get("pk") is None:
            return None

        if dst.get("pk") is None:
            return None

        # TODO: Cal revisar que passa quan pk es ne4jid
        query = (
            "MATCH (a:"
            + src["main_label"]
            + ")-[r:"
            + rel_type
            + "]->(b:"
            + dst["main_label"]
            + ") "
            + "MATCH (a:"
            + src["main_label"]
            + ") WHERE "
            + _generate_where_cond("a", src["pk"])
            + "MATCH (b:"
            + dst["main_label"]
            + ") WHERE  "
            + _generate_where_cond("b", dst["pk"])
            + "RETURN id(r) AS id"
        )

        idnode = tx.run(query).single()

        if idnode is not None:
            return idnode.value("id")

        return None

    @staticmethod
    def _check_relation_by_id(
        tx: Any,
        src: Dict[str, Union[str, int, Dict[str, Union[str, int]]]],
        dst: Dict[str, Union[str, int, Dict[str, Union[str, int]]]],
        rel_type: str = "None",
    ) -> Optional[int]:
        if src.get("pk") is None:
            return None

        if dst.get("pk") is None:
            return None

        # TODO: Cal revisar que passa quan pk es ne4jid
        query = (
            "MATCH (a:"
            + src["main_label"]
            + ")-[r:"
            + rel_type
            + "]->(b:"
            + dst["main_label"]
            + ") "
            + "MATCH (a:"
            + src["main_label"]
            + ") WHERE "
            + _generate_where_cond("a", src["pk"])
            + "MATCH (b:"
            + dst["main_label"]
            + ") WHERE  "
            + _generate_where_cond("b", dst["pk"])
            + "RETURN id(r) AS id"
        )

        idnode = tx.run(query).single()

        if idnode is not None:
            return idnode.value("id")

        return None

    # ------------------------------------------------------------------
    # Static helpers: constraint / query helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_fk(
        tx: Any,
        node_data: Dict[str, Any],
        label: str,
    ) -> bool:
        """Verify that a node referenced by a relation exists in the database.

        This enforces foreign-key consistency: a relation can only connect
        nodes that already exist.  Mirrors the relational constraint
        ``ON DELETE RESTRICT`` / ``ON UPDATE CASCADE`` for graph edges.

        Returns True if the node exists, False otherwise.
        """
        if node_data.get("pk") is None:
            return False
        if node_data.get("main_label") is None:
            return False
        return tx.run(
            "MATCH (n:"
            + node_data["main_label"]
            + ") WHERE "
            + _generate_where_cond("n", node_data["pk"])
            + " RETURN count(n) > 0 AS found"
        ).single()["found"]

    @staticmethod
    def _create_constraint(tx: Any, main_label: str, id: List[str]) -> None:
        # Check whether an index (unique) exists for each node label. If not, it creates one to ensure unicity
        try:
            fields = ".".join([f"c.{f}" for f in id])
            query = (
                "CREATE CONSTRAINT " + main_label + "_PK IF NOT EXISTS "
                "FOR (c:" + main_label + ") REQUIRE c." + fields + " IS NODE KEY"
            )

            result = tx.run(query)
        except ConstraintError as err:
            print("[ADGT Message]: " + err.message)
            pass

    @staticmethod
    def _has_no_edges(tx: Any, node: Node) -> bool:
        """Check if a node has no connected edges (for ON DELETE RESTRICT)."""
        neo4j_id = node.neo4j_id
        if neo4j_id is not None:
            query = (
                "MATCH (n) WHERE id(n) = "
                + str(neo4j_id)
                + " OPTIONAL MATCH (n)-[x]-() RETURN count(x) = 0 AS has_no_edges"
            )
        else:
            main_label = "" if node.main_label == "" else ":" + node.main_label
            query = (
                "MATCH (a"
                + main_label
                + ") WHERE "
                + _generate_where_cond("a", node["pk"])
                + " OPTIONAL MATCH (a)-[x]-() RETURN count(x) = 0 AS has_no_edges"
            )
        return tx.run(query).single()["has_no_edges"]

    @staticmethod
    def _get_propagated_nodes(tx: Any, node: Node) -> List[Any]:
        """Get child nodes that should be deleted when this node is deleted.

        Matches edges where r._propagate=TRUE (set on WeakNode relations).
        """
        neo4j_id = node.neo4j_id
        if neo4j_id is None:
            main_label = "" if node.main_label == "" else ":" + node.main_label
            query = (
                "MATCH (a"
                + main_label
                + ")-[r]->(b) WHERE r._propagate=TRUE AND "
                + _generate_where_cond("a", node["pk_attributes"])
                + " RETURN b"
            )
        else:
            query = (
                "MATCH (n)-[r]->(b) WHERE id(n)="
                + str(neo4j_id)
                + " AND r._propagate=TRUE RETURN b"
            )
        return tx.run(query).values()


def _generate_tuple(node_name, pk, with_values=False):
    if with_values:
        return (
            " (" + ",".join([node_name + ".{}={}".format(k, pk[k]) for k in pk]) + ") "
        )
    else:
        return " (" + ",".join([node_name + ".{}".format(k) for k in pk]) + ") "


def _generate_where_cond(node_name, pk, type="where"):
    valor = [pk[a] for a in pk.keys() if a == 'neo4j_id']
    valor = valor[0] if len(valor) > 0 else None

    if valor is not None and len(pk) == 1:
        pk = { 'id('+node_name+')' : valor}

    if type.lower() == "where":
        conj, equal = " AND ", "="
        node_name += "."
    if type.lower() == "merge":
        conj, equal = " , ", " : "
        node_name = ""

    return (
        " "
        + conj.join(
            [
                node_name
                + "{}{}{}".format(
                    k, equal, pk[k] if isinstance(pk[k], int) else '"' + pk[k] + '"'
                )
                for k in pk
            ]
        )
        + " "
    )
