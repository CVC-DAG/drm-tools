"""Core data structures: Node, Relation, WeakNode, WeakRelation.

These classes represent the graph primitives used by both Neo4jGraph
and MockGraph.  Nodes carry a primary key (``pk``), a main label,
optional alternative labels, and optional parent relationships for
WeakNode hierarchies.  Relations connect two nodes with a typed edge.
"""

from typing import *

# TODO: Typing, qué retorna cada funció


def _single_pk(pk: Dict, version=5):
    if version == 3 and len(pk) > 1:
        return {"_".join(pk.keys()): "_".join([str(x) for x in pk.values()])}

    return pk


def _new_key(old_key, list_keys):
    n = 0
    while old_key + "_" + str(n) in list_keys:
        n += 1

    return old_key + "_" + str(n)


def _mergePK(pk_a, pk_b, version=5):
    k = set(pk_a.keys()).intersection(set(pk_b.keys()))

    for v in k:
        new_key = _new_key(v, set(pk_a.keys()).union(pk_b.keys()))
        pk_b[new_key] = pk_b.pop(v)

    pk = {**pk_a, **pk_b}

    return _single_pk(pk, version)


def _setNodePK(value):
    try:
        main_label = value.pop("main_label", None)
        pk = value.pop("pk", None)

        if main_label is None:
            raise Exception("Error")

        if pk is None:
            raise Exception("Error")
    except Exception:
        print("error")

    return {"main_label": main_label, "pk": pk}


# TODO: Cal modificar el codi per quan es posi src['pk'] retorni la pk en funció de la versió del Neo4j, on src és un node
class Node(object):
    """A graph node with a primary key, labels, and optional parent.

    Nodes are the fundamental building blocks of the DRM graph.  Each node
    has a ``main_label`` (the primary Cypher label), optional ``alternative_labels``,
    and a ``pk`` (primary key) that uniquely identifies it within its label.

    When a ``parent`` is provided the node becomes a **WeakNode**: its primary
    key is merged with the parent's key to form a composite key, and a typed
    edge is created when the node is inserted into a graph store.

    Args:
        pk: Primary key — an int is converted to ``{"id": pk}``, a dict is used
            as-is.  Must be provided unless ``neo4j_id`` is given.
        main_label: The primary label used in Cypher queries.
        alternative_labels: Additional labels attached to the node.
        version: Neo4j protocol version (default 5).
        neo4j_id: Internal Neo4j node ID (used when reconstructing a node
            from a database result).
        **kwargs: Arbitrary additional attributes stored on the node.
            Special kwargs: ``parent`` (Node), ``parent_relation`` (str),
            ``is_weak`` (bool), ``_propagate`` (bool), ``dependencies``.
    """

    def __init__(
        self,
        pk: Dict[str, Union[int, str]] = None,
        main_label: str = "",
        alternative_labels: Union[str, List[str]] = None,
        version: int = 5,
        neo4j_id: int | None = None,
        **kwargs: Any
    ):
        # Definim les propietats
        self._neo4j_id = neo4j_id
        self._version = version

        if pk is None:
            if neo4j_id is not None:
                # Node recuperat de la BD: PK sintètica basada en neo4j_id
                self._primary_key = {"id": neo4j_id}
            else:
                raise ValueError(
                    "Node must have either a primary key (pk) or a neo4j_id. "
                    "A node without either cannot be inserted or referenced."
                )
        elif isinstance(pk, int):
            self._primary_key = {"id": pk}
        elif isinstance(pk, Dict):
            self._primary_key = _single_pk(pk, version)
        else:
            raise TypeError(
                f"pk must be an int or dict, got {type(pk).__name__}"
            )

        self._main_label = main_label  # main_label.lower().capitalize()

        if isinstance(alternative_labels, str):
            self._label = [
                alternative_labels
            ]  # [alternative_labels.lower().capitalize()]
        else:
            self._label = (
                alternative_labels
                if alternative_labels is None
                else [x for x in alternative_labels]  # x.lower().capitalize()
            )

        self._is_weak = kwargs.pop("is_weak", False)
        self._propagate = kwargs.pop("_propagate", False)
        parent_relation = kwargs.pop("parent_relation", None)
        self._parent = kwargs.pop("parent", None)
        if self._parent is not None:
            assert isinstance(self._parent, Node), "parent must be a Node"
            self._is_weak = True
            self._primary_key = _mergePK(self._parent._primary_key, self._primary_key)
            self._parent_relation = (
                parent_relation if parent_relation is not None else "HAS"
            )

        dependencies = kwargs.pop("dependencies", False)
        if dependencies:
            self._dependencies = dependencies
        else:
            self._dependencies = None

        if kwargs is not None:
            for k in kwargs:
                self.__setattr__(k, kwargs[k])

    # def __str__(self):
    #    return "a:"+ ":".join(self.labels)

    def __repr__(self):
        main_label = ":" + self._main_label if len(self._main_label) > 0 else ""
        id = " <Id>: " + str(self._neo4j_id) if self._neo4j_id is not None else ""
        mess = "(a" + main_label + id + ")"
        mess += """, pk:""" + self._primary_key.__repr__()
        mess += (
            (", attributes:" + self.attributes[1].__repr__())
            if len(self.attributes[1]) > 0
            else ""
        )
        return mess

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value
        if value == 3:
            self._primary_key = _single_pk(self._primary_key, value)

    @property
    def attributes(self):
        at = self.__dict__.copy()
        # at.pop('_label',None)
        # at.pop('_main_label')
        # at.pop('_neo4j_id',None)
        # at.pop('_version')
        # at.pop('_parent')
        # at.pop('_is_weak')
        # at.pop('_parent_relation',None)
        # at.pop('_propagate', None)
        pk = at.pop("_primary_key",None)
        for x in list(at.keys()):
            if x[0] == "_":
                at.pop(x, None)


        return pk, at

    @property
    def labels(self):
        if self._label is None:
            return [self._main_label]
        else:
            return [self._main_label] + self._label

    @property
    def main_label(self):
        return self._main_label

    @property
    def neo4j_id(self):
        return self._neo4j_id

    @neo4j_id.setter
    def neo4j_id(self, value):
        self._neo4j_id = value

    def __getitem__(self, key):
        def get_pk():
            if hasattr(self,'_primary_key'):
                return self._primary_key
            if hasattr(self,'_neo4j_id'):
                return { 'neo4j_id': self._neo4j_id}

            return 0

        if key == "pk":
            return {"main_label": self._main_label, "pk": get_pk() }

        if key == "main_label":
            return self._main_label

        if key == "labels":
            if self._label is None:
                return [self._main_label]
            else:
                return [self._main_label] + self._label

        if key == "pk_attributes":
            return get_pk()

        attr = self.__dict__.copy()
        if key == "attributes":
            attr.pop("_label", None)
            attr.pop("_main_label")
            attr.pop("_neo4j_id", None)
            pk = attr.pop("_primary_key")

            return pk, attr

        if "_" + key in attr:
            return attr["_" + key]
        else:
            raise Exception(key + " is not a node attribute")

    def __setitem__(self, key, value):
        if key == "pk":
            aux = _setNodePK(value)
            self._main_label, self._pk = aux["_main_label"], aux["pk"]
            return

        if key == "main_label":
            self._main_label = value
            return

        if key == "labels":
            self._label = value
            return

        if key == "pk_attributes":
            if isinstance(value, dict):
                self._primary_key = value
            else:
                raise Exception("dictionary expected")

            return

        self.__setattr__(key, value)


