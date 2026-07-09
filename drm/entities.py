"""Semantic entity definitions for the DRM graph model.

This module defines domain-specific node types (IndividuPadro, LlocPadro,
Fotografia, etc.) that extend the base Node class with validation,
default labels, and relationship configuration.
"""

from typing import Any, Dict, Iterable, Tuple

from .base import Node, Relation, WeakNode


def assert_on_properties(
    args: Dict,
    properties: Iterable,
    entity: object,
    accepted_types: tuple = (
        str,
        int,
        dict,
        bool,
    ),
) -> Tuple[bool, str]:
    """Precondition on node insertion: asserts if a specified property isn't an instance.

    Args:
        args: dict of arguments for a certain entity.
        properties: iterable with properties to be asserted.
        entity: entity we are checking out.
        accepted_types: tuple of accepted types as property of object
            type Node or Relation. Non-hashable types are rejected.

    Returns:
        A tuple (success: bool, message: str). On success, message is "OKAY".
        On failure, message describes the missing property.
    """
    for prop in properties:
        if prop not in args or not isinstance(args[prop], accepted_types):
            return (
                False,
                f"AssertionError: Node type {type(entity).__name__} must receive "
                f"{prop}, therefore hasn't been added.",
            )
    return (True, "OKAY")


def _build_alternative_labels(al, suffix: str):
    """Append a suffix label to an alternative_labels value.

    Args:
        al: existing alternative labels (list, str, or None).
        suffix: label to append (e.g. "Individu", "Lloc").

    Returns:
        A list of alternative labels with the suffix appended.
    """
    if al is not None:
        if isinstance(al, list):
            return [*al, suffix]
        if isinstance(al, str):
            return [al, suffix]
    return [suffix]


# =================== Nodes =======================


# ========= Semantic Nodes =============
class IndividuPadro(Node):
    """A person entity with a name attribute.

    Extends Node with mandatory ``pk`` and ``nom`` properties.
    The ``nom`` and ``cognom`` attributes are automatically
    materialised as ``Valor`` nodes connected by typed edges.

    Args:
        pk: Primary key.
        nom: Person's first name (creates a Valor node).
        cognom1: First surname (creates a Valor node).
        cognom2: Second surname (creates a Valor node).
        alternative_labels: Additional labels (appends "Individu").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk", "nom")
    be_value_properties = ("nom", "cognom1", "cognom2")

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize an IndividuPadro node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, nom, cognom1, cognom2,
                alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "Individu")
        else:
            al = ["Individu"]

        if precondition or ignore_assertion:
            deps = {}
            for r in self.be_value_properties:
                valor = kwargs.pop(r, None)
                if valor is not None:
                    deps[r] = Atribut(valor)
            Node.__init__(
                self,
                main_label="IndividuPadro",
                pk=pk,
                alternative_labels=al,
                dependencies=deps,
                **kwargs,
            )
        else:
            print(message)
            exit()


class IndividuFoto(Node):
    """A person entity linked to a photograph.

    Extends Node with mandatory ``pk`` property.
    The ``alternative_labels`` automatically appends "Individu".

    Args:
        pk: Primary key.
        alternative_labels: Additional labels (appends "Individu").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize an IndividuFoto node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "Individu")
        else:
            al = ["Individu"]

        if precondition or ignore_assertion:
            deps = {}
            for r in self.be_value_properties:
                valor = kwargs.pop(r, None)
                if valor is not None:
                    deps[r] = Atribut(valor)
            Node.__init__(
                self,
                main_label="IndividuFoto",
                pk=pk,
                alternative_labels=al,
                dependencies=deps,
                **kwargs,
            )
        else:
            print(message)
            exit()


