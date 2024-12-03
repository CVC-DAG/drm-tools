from traitlets import Bool
from .base import Node, Relation, WeakNode
from typing import *


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
) -> Tuple[Bool, str]:
    """
    Precondition on node insertion: Asserts if a specified property isn't instance.

    Input:
        args: dict of arguments for a certain entity
        properties: iterable with properties to be asserted
        entity: Entity we are checking out
        accepted_types: Tuple of accepted types* as property of object type Node or Relation.
                        * Makes no sense to accept non-hashable types.

    Returns: Boolean and list of exceptions
    """
    for prop in properties:
        if not isinstance(args.get(prop, None), accepted_types):
            return (
                False,
                f"AssertionError: Node type {type(entity).__name__} must receive {prop}, therefore hasn't been added.",
            )  # Node not constructed: TODO should it return an error?
    # if a certain property 'prop' (stated as mandatory) is not on the constructor.
    return (True, "OKAY")  # otherwise it's true


# =================== Nodes =======================
# TODO: Check https://gitlab.cvc.uab.cat/dag/AdministrativeDocumentsGT/blob/master/core/entities.py
#       as examples of proper entitie construction


# ========= Semantic Nodes =============
class IndividuPadro(Node):
    existing_relations = ("nom",)
    be_value_properties = ("nom", "cognom1", "cognom2")
    mandatory_properties = existing_relations

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            if isinstance(al, list):
                al = [*al, "Individu"]
            if isinstance(al, str):
                al = [al, "Individu"]
        else:
            al = ["Individu"]

        if precondition or ignore_assertion:
            # comprovem si hi ha atributs amb algunes de les relacions predefinides
            deps = dict()
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

    # def __str__(self) -> str:
    #    return f"Node type {self.name}"


class IndividuFoto(Node):
    be_value_properties = []  # ("nom", "cognom1", "cognom2")
    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            if isinstance(al, list):
                al = [*al, "Individu"]
            if isinstance(al, str):
                al = [al, "Individu"]
        else:
            al = ["Individu"]

        if precondition or ignore_assertion:
            # comprovem si hi ha atributs amb algunes de les relacions predefinides
            deps = dict()
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
    mandatory_properties = ("pk", "nom")

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
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
    name = "individu_agregat_node"
    pk = ""
    if isinstance(pk, (tuple, list)):
        mandatory_properties = (
            *pk,
        )  # TODO: Define mandatory_properties on class "individu"
    else:
        mandatory_properties = ("main_label", pk)

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            if isinstance(al, list):
                al = [*al, "Individu"]
            if isinstance(al, str):
                al = [al, "Individu"]
        else:
            al = ["Individu"]

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label="PersonaAgregat",
                pk=self.pk,
                alternative_labels=al,
                **kwargs,
            )  # TODO: Primary key is left
        else:
            print(message)
            exit()


class Atribut(Node):
    name = "atribut_node"
    pk = None
    if isinstance(pk, (tuple, list)):
        mandatory_properties = (
            *pk,
        )  # TODO: Define mandatory_properties on class "individu"
    else:
        mandatory_properties = ("main_label", pk)

    def __init__(self, value: str, **kwargs: Any) -> None:
        # precondition, message = assert_on_properties(
        #    kwargs, self.mandatory_properties, self
        # )

        # if precondition:
        Node.__init__(
            self,
            pk={"name": value.lower()},
            main_label="Valor",
            **kwargs,
        )  # TODO: Primary key is left
        # else:
        #    print(message)


class Esdeventiment(Node):
    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label="Esdeveniment",
                pk=self.pk,
                alternative_labels="Semantic",
                **kwargs,
            )  # TODO: Primary key is left
        else:
            print(message)
            exit()


class LlocPadro(Node):
    mandatory_properties = ("pk",)

    def __init__(
        self, main_label="LlocPadro", ignore_assertion=False, **kwargs: Any
    ) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            if isinstance(al, list):
                al = [*al, "Lloc"]
            if isinstance(al, str):
                al = [al, "Lloc"]
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
    mandatory_properties = ("pk",)

    def __init__(
        self, main_label="LlocFoto", ignore_assertion=False, **kwargs: Any
    ) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            if isinstance(al, list):
                al = [*al, "Lloc"]
            if isinstance(al, str):
                al = [al, "Lloc"]
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
    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
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
    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            if isinstance(al, list):
                al = [*al, "DocumentCultural"]
            if isinstance(al, str):
                al = [al, "DocumentCultural"]
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
    mandatory_properties = ("pk", "ruta")

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)
        if al is not None:
            if isinstance(al, list):
                al = [*al, "DocumentCultural"]
            if isinstance(al, str):
                al = [al, "DocumentCultural"]
        else:
            al = ["DocumentCultural"]

        if precondition or ignore_assertion:
            Node.__init__(
                self,
                main_label="Padro",
                pk=pk,
                alternative_labels=al,
                **kwargs,
            )
        else:
            print(message)
            exit()


class Fotografia(WeakNode):
    mandatory_properties = ("pk",)

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)
        al = kwargs.pop("alternative_labels", None)

        if precondition:
            Node.__init__(
                self,
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
    # TODO: Define betach and cascade for weak node connecting semantic (detach) and cascade (from document)
    name = "regio_fisica_node"
    pk = ""
    mandatory_properties = ("main_label", pk, "contours")

    def __init__(self, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        main_label = kwargs.pop("main_label", None)

        if precondition:
            Node.__init__(
                self,
                main_label=main_label,
                pk=kwargs[self.pk],
                alternative_labels="layout",
                kwargs={**kwargs},
            )  # TODO: Primary key is left
        else:
            print(message)
            exit()


class OCRTranscript(WeakNode):

    def __init__(self, **kwargs: Any) -> None:

        pk = kwargs.pop("pk", None)

        Node.__init__(
            self,
            main_label=kwargs.pop("main_label"),
            pk=pk,
            alternative_labels="semantic",
            **kwargs,
        )


# ======= Document Nodes =============
class DocumentCultural(Node):
    document_class = "abstract_class"

    mandatory_properties = "path_to_document"

    def __init__(self, **kwargs: Any) -> None:
        """
        Init for abstract class "document cultural"
        Will set a document class depending the name of the children class we are constructing.

        main_label = self.document_class takes the value of the child, therefore you can define the methods for documents here.
        Init should be done by child.

        """

        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        if precondition:
            Node.__init__(
                alternative_labels="document",
                main_label=self.document_class,
                kwargs={**kwargs},
            )  # TODO: Primmary key
        else:
            print(message)
            exit()


class BOE(WeakNode):
    mandatory_properties = ("pk", "ruta")

    def __init__(self, ignore_assertion=False, **kwargs: Any) -> None:
        precondition, message = assert_on_properties(
            kwargs, self.mandatory_properties, self
        )
        pk = kwargs.pop("pk", None)

        if precondition:
            Node.__init__(
                self,
                main_label="BOE",
                pk=pk,
                alternative_labels="document",
                **kwargs,
            )
        elif ignore_assertion:
            if "ruta" not in kwargs:
                kwargs["ruta"] = "Camp obligatori sense dades"
            Node.__init__(
                self,
                main_label="BOE",
                pk=pk,
                alternative_labels="document",
                **kwargs,
            )
        else:
            print(message)
            exit()


EDGES = []