# Class Relation denotes the relation of two nodes in the graph database
class Relation(object):
    """A typed edge connecting two nodes in the graph.

    Relations store the primary keys of their source and destination nodes
    and can carry arbitrary edge properties.

    Args:
        src: Source node. Its ``pk`` is extracted and stored.
        dst: Destination node. Its ``pk`` is extracted and stored.
        type: Relation type (e.g. "HAS_NOM", "CONNECTS"). Stored uppercase.
        **kwargs: Edge properties stored as attributes.
    """

    def __init__(self, src: Node, dst: Node, type: str, **kwargs: Any):
        """Initialize a Relation between two nodes."""
        # Definim les propietats
        self._type = type.upper()
        self._src = src["pk"]
        self._dst = dst["pk"]

        if kwargs is not None:
            for k in kwargs:
                self.__setattr__(k, kwargs[k])

    @property
    def src(self):
        return self._src["main_label"], self._src["pk"]

    @src.setter
    def src(self, value):
        self._src = _setNodePK(value)

    @property
    def dst(self):
        return self._dst["main_label"], self._dst["pk"]

    @dst.setter
    def dst(self, value):
        self._dst = _setNodePK(value)

    def __repr__(self):
        mess = (
            "src:" + str(self._src) + ", dst:" + str(self._dst) + " type:" + self._type
        )
        return mess

    def __getitem__(self, key):
        if key == "src":
            return {"main_label": self._src["main_label"], "pk": self._src["pk"]}

        if key == "dst":
            return {"main_label": self._dst["main_label"], "pk": self._dst["pk"]}

        if key == "type":
            return self._type

        attr = self.__dict__.copy()
        if key == "attributes":
            # remove private attributes
            attr.pop("_src", None)
            attr.pop("_dst", None)
            attr.pop("_type", None)

            if attr == {}:
                return None
            else:
                return attr

        if key in attr:
            return attr[key]
        else:
            raise Exception(key + " is not a relation attribute")

    def __setitem__(self, key, value):
        if key == "src":
            self._src = _setNodePK(value)
            return

        if key == "dst":
            self._dst = _setNodePK(value)
            return

        if key == "type":
            self._type = value
            return

        self.__setattr__(key, value)


class WeakNode(Node):
    def __init__(self, parent: Node, **kwargs: Any):
        kwargs.pop("is_weak", None)
        kwargs.pop("parent", None)
        super().__init__(is_weak=True, parent=parent, **kwargs)


class WeakRelation(Relation):
    def __init__(self, src: Node, dst: Node, type: str, **kwargs: Any):
        # kwargs.pop('propagate', True)
        super().__init__(
            src, dst, type, _propagate=kwargs.pop("propagate", True), **kwargs
        )