class EntitatAmbNom(Node):
    """A named entity with a ``nom`` property.

    Extends Node with mandatory ``pk`` and ``nom`` properties.

    Args:
        pk: Primary key.
        nom: Entity name.
        alternative_labels: Additional labels.
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk", "nom")

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize an EntitatAmbNom node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, nom, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label="ner_tag",
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class IndividuAgregat(Node):
    """An aggregated person entity with configurable mandatory properties.

    Extends Node with a configurable set of mandatory properties
    derived from a tuple or list of property names.

    Args:
        pk: Primary key (defaults to empty string).
        main_label: Primary Cypher label (defaults to "PersonaAgregat").
        alternative_labels: Additional labels (appends "Individu").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties: Tuple[str, ...] = ("pk",)

    def __init__(
        self,
        pk: str = "",
        main_label: str = "PersonaAgregat",
        ignore_assertion: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize an IndividuAgregat node.

        Args:
            pk: Primary key.
            main_label: Primary Cypher label.
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "Individu")
        else:
            al = ["Individu"]

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label=main_label,
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class Atribut(Node):
    """A value node wrapping a string attribute.

    Extends Node to represent a string value as a graph node with
    label "Valor" and a ``name`` primary key derived from the value.

    Args:
        value: The string value to wrap.
        **kwargs: Additional node attributes passed to Node.__init__.
    """

    def __init__(self, value: str, **kwargs: Any) -> None:
        """Initialize an Atribut value node.

        Args:
            value: The string value. Stored as ``{"name": value.lower()}`` pk.
            **kwargs: Passed to Node.__init__ (alternative_labels, etc.).
        """
        Node.__init__(
            self,
            pk={"name": value.lower()},
            main_label="Valor",
            **kwargs,
        )


class Esdeventiment(Node):
    """An event entity.

    Extends Node with mandatory ``pk`` property and label "Esdeveniment".

    Args:
        pk: Primary key.
        alternative_labels: Additional labels (appends "Semantic").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk",)

    def __init__(
        self, ignore_assertion: bool = False, **kwargs: Any
    ) -> None:
        """Initialize an Esdeventiment node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label="Esdeveniment",
                pk=kwargs.get("pk"),
                alternative_labels="Semantic",
                **kwargs,
            )
        else:
            print(message)
            exit()


class LlocPadro(Node):
    """A location entity with a custom label.

    Extends Node with mandatory ``pk`` property.
    The ``alternative_labels`` automatically appends "Lloc".

    Args:
        main_label: Primary Cypher label (default "LlocPadro").
        pk: Primary key.
        alternative_labels: Additional labels (appends "Lloc").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk",)

    def __init__(
        self, main_label: str = "LlocPadro", ignore_assertion: bool = False, **kwargs: Any
    ) -> None:
        """Initialize a LlocPadro node.

        Args:
            main_label: Primary Cypher label.
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "Lloc")
        else:
            al = ["Lloc"]

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label=main_label,
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class LlocFoto(Node):
    """A location entity linked to a photograph.

    Extends Node with mandatory ``pk`` property.
    The ``alternative_labels`` automatically appends "Lloc".

    Args:
        main_label: Primary Cypher label (default "LlocFoto").
        pk: Primary key.
        alternative_labels: Additional labels (appends "Lloc").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk",)

    def __init__(
        self, main_label: str = "LlocFoto", ignore_assertion: bool = False, **kwargs: Any
    ) -> None:
        """Initialize a LlocFoto node.

        Args:
            main_label: Primary Cypher label.
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "Lloc")
        else:
            al = ["Lloc"]

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label=main_label,
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class ActaTemporal(Node):
    """A temporary act/document entity.

    Extends Node with mandatory ``pk`` property and label "ActaTemporal".

    Args:
        pk: Primary key.
        alternative_labels: Additional labels (appends "Semantic").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize an ActaTemporal node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)

        if precondition:
            Node.__init__(
                self,
                main_label="ActaTemporal",
                pk=pk,
                alternative_labels="Semantic",
                **kwargs,
            )
        else:
            print(message)
            exit()


class Fons(Node):
    """A document collection (fonds) entity.

    Extends Node with mandatory ``pk`` property.
    The ``alternative_labels`` automatically appends "DocumentCultural".

    Args:
        pk: Primary key.
        alternative_labels: Additional labels (appends "DocumentCultural").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes.
    """

    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize a Fons node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to Node.__init__ (pk, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "DocumentCultural")
        else:
            al = ["DocumentCultural"]

        if precondition:
            Node.__init__(
                self,
                main_label="Fons",
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class Padro(WeakNode):
    """A padro document entity with a path property.

    Extends WeakNode with mandatory ``pk`` and ``ruta`` properties.
    The ``alternative_labels`` automatically appends "DocumentCultural".

    Args:
        parent: The parent ``Node``.
        pk: Primary key.
        ruta: Path property.
        alternative_labels: Additional labels (appends "DocumentCultural").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes passed to WeakNode.__init__.
    """

    mandatory_properties = ("pk", "ruta")

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize a Padro weak node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to WeakNode.__init__ (pk, ruta, alternative_labels,
                parent, parent_relation, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "DocumentCultural")
        else:
            al = ["DocumentCultural"]

        if precondition or ignore_assertion:
            super().__init__(
                main_label="Padro",
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class Fotografia(WeakNode):
    """A photograph entity.

    Extends WeakNode with mandatory ``pk`` property.

    Args:
        parent: The parent ``Node``.
        pk: Primary key.
        alternative_labels: Additional labels.
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes passed to WeakNode.__init__.
    """

    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize a Fotografia weak node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to WeakNode.__init__ (pk, alternative_labels,
                parent, parent_relation, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)

        if precondition:
            super().__init__(
                main_label="Fotografia",
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


NODES = [
    IndividuPadro,
    IndividuFoto,
    Atribut,
    IndividuAgregat,
    Esdeventiment,
    LlocPadro,
    LlocFoto,
    ActaTemporal,
    Fons,
    Padro,
    Fotografia,
]


# ======= Layout Nodes ===============
class RegioFisica(WeakNode):
    """A physical region entity with contours.

    Extends WeakNode with mandatory ``main_label``, ``pk``, and ``contours``
    properties. The ``alternative_labels`` automatically appends "layout".

    Args:
        parent: The parent ``Node``.
        main_label: Primary Cypher label.
        pk: Primary key.
        contours: Region contour data.
        alternative_labels: Additional labels (appends "layout").
        **kwargs: Additional node attributes passed to WeakNode.__init__.
    """

    mandatory_properties = ("main_label", "pk", "contours")

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a RegioFisica weak node.

        Args:
            **kwargs: Passed to WeakNode.__init__ (main_label, pk, contours,
                parent, parent_relation, alternative_labels, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )

        if precondition:
            main_label = kwargs.pop("main_label", None)
            pk = kwargs.pop("pk", None)
            al = kwargs.pop("alternative_labels", None)
            if al is not None:
                al = _build_alternative_labels(al, "layout")
            else:
                al = ["layout"]

            super().__init__(
                main_label=main_label,
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class OCRTranscript(WeakNode):
    """An OCR transcript entity.

    Extends WeakNode with a ``main_label`` and optional ``pk``.
    The ``alternative_labels`` automatically appends "semantic".

    Args:
        parent: The parent ``Node``.
        main_label: Primary Cypher label.
        pk: Primary key.
        alternative_labels: Additional labels (appends "semantic").
        **kwargs: Additional node attributes passed to WeakNode.__init__.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize an OCRTranscript weak node.

        Args:
            **kwargs: Passed to WeakNode.__init__ (main_label, pk,
                parent, parent_relation, alternative_labels, etc.).
        """
        main_label = kwargs.pop("main_label")
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            al = _build_alternative_labels(al, "semantic")
        else:
            al = ["semantic"]

        super().__init__(
            main_label=main_label,
            pk=pk,
            alternative_labels=al,
            **kwargs,
        )


# ======= Document Nodes =============
class DocumentCultural(Node):
    """An abstract base class for cultural documents.

    This class should not be instantiated directly. Subclasses
    override ``document_class`` to set the appropriate label.

    Attributes:
        document_class: The Cypher label for this document type.
            Defaults to "abstract_class".
    """

    document_class = "abstract_class"

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a DocumentCultural node.

        Args:
            **kwargs: Passed to Node.__init__ (alternative_labels, etc.).
        """
        Node.__init__(
            self,
            alternative_labels="document",
            main_label=self.document_class,
            **kwargs,
        )


class BOE(WeakNode):
    """A Boletín Oficial del Estado (Spanish government gazette) entity.

    Extends WeakNode with mandatory ``pk`` and ``ruta`` properties.

    Args:
        parent: The parent ``Node``.
        pk: Primary key.
        ruta: Path to the document.
        alternative_labels: Additional labels (appends "document").
        ignore_assertion: If True, skip mandatory property checks.
        **kwargs: Additional node attributes passed to WeakNode.__init__.
    """

    mandatory_properties = ("pk", "ruta")

    def __init__(self, ignore_assertion: bool = False, **kwargs: Any) -> None:
        """Initialize a BOE weak node.

        Args:
            ignore_assertion: Skip mandatory property checks.
            **kwargs: Passed to WeakNode.__init__ (pk, ruta, alternative_labels,
                parent, parent_relation, etc.).
        """
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)

        if precondition:
            super().__init__(
                main_label="BOE",
                pk=pk,
                alternative_labels="document",
                **kwargs,
            )
        elif ignore_assertion:
            if "ruta" not in kwargs:
                kwargs["ruta"] = "Camp obligatori sense dades"
            super().__init__(
                main_label="BOE",
                pk=pk,
                alternative_labels="document",
                **kwargs,
            )
        else:
            print(message)
            exit()


EDGES = []
