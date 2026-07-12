"""Auto-generated entity classes from schema."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from drm.base import Node, WeakNode, Relation, WeakRelation


class AccumulationRelation(WeakNode):
    """Connects at least one Record Resource or Instantiation to at least
         one Agent, when the Record Resource or Instantiation is or was accumulated by the Agent, be
         it intentionally (collecting it) or not (receiving it in the course of its activities). The
         Record Resource(s) or Instantiation(s) is the source of the Relation, and the Agent(s) is
         the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AccumulationRelation weak node.

        Args:
            parent: The parent OrganicProvenanceRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AccumulationRelation", parent_relation="HAS_ACCUMULATIONRELATION", **kwargs)
class Activity(WeakNode):
    """The doing of something for some human purpose.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Activity weak node.

        Args:
            parent: The parent Event instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Activity", parent_relation="HAS_ACTIVITY", **kwargs)
class ActivityDocumentationRelation(WeakNode):
    """Connects at least one Record Resource or Instantiation to at least
         one Activity, when the Record Resource or Instantiation results from the Activity. The
         Record Resource(s) or Instantiation(s) is the source of the Relation, and the
         Activity(-ies) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a ActivityDocumentationRelation weak node.

        Args:
            parent: The parent OrganicOrFunctionalProvenanceRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="ActivityDocumentationRelation", parent_relation="HAS_ACTIVITYDOCUMENTATIONRELATION", **kwargs)
class ActivityType(WeakNode):
    """Categorization of an Activity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a ActivityType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="ActivityType", parent_relation="HAS_ACTIVITYTYPE", **kwargs)
class Agent(WeakNode):
    """A Person, or Group, or an entity created by a Person or Group
         (Mechanism), or a Position, that acts in the world.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Agent weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Agent", parent_relation="HAS_AGENT", **kwargs)
        self.authorizingMandate = kwargs.get("authorizingMandate", 'string')
class AgentControlRelation(WeakNode):
    """Connects at least one Agent, to at least another Agent, when the
         first one(s) control(s) or controlled in a way the activities of the second one(s). The
         Relation is oriented from the controlling agent to the controlled one: the controlling
         Agent(s) is the source of the Relation, and the controlled Agent(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AgentControlRelation weak node.

        Args:
            parent: The parent AuthorityRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AgentControlRelation", parent_relation="HAS_AGENTCONTROLRELATION", **kwargs)
class AgentHierarchicalRelation(WeakNode):
    """Connects at least one Agent to at least another Agent, when the
         first one is or was hierarchically superior to the second one. The Relation is oriented
         towards the 'bottom' of the hierarchical tree: the superior Agent(s) is the source of the
         Relation, and the inferior Agent(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AgentHierarchicalRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AgentHierarchicalRelation", parent_relation="HAS_AGENTHIERARCHICALRELATION", **kwargs)
class AgentName(WeakNode):
    """A label, title or term designating an Agent in order to make it
         distinguishable from other similar entities.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AgentName weak node.

        Args:
            parent: The parent Name instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AgentName", parent_relation="HAS_AGENTNAME", **kwargs)
class AgentTemporalRelation(WeakNode):
    """Connects at least one Agent to at least another Agent that
         succeeds it chronologically for, for instance, fullfilling some functions or performing
         some activities. The Relation is oriented chronologically, from the predecessor to the
         successor: the predecessor Agent(s) is the source of the Relation, and the successor
         Agent(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AgentTemporalRelation weak node.

        Args:
            parent: The parent TemporalRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AgentTemporalRelation", parent_relation="HAS_AGENTTEMPORALRELATION", **kwargs)
class AgentToAgentRelation(WeakNode):
    """Connects at least two Agents. This Relation is a generic, not
         oriented one.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AgentToAgentRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AgentToAgentRelation", parent_relation="HAS_AGENTTOAGENTRELATION", **kwargs)
class Appellation(WeakNode):
    """A concept of any kind that is used for designating an Entity and
         referring to it.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Appellation weak node.

        Args:
            parent: The parent Concept instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Appellation", parent_relation="HAS_APPELLATION", **kwargs)
        self.usedFromDate = kwargs.get("usedFromDate", 'string')
        self.usedToDate = kwargs.get("usedToDate", 'string')
class AppellationRelation(WeakNode):
    """Connects an Appellation and at least one Thing that the
         Appellation designates or designated. The Appellation is the source of the Relation and the
         Thing(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AppellationRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AppellationRelation", parent_relation="HAS_APPELLATIONRELATION", **kwargs)
class AuthorityRelation(WeakNode):
    """Connects at least one Agent and at least one Thing over which the
         Agent has or had some authority. The Agent(s) is the source of the relation, and the
         Thing(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AuthorityRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AuthorityRelation", parent_relation="HAS_AUTHORITYRELATION", **kwargs)
class AuthorshipRelation(WeakNode):
    """Connects at least one Record to at least one Person, Group or
         Position that is or was responsible for conceiving and formulating the information
         contained in the Record. The Record is the source of the Relation and the Person(s),
         Group(s) or Position(s) is the target. ."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a AuthorshipRelation weak node.

        Args:
            parent: The parent CreationRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="AuthorshipRelation", parent_relation="HAS_AUTHORSHIPRELATION", **kwargs)
class CarrierExtent(WeakNode):
    """Number of physical units and/or physical dimensions of the carrier
         of an Instantiation.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a CarrierExtent weak node.

        Args:
            parent: The parent Extent instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="CarrierExtent", parent_relation="HAS_CARRIEREXTENT", **kwargs)
class CarrierType(WeakNode):
    """Categorization of physical material on which information is
         represented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a CarrierType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="CarrierType", parent_relation="HAS_CARRIERTYPE", **kwargs)
class ChildRelation(WeakNode):
    """Connects at least one Person to at least another Person, when the
         first has(ave) child(s) the second one(s). The Relation is oriented from the parent to the
         child: the parent is the source of the relation, and the child(ren) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a ChildRelation weak node.

        Args:
            parent: The parent DescendanceRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="ChildRelation", parent_relation="HAS_CHILDRELATION", **kwargs)
class Concept(WeakNode):
    """An idea, unit of thought, abstract cultural object or
         category."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Concept weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Concept", parent_relation="HAS_CONCEPT", **kwargs)
class ContentType(WeakNode):
    """The fundamental form of communication in which a Record or Record
         Part is expressed.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a ContentType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="ContentType", parent_relation="HAS_CONTENTTYPE", **kwargs)
class Coordinates(WeakNode):
    """Longitudinal and latitudinal information about a
         Place.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Coordinates weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Coordinates", parent_relation="HAS_COORDINATES", **kwargs)
        self.altimetricSystem = kwargs.get("altimetricSystem", 'string')
        self.altitude = kwargs.get("altitude", 'string')
        self.geodesicSystem = kwargs.get("geodesicSystem", 'string')
        self.latitude = kwargs.get("latitude", 'string')
        self.longitude = kwargs.get("longitude", 'string')
class CorporateBody(WeakNode):
    """An organized group of persons that act together as an Agent, and
         that has a recognized legal or social status.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a CorporateBody weak node.

        Args:
            parent: The parent Group instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="CorporateBody", parent_relation="HAS_CORPORATEBODY", **kwargs)
class CorporateBodyType(WeakNode):
    """Categorization of a Corporate Body.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a CorporateBodyType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="CorporateBodyType", parent_relation="HAS_CORPORATEBODYTYPE", **kwargs)
class CorrespondenceRelation(WeakNode):
    """Connects at least two Persons, when they correspond or
         corresponded to each other. This Relation is not oriented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a CorrespondenceRelation weak node.

        Args:
            parent: The parent KnowingRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="CorrespondenceRelation", parent_relation="HAS_CORRESPONDENCERELATION", **kwargs)
class CreationRelation(WeakNode):
    """Connects at least one Record Resource or Instantiation to at least
         one Agent, when the Agent is either responsible for all or some of the content of the
         Record Resource, or is a contributor to the genesis or production of the Instantiation. The
         Record Resource or Instantiation is the source of the Relation, and the Agent(s) is the
         target. ."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a CreationRelation weak node.

        Args:
            parent: The parent OrganicProvenanceRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="CreationRelation", parent_relation="HAS_CREATIONRELATION", **kwargs)
class Date(WeakNode):
    """Chronological information associated with an entity that
         contributes to its identification and contextualization.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Date weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Date", parent_relation="HAS_DATE", **kwargs)
        self.dateQualifier = kwargs.get("dateQualifier", 'string')
        self.expressedDate = kwargs.get("expressedDate", 'string')
        self.normalizedDateValue = kwargs.get("normalizedDateValue", 'string')
class DateType(WeakNode):
    """Categorization of a Date.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a DateType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="DateType", parent_relation="HAS_DATETYPE", **kwargs)
class DemographicGroup(WeakNode):
    """Categorization of a Person or Group based on shared
         characteristics.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a DemographicGroup weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="DemographicGroup", parent_relation="HAS_DEMOGRAPHICGROUP", **kwargs)
class DerivationRelation(WeakNode):
    """Connects an Instantiation to at least one Instantiation that is
         derived from it, whether it exists or has been lost or destroyed. The Relation is oriented
         chronologically, from the first Instantiation in time to the derived Instantiation: the
         first Instantiation is the source of the Relation, and the derived Instantiation(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a DerivationRelation weak node.

        Args:
            parent: The parent InstantiationToInstantiationRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="DerivationRelation", parent_relation="HAS_DERIVATIONRELATION", **kwargs)
class DescendanceRelation(WeakNode):
    """Connects at least one Person to at least another Person, when the
         first has/have descendant the second one(s). The Relation is oriented from the ascendant to
         the descendant: the ascendant Person(s) is the source of the Relation, and the descendant
         Person(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a DescendanceRelation weak node.

        Args:
            parent: The parent FamilyRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="DescendanceRelation", parent_relation="HAS_DESCENDANCERELATION", **kwargs)
class DocumentaryFormType(WeakNode):
    """Categorization of a Record or Record Part with respect to its
         extrinsic and intrinsic elements that together communicate its content, administrative and
         documentary context, and authority.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a DocumentaryFormType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="DocumentaryFormType", parent_relation="HAS_DOCUMENTARYFORMTYPE", **kwargs)
class Event(WeakNode):
    """Something that happens or occurs in time and space.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Event weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Event", parent_relation="HAS_EVENT", **kwargs)
class EventRelation(WeakNode):
    """Connects at least one Event to at least one Thing, when the first
         is associated with the existence and lifecycle of the second one. The Event(s) is the
         source of the Relation, and the Thing(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a EventRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="EventRelation", parent_relation="HAS_EVENTRELATION", **kwargs)
class EventType(WeakNode):
    """Categorization of an Event.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a EventType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="EventType", parent_relation="HAS_EVENTTYPE", **kwargs)
class Extent(WeakNode):
    """Countable characteristics of the content of an entity expressed as
         a quantity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Extent weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Extent", parent_relation="HAS_EXTENT", **kwargs)
        self.quantity = kwargs.get("quantity", 'float')
        self.unitOfMeasurement = kwargs.get("unitOfMeasurement", 'string')
class ExtentType(WeakNode):
    """Categorization of the extent that is being
         measured.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a ExtentType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="ExtentType", parent_relation="HAS_EXTENTTYPE", **kwargs)
class Family(WeakNode):
    """Two or more persons related by birth, or through marriage,
         adoption, civil union, or other social conventions that bind them together as a socially
         recognized familial group.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Family weak node.

        Args:
            parent: The parent Group instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Family", parent_relation="HAS_FAMILY", **kwargs)
class FamilyRelation(WeakNode):
    """Connects at least two Persons, when they have some family link,
         i.e. belong to the same family. This Relation is a generic, not oriented
         one.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a FamilyRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="FamilyRelation", parent_relation="HAS_FAMILYRELATION", **kwargs)
class FamilyType(WeakNode):
    """Categorization of a Family.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a FamilyType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="FamilyType", parent_relation="HAS_FAMILYTYPE", **kwargs)
class FunctionalEquivalenceRelation(WeakNode):
    """Connects at least two Instantiations which may be considered as
         equivalent. This Relation is not oriented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a FunctionalEquivalenceRelation weak node.

        Args:
            parent: The parent InstantiationToInstantiationRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="FunctionalEquivalenceRelation", parent_relation="HAS_FUNCTIONALEQUIVALENCERELATION", **kwargs)
class Group(WeakNode):
    """Two or more Agents that act together as an Agent.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Group weak node.

        Args:
            parent: The parent Agent instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Group", parent_relation="HAS_GROUP", **kwargs)
class GroupSubdivisionRelation(WeakNode):
    """Connects a Group and at least another Group, when the first one
         has or had the second one(s) among its subdivisions. The Relation is oriented from the
         Group to its subdivision(s): the parent Group is the source and the subdivision Group(s) is
         the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a GroupSubdivisionRelation weak node.

        Args:
            parent: The parent WholePartRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="GroupSubdivisionRelation", parent_relation="HAS_GROUPSUBDIVISIONRELATION", **kwargs)
class Identifier(WeakNode):
    """A word, number, letter, symbol, or any combination of these used
         to uniquely identify or reference an individual instance of an entity within a specific
         information domain.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Identifier weak node.

        Args:
            parent: The parent Appellation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Identifier", parent_relation="HAS_IDENTIFIER", **kwargs)
class IdentifierType(WeakNode):
    """Categorization of an Identifier.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a IdentifierType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="IdentifierType", parent_relation="HAS_IDENTIFIERTYPE", **kwargs)
class Instantiation(WeakNode):
    """The inscription of information made by an Agent on a physical
         carrier in any persistent, recoverable form as a means of communicating information through
         time and space.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Instantiation weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Instantiation", parent_relation="HAS_INSTANTIATION", **kwargs)
        self.carrierExtent = kwargs.get("carrierExtent", 'string')
        self.derivationDate = kwargs.get("derivationDate", 'string')
        self.instantiationExtent = kwargs.get("instantiationExtent", 'string')
        self.instantiationStructure = kwargs.get("instantiationStructure", 'string')
        self.migrationDate = kwargs.get("migrationDate", 'string')
        self.physicalCharacteristicsNote = kwargs.get("physicalCharacteristicsNote", 'string')
        self.productionTechnique = kwargs.get("productionTechnique", 'string')
        self.qualityOfRepresentationNote = kwargs.get("qualityOfRepresentationNote", 'string')
class InstantiationExtent(WeakNode):
    """Countable characteristics of an Instantiation expressed as a
         quantity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a InstantiationExtent weak node.

        Args:
            parent: The parent Extent instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="InstantiationExtent", parent_relation="HAS_INSTANTIATIONEXTENT", **kwargs)
class InstantiationToInstantiationRelation(WeakNode):
    """Connects at least two instantiations. This Relation is a generic,
         not oriented one.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a InstantiationToInstantiationRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="InstantiationToInstantiationRelation", parent_relation="HAS_INSTANTIATIONTOINSTANTIATIONRELATION", **kwargs)
class IntellectualPropertyRightsRelation(WeakNode):
    """Connects at least one Agent and one Record Resource or
         Instantiation on which the Agent has or had some intellectual property rights. The Agent(s)
         is the source of the Relation and the Record Resource(s) or Instantiation(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a IntellectualPropertyRightsRelation weak node.

        Args:
            parent: The parent AuthorityRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="IntellectualPropertyRightsRelation", parent_relation="HAS_INTELLECTUALPROPERTYRIGHTSRELATION", **kwargs)
class KnowingOfRelation(WeakNode):
    """Connects at least one Person to at least another one, when the
         first one has some knowledge of the second one through time or space. The first Person is
         the source of the Relation, and the second one is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a KnowingOfRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="KnowingOfRelation", parent_relation="HAS_KNOWINGOFRELATION", **kwargs)
class KnowingRelation(WeakNode):
    """Connects at least two Persons who directly know each other during
         their existence. This Relation is not oriented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a KnowingRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="KnowingRelation", parent_relation="HAS_KNOWINGRELATION", **kwargs)
class Language(WeakNode):
    """A spoken or written human language represented in a Record
         Resource or used by an Agent.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Language weak node.

        Args:
            parent: The parent Concept instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Language", parent_relation="HAS_LANGUAGE", **kwargs)
class LeadershipRelation(WeakNode):
    """Connects at least one Person and at least one Group, when the
         first one(s) lead(s) or led the second one(s). The Relation is oriented from the leading
         Person to the Group: the leading Person(s) is the source of the Relation, and the Group(s)
         is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a LeadershipRelation weak node.

        Args:
            parent: The parent AgentControlRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="LeadershipRelation", parent_relation="HAS_LEADERSHIPRELATION", **kwargs)
class LegalStatus(WeakNode):
    """A status defined by law.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a LegalStatus weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="LegalStatus", parent_relation="HAS_LEGALSTATUS", **kwargs)
class ManagementRelation(WeakNode):
    """Connects at least one Agent and at least one Record Resource or
         Instantiation that the Agent manages or managed. The Agent(s) is the source of the
         Relation, and the Record Resource(s) or Instantiation(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a ManagementRelation weak node.

        Args:
            parent: The parent AuthorityRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="ManagementRelation", parent_relation="HAS_MANAGEMENTRELATION", **kwargs)
class Mandate(WeakNode):
    """Delegation of responsibility or authority by an Agent to another
         Agent to perform an Activity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Mandate weak node.

        Args:
            parent: The parent Rule instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Mandate", parent_relation="HAS_MANDATE", **kwargs)
class MandateRelation(WeakNode):
    """Connects at least one Mandate and at least one Agent, when the
         first gives or gave the second one the authority or competencies to act. May also involve
         one to many Activities that the Mandate(s) assign(s) or assigned to the Agent(s). The
         Mandate(s) is the source of the Relation and the Agent(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a MandateRelation weak node.

        Args:
            parent: The parent RuleRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="MandateRelation", parent_relation="HAS_MANDATERELATION", **kwargs)
class MandateType(WeakNode):
    """Categorization of a Mandate.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a MandateType weak node.

        Args:
            parent: The parent RuleType instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="MandateType", parent_relation="HAS_MANDATETYPE", **kwargs)
class Mechanism(WeakNode):
    """A process or system created by a Person or Group that performs an
         Activity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Mechanism weak node.

        Args:
            parent: The parent Agent instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Mechanism", parent_relation="HAS_MECHANISM", **kwargs)
        self.technicalCharacteristics = kwargs.get("technicalCharacteristics", 'string')
class MembershipRelation(WeakNode):
    """Connects a Group and at least one Person, when the first one has
         or had the second one(s) among its members. The Relation is oriented from the Group to its
         members: the Group(s) is the source of the Relation, and the Person(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a MembershipRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="MembershipRelation", parent_relation="HAS_MEMBERSHIPRELATION", **kwargs)
class MigrationRelation(WeakNode):
    """Connects an Instantiation and at least another Instantiation it
         has been migrated into. The Relation is oriented chronologically, from the first
         Instantiation in time (the migrated one) to the one which results from its migration: the
         first Instantiation in time is the source of the Relation, and the resulting Instantiation
         is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a MigrationRelation weak node.

        Args:
            parent: The parent DerivationRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="MigrationRelation", parent_relation="HAS_MIGRATIONRELATION", **kwargs)
class Name(WeakNode):
    """A label, title or term designating an entity in order to make it
         distinguishable from other similar entities.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Name weak node.

        Args:
            parent: The parent Appellation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Name", parent_relation="HAS_NAME", **kwargs)
class OccupationType(WeakNode):
    """Categorization of a profession, trade, or craft pursued by a
         Person in fulfilment of an Activity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a OccupationType weak node.

        Args:
            parent: The parent DemographicGroup instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="OccupationType", parent_relation="HAS_OCCUPATIONTYPE", **kwargs)
class OrganicOrFunctionalProvenanceRelation(WeakNode):
    """Connects at least one Record Resource or Instantiation to at least
         one Agent or Activity, when the Agent or Activity is the provenance of the Record Resource
         or Instantiation (i.e. when the Agent created, accumulated or maintained the Record
         Resource or Instantiation, or when the Activity resulted into them). The Record Resource(s)
         or Instantiation(s) is the source of the Relation, and the Agent(s) or Activity(-ies) is
         the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a OrganicOrFunctionalProvenanceRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="OrganicOrFunctionalProvenanceRelation", parent_relation="HAS_ORGANICORFUNCTIONALPROVENANCERELATION", **kwargs)
class OrganicProvenanceRelation(WeakNode):
    """Connects at least one Record Resource or an Instantiation to at
         least one Agent that creates or accumulates the Record Resource, receives it, or sends it.
         The Record Resource(s) or Instantiation(s) is the source of the Relation, and the Agent(s)
         is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a OrganicProvenanceRelation weak node.

        Args:
            parent: The parent OrganicOrFunctionalProvenanceRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="OrganicProvenanceRelation", parent_relation="HAS_ORGANICPROVENANCERELATION", **kwargs)
class OwnershipRelation(WeakNode):
    """Connects at least one Group, Person or Position and at least a
         Thing that these Agent(s) own(s) or owned. The Group(s), Person(s) or Position(s) is the
         source of the Relation, and the Agent(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a OwnershipRelation weak node.

        Args:
            parent: The parent AuthorityRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="OwnershipRelation", parent_relation="HAS_OWNERSHIPRELATION", **kwargs)
class PerformanceRelation(WeakNode):
    """Connects at least one Activity to at least one Agent that performs
         or performed the activity. The Activity(-ies) is the source of the Relation and the
         Agent(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a PerformanceRelation weak node.

        Args:
            parent: The parent EventRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="PerformanceRelation", parent_relation="HAS_PERFORMANCERELATION", **kwargs)
class Person(WeakNode):
    """An individual human being.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Person weak node.

        Args:
            parent: The parent Agent instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Person", parent_relation="HAS_PERSON", **kwargs)
        self.birthDate = kwargs.get("birthDate", 'string')
        self.deathDate = kwargs.get("deathDate", 'string')
class PhysicalLocation(WeakNode):
    """A delimitation of the physical territory of a
         Place.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a PhysicalLocation weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="PhysicalLocation", parent_relation="HAS_PHYSICALLOCATION", **kwargs)
class Place(WeakNode):
    """Bounded, named geographic area or region.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Place weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Place", parent_relation="HAS_PLACE", **kwargs)
        self.geographicalCoordinates = kwargs.get("geographicalCoordinates", 'string')
        self.location = kwargs.get("location", 'string')
class PlaceName(WeakNode):
    """A label, title or term designating a Place in order to make it
         distinguishable from other similar entities.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a PlaceName weak node.

        Args:
            parent: The parent Name instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="PlaceName", parent_relation="HAS_PLACENAME", **kwargs)
class PlaceRelation(WeakNode):
    """Connects a Place and at least one Thing when the first is
         associated with the existence and lifecycle of the second one. The Place is the source of
         the Relation and the Thing(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a PlaceRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="PlaceRelation", parent_relation="HAS_PLACERELATION", **kwargs)
class PlaceType(WeakNode):
    """Categorization of a Place.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a PlaceType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="PlaceType", parent_relation="HAS_PLACETYPE", **kwargs)
class Position(WeakNode):
    """The functional role of a Person within a Group.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Position weak node.

        Args:
            parent: The parent Agent instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Position", parent_relation="HAS_POSITION", **kwargs)
class PositionHoldingRelation(WeakNode):
    """Connects at least one Person and at least one Position that the
         Person(s) occupies or occupied. The Person is the source of the Relation and the Position
         is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a PositionHoldingRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="PositionHoldingRelation", parent_relation="HAS_POSITIONHOLDINGRELATION", **kwargs)
class PositionToGroupRelation(WeakNode):
    """Connects at least one Position and a Group in which the
         position(s) exist(s) or existed, or that is (are) defined by that group's organizational
         structure. The Position(s) is the source of the Relation and the Group is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a PositionToGroupRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="PositionToGroupRelation", parent_relation="HAS_POSITIONTOGROUPRELATION", **kwargs)
class ProductionTechniqueType(WeakNode):
    """The method used in the representation of information on an
         instantiation.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a ProductionTechniqueType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="ProductionTechniqueType", parent_relation="HAS_PRODUCTIONTECHNIQUETYPE", **kwargs)
class Proxy(WeakNode):
    """A Proxy represents (stands for) a Record Resource as it exists in
         a specific other Record Resource.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Proxy weak node.

        Args:
            parent: The parent Concept instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Proxy", parent_relation="HAS_PROXY", **kwargs)
class Record(WeakNode):
    """Discrete information content formed and inscribed, at least once,
         by any method on any carrier in any persistent, recoverable form by an Agent in the course
         of life or work activity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Record weak node.

        Args:
            parent: The parent RecordResource instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Record", parent_relation="HAS_RECORD", **kwargs)
class RecordPart(WeakNode):
    """Component of a Record with independent information content that
         contributes to the intellectual completeness of the Record.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordPart weak node.

        Args:
            parent: The parent RecordResource instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordPart", parent_relation="HAS_RECORDPART", **kwargs)
class RecordResource(WeakNode):
    """Information produced or acquired and retained by an Agent in the
         course of life or work activity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordResource weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordResource", parent_relation="HAS_RECORDRESOURCE", **kwargs)
        self.classification = kwargs.get("classification", 'string')
        self.integrityNote = kwargs.get("integrityNote", 'string')
        self.publicationDate = kwargs.get("publicationDate", 'string')
        self.recordResourceExtent = kwargs.get("recordResourceExtent", 'string')
        self.recordResourceSourceOfInformation = kwargs.get("recordResourceSourceOfInformation", 'string')
        self.recordResourceStructure = kwargs.get("recordResourceStructure", 'string')
        self.scopeAndContent = kwargs.get("scopeAndContent", 'string')
class RecordResourceExtent(WeakNode):
    """The quantity of information content, as human experienced,
         contained in a Record Resource.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordResourceExtent weak node.

        Args:
            parent: The parent Extent instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordResourceExtent", parent_relation="HAS_RECORDRESOURCEEXTENT", **kwargs)
class RecordResourceGeneticRelation(WeakNode):
    """Connects two or more record resources when there is a genetic link
         between them. Genetic in this sense is as defined by diplomatics, i.e., the process by
         which a record resource is developed. This Relation is a generic, not oriented
         one.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordResourceGeneticRelation weak node.

        Args:
            parent: The parent RecordResourceToRecordResourceRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordResourceGeneticRelation", parent_relation="HAS_RECORDRESOURCEGENETICRELATION", **kwargs)
class RecordResourceHoldingRelation(WeakNode):
    """Connects at least one Agent and one or more Record Resource or
         Instantiation that the Agent(s) hold(s) or held. The Agent(s) is the source of the Relation
         and the Record Resource(s) or Instantiation is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordResourceHoldingRelation weak node.

        Args:
            parent: The parent ManagementRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordResourceHoldingRelation", parent_relation="HAS_RECORDRESOURCEHOLDINGRELATION", **kwargs)
class RecordResourceToInstantiationRelation(WeakNode):
    """Connects a Record Resource to one or more Instantiations that
         instantiate it, and which either may exist or may have been lost or destroyed. The Record
         Resource is the source of the Relation and the Instantiation(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordResourceToInstantiationRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordResourceToInstantiationRelation", parent_relation="HAS_RECORDRESOURCETOINSTANTIATIONRELATION", **kwargs)
class RecordResourceToRecordResourceRelation(WeakNode):
    """Connects at least two Record Resources. This Relation is a
         generic, not oriented one.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordResourceToRecordResourceRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordResourceToRecordResourceRelation", parent_relation="HAS_RECORDRESOURCETORECORDRESOURCERELATION", **kwargs)
class RecordSet(WeakNode):
    """One or more records that are grouped together by an Agent based on
         the records sharing one or more attributes or relations.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordSet weak node.

        Args:
            parent: The parent RecordResource instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordSet", parent_relation="HAS_RECORDSET", **kwargs)
        self.accruals = kwargs.get("accruals", 'string')
        self.accrualsStatus = kwargs.get("accrualsStatus", 'string')
        self.allMembersWithAccumulationDate = kwargs.get("allMembersWithAccumulationDate", 'string')
        self.allMembersWithCreationDate = kwargs.get("allMembersWithCreationDate", 'string')
        self.mostMembersWithAccumulationDate = kwargs.get("mostMembersWithAccumulationDate", 'string')
        self.mostMembersWithCreationDate = kwargs.get("mostMembersWithCreationDate", 'string')
        self.someMembersWithAccumulationDate = kwargs.get("someMembersWithAccumulationDate", 'string')
        self.someMembersWithCreationDate = kwargs.get("someMembersWithCreationDate", 'string')
class RecordSetType(WeakNode):
    """A broad categorization of the type of Record Set.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordSetType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordSetType", parent_relation="HAS_RECORDSETTYPE", **kwargs)
class RecordState(WeakNode):
    """Description of the production or reproduction status of a Record
         or Record Part.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RecordState weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RecordState", parent_relation="HAS_RECORDSTATE", **kwargs)
class Relation(WeakNode):
    """The top level relation class. It connects at least two Things. An
         instance of a Relation may have some datatype and object properties: a general description
         (datatype property) like any Thing; a certainty (for 'certain', 'quite probable',
         'uncertain','unknown'); a date (use either the date datatype property or the Date class and
         isAssociatedWithDate object property); a state (relationState); a location (use the Place
         class and isAssociatedWithPlace object property); a source of information that can be used
         as an evidence for it (use either source datatype property or hasSource object property).
         This Relation is the most generic one; it is not oriented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Relation weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Relation", parent_relation="HAS_RELATION", **kwargs)
        self.relationCertainty = kwargs.get("relationCertainty", 'string')
        self.relationSource = kwargs.get("relationSource", 'string')
        self.relationState = kwargs.get("relationState", 'string')
class RepresentationType(WeakNode):
    """Method of recording the content type of an
         Instantiation."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RepresentationType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RepresentationType", parent_relation="HAS_REPRESENTATIONTYPE", **kwargs)
class RoleType(WeakNode):
    """The role an Agent plays in some context (usually in some creation
         relation). Not to be confused with a Position (position of an agent in some group). For
         example, a Person who is the head of some Corporate Body may play the role of annotator (of
         a record) in a creation relation.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RoleType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RoleType", parent_relation="HAS_ROLETYPE", **kwargs)
class Rule(WeakNode):
    """Conditions that govern the existence, responsibility, or authority
         of an Agent; or the performance of an Activity by an Agent; or that contribute to the
         distinct characteristics of things created or managed by an Agent.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Rule weak node.

        Args:
            parent: The parent Thing instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Rule", parent_relation="HAS_RULE", **kwargs)
class RuleRelation(WeakNode):
    """Connects at least one Rule to at least one Thing when it is
         associated with existence and lifecycle of the Thing. The Rule(s) is the source of the
         Relation, and the Thing(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RuleRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RuleRelation", parent_relation="HAS_RULERELATION", **kwargs)
class RuleType(WeakNode):
    """Categorization of a Rule.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a RuleType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="RuleType", parent_relation="HAS_RULETYPE", **kwargs)
class SequentialRelation(WeakNode):
    """Connects at least one Thing to at least one other Thing that
         follows or followed it in some sequence. The Relation is oriented from the first Thing(s)
         in the sequence to the following one(s): the first Thing(s) is the source, and the
         following Thing(s) is the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a SequentialRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="SequentialRelation", parent_relation="HAS_SEQUENTIALRELATION", **kwargs)
class SiblingRelation(WeakNode):
    """Connects at least two Persons, when they are siblings. This
         Relation is not oriented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a SiblingRelation weak node.

        Args:
            parent: The parent FamilyRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="SiblingRelation", parent_relation="HAS_SIBLINGRELATION", **kwargs)
class SpouseRelation(WeakNode):
    """Connects at least two Persons, when they are spouses. This
         Relation is not oriented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a SpouseRelation weak node.

        Args:
            parent: The parent FamilyRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="SpouseRelation", parent_relation="HAS_SPOUSERELATION", **kwargs)
class StudyAtRelation(WeakNode):
    """Connects a Group (as an educational institution) to at least one
         Person who studied or study at this group. Both 'institution' and 'at' can be interpreted
         broadly. The Relation is oriented from the educational institution to the student(s): the
         former is the source of the Relation, and the latter is/are the target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a StudyAtRelation weak node.

        Args:
            parent: The parent MembershipRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="StudyAtRelation", parent_relation="HAS_STUDYATRELATION", **kwargs)
class TeachingRelation(WeakNode):
    """Connects at least one Person to at least another Person who is or
         was their student. The Relation is oriented from the teacher(s) to the student(s): the
         teacher Person(s) is the source of the Relation, and the student Person(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a TeachingRelation weak node.

        Args:
            parent: The parent KnowingRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="TeachingRelation", parent_relation="HAS_TEACHINGRELATION", **kwargs)
class TemporalRelation(WeakNode):
    """Connects at least one Thing to at least one other Thing that
         follows it in chronological order. The Relation is oriented chronologically: the preceding
         Thing(s) is the source of the Relation, the following Thing(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a TemporalRelation weak node.

        Args:
            parent: The parent SequentialRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="TemporalRelation", parent_relation="HAS_TEMPORALRELATION", **kwargs)
class Thing(Node):
    """Any idea, material thing, or event within the realm of human
         experience.."""

    def __init__(self, pk: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        """Initialize a Thing node.

        Args:
            pk: Optional primary key dict. When not provided, the backend assigns an ID.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(pk=pk, main_label="Thing", **kwargs)
        self.beginningDate = kwargs.get("beginningDate", 'string')
        self.date = kwargs.get("date", 'string')
        self.endDate = kwargs.get("endDate", 'string')
        self.generalDescription = kwargs.get("generalDescription", 'string')
        self.height = kwargs.get("height", 'string')
        self.identifier = kwargs.get("identifier", 'string')
        self.lastModificationDate = kwargs.get("lastModificationDate", 'string')
        self.length = kwargs.get("length", 'string')
        self.measure = kwargs.get("measure", 'string')
        self.modificationDate = kwargs.get("modificationDate", 'string')
        self.name = kwargs.get("name", 'string')
        self.note = kwargs.get("note", 'string')
        self.referenceSystem = kwargs.get("referenceSystem", 'string')
        self.ruleFollowed = kwargs.get("ruleFollowed", 'string')
        self.type = kwargs.get("type", 'string')
        self.width = kwargs.get("width", 'string')
class Title(WeakNode):
    """A name that is used for a Record Resource or a Rule."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Title weak node.

        Args:
            parent: The parent Name instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Title", parent_relation="HAS_TITLE", **kwargs)
class TitleType(WeakNode):
    """Categorization of a Title.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a TitleType weak node.

        Args:
            parent: The parent Type instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="TitleType", parent_relation="HAS_TITLETYPE", **kwargs)
class Type(WeakNode):
    """A superclass for any type of some thing. A type characterizes an
         entity.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a Type weak node.

        Args:
            parent: The parent Concept instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="Type", parent_relation="HAS_TYPE", **kwargs)
class TypeRelation(WeakNode):
    """Connects a category (a Type) and at least one Thing that belongs
         to this category. The Type(s) is the source of the Relation, and the Thing(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a TypeRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="TypeRelation", parent_relation="HAS_TYPERELATION", **kwargs)
class UnitOfMeasurement(WeakNode):
    """A definite magnitude of a quantity, defined and adopted by
         convention or by law, that is used as a standard for measurement of the same kind of
         quantity. Can be spacial units (cm, m), weight (g, kg), time (s, h), storage (MB, TB) or
         more informal units used in the archival context like number of boxes, pages or
         words.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a UnitOfMeasurement weak node.

        Args:
            parent: The parent Concept instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="UnitOfMeasurement", parent_relation="HAS_UNITOFMEASUREMENT", **kwargs)
class WholePartRelation(WeakNode):
    """Connects a Thing to at least one other Thing that is or was a
         portion or division of the whole Thing. The Relation is oriented from the Thing to its
         part(s): the Thing is the source of the Relation, and the part Thing(s) is the
         target.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a WholePartRelation weak node.

        Args:
            parent: The parent Relation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="WholePartRelation", parent_relation="HAS_WHOLEPARTRELATION", **kwargs)
class WorkRelation(WeakNode):
    """Connects at least two Agents that have or had some type of work
         relation in the course of their activities. This Relation is not oriented.."""

    def __init__(self, parent: Node, **kwargs: Any) -> None:
        """Initialize a WorkRelation weak node.

        Args:
            parent: The parent AgentToAgentRelation instance.
            **kwargs: Additional properties and attributes.
        """
        super().__init__(parent=parent, main_label="WorkRelation", parent_relation="HAS_WORKRELATION", **kwargs)
class AccumulationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AccumulationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="accumulationRelation_role", **kwargs)
class ActivitydocumentationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a ActivitydocumentationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="activityDocumentationRelation_role", **kwargs)
class Activityiscontextofrelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Activityiscontextofrelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="activityIsContextOfRelation", **kwargs)
class Affectsoraffected(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Affectsoraffected relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="affectsOrAffected", **kwargs)
class AgentcontrolrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AgentcontrolrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="agentControlRelation_role", **kwargs)
class Agenthasorhadlocation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Agenthasorhadlocation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="agentHasOrHadLocation", **kwargs)
class AgenthierarchicalrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AgenthierarchicalrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="agentHierarchicalRelation_role", **kwargs)
class AgenttemporalrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AgenttemporalrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="agentTemporalRelation_role", **kwargs)
class AgenttoagentrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AgenttoagentrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="agentToAgentRelation_role", **kwargs)
class AppellationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AppellationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="appellationRelation_role", **kwargs)
class Asconcernsactivity(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Asconcernsactivity relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="asConcernsActivity", **kwargs)
class AuthorityrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AuthorityrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="authorityRelation_role", **kwargs)
class Authorizedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Authorizedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="authorizedBy", **kwargs)
class Authorizes(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Authorizes relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="authorizes", **kwargs)
class Authorizingagent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Authorizingagent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="authorizingAgent", **kwargs)
class AuthorshiprelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a AuthorshiprelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="authorshipRelation_role", **kwargs)
class ChildrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a ChildrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="childRelation_role", **kwargs)
class Contained(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Contained relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="contained", **kwargs)
class Containsorcontained(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Containsorcontained relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="containsOrContained", **kwargs)
class Containstransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Containstransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="containsTransitive", **kwargs)
class CorrespondencerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a CorrespondencerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="correspondenceRelation_role", **kwargs)
class CreationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a CreationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="creationRelation_role", **kwargs)
class Creationwithrole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Creationwithrole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="creationWithRole", **kwargs)
class DerivationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a DerivationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="derivationRelation_role", **kwargs)
class DescendancerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a DescendancerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="descendanceRelation_role", **kwargs)
class Describesordescribed(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Describesordescribed relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="describesOrDescribed", **kwargs)
class Directlycontains(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Directlycontains relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="directlyContains", **kwargs)
class Directlyfollowsinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Directlyfollowsinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="directlyFollowsInSequence", **kwargs)
class Directlyfollowsproxyinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Directlyfollowsproxyinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="directlyFollowsProxyInSequence", **kwargs)
class Directlyincludes(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Directlyincludes relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="directlyIncludes", **kwargs)
class Directlyincludesproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Directlyincludesproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="directlyIncludesProxy", **kwargs)
class Directlyprecedesinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Directlyprecedesinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="directlyPrecedesInSequence", **kwargs)
class Directlyprecedesproxyinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Directlyprecedesproxyinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="directlyPrecedesProxyInSequence", **kwargs)
class Documentedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Documentedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="documentedBy", **kwargs)
class Documents(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Documents relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="documents", **kwargs)
class EventrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a EventrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="eventRelation_role", **kwargs)
class Evidences(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Evidences relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="evidences", **kwargs)
class Existsorexistedin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Existsorexistedin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="existsOrExistedIn", **kwargs)
class Expressesorexpressed(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Expressesorexpressed relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="expressesOrExpressed", **kwargs)
class FamilyrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a FamilyrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="familyRelation_role", **kwargs)
class Followedinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Followedinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="followedInSequence", **kwargs)
class Followsinsequencetransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Followsinsequencetransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="followsInSequenceTransitive", **kwargs)
class Followsintime(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Followsintime relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="followsInTime", **kwargs)
class Followsorfollowed(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Followsorfollowed relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="followsOrFollowed", **kwargs)
class Followsproxyinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Followsproxyinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="followsProxyInSequence", **kwargs)
class FunctionalequivalencerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a FunctionalequivalencerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="functionalEquivalenceRelation_role", **kwargs)
class GroupsubdivisionrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a GroupsubdivisionrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="groupSubdivisionRelation_role", **kwargs)
class Hadcomponent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hadcomponent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hadComponent", **kwargs)
class Hadpart(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hadpart relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hadPart", **kwargs)
class Hadsubdivision(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hadsubdivision relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hadSubdivision", **kwargs)
class Hadsubevent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hadsubevent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hadSubevent", **kwargs)
class Hadsubordinate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hadsubordinate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hadSubordinate", **kwargs)
class Hasaccumulationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasaccumulationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasAccumulationDate", **kwargs)
class Hasaccumulator(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasaccumulator relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasAccumulator", **kwargs)
class Hasactivitytype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasactivitytype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasActivityType", **kwargs)
class Hasaddressee(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasaddressee relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasAddressee", **kwargs)
class Hasancestor(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasancestor relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasAncestor", **kwargs)
class Hasauthor(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasauthor relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasAuthor", **kwargs)
class Hasbeginningdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasbeginningdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasBeginningDate", **kwargs)
class Hasbirthdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasbirthdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasBirthDate", **kwargs)
class Hasbirthplace(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasbirthplace relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasBirthPlace", **kwargs)
class Hascarriertype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascarriertype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasCarrierType", **kwargs)
class Haschild(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Haschild relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasChild", **kwargs)
class Hascollector(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascollector relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasCollector", **kwargs)
class Hascomponenttransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascomponenttransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasComponentTransitive", **kwargs)
class Hasconstituentproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasconstituentproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasConstituentProxy", **kwargs)
class Hascontentoftype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascontentoftype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasContentOfType", **kwargs)
class Hascontentwhichmainlyrepresents(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascontentwhichmainlyrepresents relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasContentWhichMainlyRepresents", **kwargs)
class Hascontentwhichrepresents(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascontentwhichrepresents relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasContentWhichRepresents", **kwargs)
class Hascopy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascopy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasCopy", **kwargs)
class Hascreationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascreationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasCreationDate", **kwargs)
class Hascreator(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hascreator relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasCreator", **kwargs)
class Hasdatetype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdatetype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDateType", **kwargs)
class Hasdeathdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdeathdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDeathDate", **kwargs)
class Hasdeathplace(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdeathplace relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDeathPlace", **kwargs)
class Hasderivationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasderivationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDerivationDate", **kwargs)
class Hasdescendant(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdescendant relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDescendant", **kwargs)
class Hasdestructiondate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdestructiondate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDestructionDate", **kwargs)
class Hasdirectcomponent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdirectcomponent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDirectComponent", **kwargs)
class Hasdirectconstituentproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdirectconstituentproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDirectConstituentProxy", **kwargs)
class Hasdirectpart(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdirectpart relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDirectPart", **kwargs)
class Hasdirectsubdivision(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdirectsubdivision relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDirectSubdivision", **kwargs)
class Hasdirectsubevent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdirectsubevent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDirectSubevent", **kwargs)
class Hasdirectsubordinate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdirectsubordinate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDirectSubordinate", **kwargs)
class Hasdocumentaryformtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasdocumentaryformtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasDocumentaryFormType", **kwargs)
class Hasenddate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasenddate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasEndDate", **kwargs)
class Haseventtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Haseventtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasEventType", **kwargs)
class Hasextent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasextent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasExtent", **kwargs)
class Hasextenttype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasextenttype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasExtentType", **kwargs)
class Hasfamilyassociationwith(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasfamilyassociationwith relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasFamilyAssociationWith", **kwargs)
class Hasfamilytype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasfamilytype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasFamilyType", **kwargs)
class Hasgeneticlinktorecordresource(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasgeneticlinktorecordresource relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasGeneticLinkToRecordResource", **kwargs)
class Hasidentifiertype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasidentifiertype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasIdentifierType", **kwargs)
class Hasmigrationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasmigrationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasMigrationDate", **kwargs)
class Hasmodificationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasmodificationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasModificationDate", **kwargs)
class Hasorhadagentname(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadagentname relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAgentName", **kwargs)
class Hasorhadallmemberswithaccumulationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithaccumulationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithAccumulationDate", **kwargs)
class Hasorhadallmemberswithcontenttype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithcontenttype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithContentType", **kwargs)
class Hasorhadallmemberswithcreationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithcreationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithCreationDate", **kwargs)
class Hasorhadallmemberswithdocumentaryformtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithdocumentaryformtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithDocumentaryFormType", **kwargs)
class Hasorhadallmemberswithlanguage(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithlanguage relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithLanguage", **kwargs)
class Hasorhadallmemberswithlegalstatus(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithlegalstatus relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithLegalStatus", **kwargs)
class Hasorhadallmemberswithmainsubject(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithmainsubject relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithMainSubject", **kwargs)
class Hasorhadallmemberswithrecordstate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithrecordstate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithRecordState", **kwargs)
class Hasorhadallmemberswithsubject(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithsubject relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithSubject", **kwargs)
class Hasorhadallmemberswithtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadallmemberswithtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAllMembersWithType", **kwargs)
class Hasorhadanalogueinstantiation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadanalogueinstantiation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAnalogueInstantiation", **kwargs)
class Hasorhadappellation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadappellation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAppellation", **kwargs)
class Hasorhadauthorityover(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadauthorityover relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadAuthorityOver", **kwargs)
class Hasorhadcomponent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadcomponent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadComponent", **kwargs)
class Hasorhadcontroller(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadcontroller relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadController", **kwargs)
class Hasorhadcoordinates(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadcoordinates relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadCoordinates", **kwargs)
class Hasorhadcorporatebodytype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadcorporatebodytype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadCorporateBodyType", **kwargs)
class Hasorhadcorrespondent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadcorrespondent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadCorrespondent", **kwargs)
class Hasorhaddemographicgroup(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhaddemographicgroup relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadDemographicGroup", **kwargs)
class Hasorhadderivedinstantiation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadderivedinstantiation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadDerivedInstantiation", **kwargs)
class Hasorhaddigitalinstantiation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhaddigitalinstantiation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadDigitalInstantiation", **kwargs)
class Hasorhademployer(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhademployer relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadEmployer", **kwargs)
class Hasorhadholder(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadholder relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadHolder", **kwargs)
class Hasorhadidentifier(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadidentifier relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadIdentifier", **kwargs)
class Hasorhadinstantiation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadinstantiation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadInstantiation", **kwargs)
class Hasorhadjurisdiction(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadjurisdiction relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadJurisdiction", **kwargs)
class Hasorhadlanguage(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadlanguage relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadLanguage", **kwargs)
class Hasorhadleader(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadleader relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadLeader", **kwargs)
class Hasorhadlegalstatus(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadlegalstatus relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadLegalStatus", **kwargs)
class Hasorhadlocation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadlocation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadLocation", **kwargs)
class Hasorhadmainsubject(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadmainsubject relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadMainSubject", **kwargs)
class Hasorhadmanager(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadmanager relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadManager", **kwargs)
class Hasorhadmandatetype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadmandatetype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadMandateType", **kwargs)
class Hasorhadmember(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadmember relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadMember", **kwargs)
class Hasorhadmostmemberswithaccumulationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadmostmemberswithaccumulationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadMostMembersWithAccumulationDate", **kwargs)
class Hasorhadmostmemberswithcreationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadmostmemberswithcreationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadMostMembersWithCreationDate", **kwargs)
class Hasorhadname(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadname relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadName", **kwargs)
class Hasorhadoccupationoftype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadoccupationoftype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadOccupationOfType", **kwargs)
class Hasorhadowner(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadowner relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadOwner", **kwargs)
class Hasorhadpart(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadpart relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadPart", **kwargs)
class Hasorhadparticipant(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadparticipant relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadParticipant", **kwargs)
class Hasorhadphysicallocation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadphysicallocation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadPhysicalLocation", **kwargs)
class Hasorhadplacename(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadplacename relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadPlaceName", **kwargs)
class Hasorhadplacetype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadplacetype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadPlaceType", **kwargs)
class Hasorhadposition(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadposition relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadPosition", **kwargs)
class Hasorhadruletype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadruletype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadRuleType", **kwargs)
class Hasorhadsomememberswhosecontentmainlyrepresents(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswhosecontentmainlyrepresents relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWhoseContentMainlyRepresents", **kwargs)
class Hasorhadsomememberswhosecontentrepresents(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswhosecontentrepresents relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWhoseContentRepresents", **kwargs)
class Hasorhadsomememberswithaccumulationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithaccumulationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithAccumulationDate", **kwargs)
class Hasorhadsomememberswithcontenttype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithcontenttype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithContentType", **kwargs)
class Hasorhadsomememberswithcreationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithcreationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithCreationDate", **kwargs)
class Hasorhadsomememberswithdocumentaryformtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithdocumentaryformtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithDocumentaryFormType", **kwargs)
class Hasorhadsomememberswithlanguage(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithlanguage relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithLanguage", **kwargs)
class Hasorhadsomememberswithlegalstatus(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithlegalstatus relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithLegalStatus", **kwargs)
class Hasorhadsomememberswithmainsubject(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithmainsubject relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithMainSubject", **kwargs)
class Hasorhadsomememberswithrecordstate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithrecordstate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithRecordState", **kwargs)
class Hasorhadsomememberswithsubject(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithsubject relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithSubject", **kwargs)
class Hasorhadsomememberswithtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsomememberswithtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSomeMembersWithType", **kwargs)
class Hasorhadspouse(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadspouse relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSpouse", **kwargs)
class Hasorhadstudent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadstudent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadStudent", **kwargs)
class Hasorhadsubdivision(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsubdivision relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSubdivision", **kwargs)
class Hasorhadsubevent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsubevent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSubevent", **kwargs)
class Hasorhadsubject(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsubject relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSubject", **kwargs)
class Hasorhadsubordinate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadsubordinate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadSubordinate", **kwargs)
class Hasorhadteacher(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadteacher relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadTeacher", **kwargs)
class Hasorhadtitle(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadtitle relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadTitle", **kwargs)
class Hasorhadtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadType", **kwargs)
class Hasorhadworkrelationwith(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorhadworkrelationwith relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrHadWorkRelationWith", **kwargs)
class Hasorganicprovenance(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorganicprovenance relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrganicProvenance", **kwargs)
class Hasorganicprovenancedate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasorganicprovenancedate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasOrganicProvenanceDate", **kwargs)
class Hasparttransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasparttransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasPartTransitive", **kwargs)
class Hasproductiontechniquetype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasproductiontechniquetype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasProductionTechniqueType", **kwargs)
class Hasproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasProxy", **kwargs)
class Haspublicationdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Haspublicationdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasPublicationDate", **kwargs)
class Haspublisher(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Haspublisher relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasPublisher", **kwargs)
class Hasreceiver(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasreceiver relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasReceiver", **kwargs)
class Hasrecordsettype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasrecordsettype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasRecordSetType", **kwargs)
class Hasrecordstate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasrecordstate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasRecordState", **kwargs)
class Hasreply(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasreply relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasReply", **kwargs)
class Hasrepresentationtype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasrepresentationtype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasRepresentationType", **kwargs)
class Hassender(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hassender relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasSender", **kwargs)
class Hassibling(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hassibling relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasSibling", **kwargs)
class Hassubdivisiontransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hassubdivisiontransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasSubdivisionTransitive", **kwargs)
class Hassubeventtransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hassubeventtransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasSubeventTransitive", **kwargs)
class Hassubordinatetransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hassubordinatetransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasSubordinateTransitive", **kwargs)
class Hassuccessor(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hassuccessor relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasSuccessor", **kwargs)
class Hastitletype(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hastitletype relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasTitleType", **kwargs)
class Hasunitofmeasurement(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Hasunitofmeasurement relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasUnitOfMeasurement", **kwargs)
class Haswithin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Haswithin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="hasWithin", **kwargs)
class Included(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Included relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="included", **kwargs)
class Includesorincluded(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Includesorincluded relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="includesOrIncluded", **kwargs)
class Includesproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Includesproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="includesProxy", **kwargs)
class Includestransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Includestransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="includesTransitive", **kwargs)
class InstantiationtoinstantiationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a InstantiationtoinstantiationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="instantiationToInstantiationRelation_role", **kwargs)
class IntellectualpropertyrightsrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a IntellectualpropertyrightsrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="intellectualPropertyRightsRelation_role", **kwargs)
class Intersects(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Intersects relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="intersects", **kwargs)
class Isaccumulationdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isaccumulationdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAccumulationDateOf", **kwargs)
class Isaccumulatorof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isaccumulatorof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAccumulatorOf", **kwargs)
class Isactivitytypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isactivitytypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isActivityTypeOf", **kwargs)
class Isaddresseeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isaddresseeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAddresseeOf", **kwargs)
class Isagentassociatedwithagent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isagentassociatedwithagent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAgentAssociatedWithAgent", **kwargs)
class Isagentassociatedwithplace(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isagentassociatedwithplace relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAgentAssociatedWithPlace", **kwargs)
class Isassociatedwithdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isassociatedwithdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAssociatedWithDate", **kwargs)
class Isassociatedwithevent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isassociatedwithevent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAssociatedWithEvent", **kwargs)
class Isassociatedwithplace(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isassociatedwithplace relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAssociatedWithPlace", **kwargs)
class Isassociatedwithrule(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isassociatedwithrule relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAssociatedWithRule", **kwargs)
class Isauthorof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isauthorof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAuthorOf", **kwargs)
class Isauthorizingagentinmandaterelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isauthorizingagentinmandaterelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isAuthorizingAgentInMandateRelation", **kwargs)
class Isbeginningdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isbeginningdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isBeginningDateOf", **kwargs)
class Isbirthdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isbirthdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isBirthDateOf", **kwargs)
class Isbirthplaceof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isbirthplaceof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isBirthPlaceOf", **kwargs)
class Iscarriertypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscarriertypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isCarrierTypeOf", **kwargs)
class Ischildof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Ischildof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isChildOf", **kwargs)
class Iscollectorof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscollectorof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isCollectorOf", **kwargs)
class Iscomponentoftransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscomponentoftransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isComponentOfTransitive", **kwargs)
class Isconstituentofproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isconstituentofproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isConstituentOfProxy", **kwargs)
class Iscontainedbytransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscontainedbytransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isContainedByTransitive", **kwargs)
class Iscontenttypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscontenttypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isContentTypeOf", **kwargs)
class Iscopyof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscopyof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isCopyOf", **kwargs)
class Iscreationdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscreationdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isCreationDateOf", **kwargs)
class Iscreatorof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iscreatorof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isCreatorOf", **kwargs)
class Isdateassociatedwith(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdateassociatedwith relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDateAssociatedWith", **kwargs)
class Isdateassociatedwithrelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdateassociatedwithrelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDateAssociatedWithRelation", **kwargs)
class Isdateofoccurrenceof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdateofoccurrenceof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDateOfOccurrenceOf", **kwargs)
class Isdatetypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdatetypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDateTypeOf", **kwargs)
class Isdeathdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdeathdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDeathDateOf", **kwargs)
class Isdeathplaceof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdeathplaceof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDeathPlaceOf", **kwargs)
class Isderivationdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isderivationdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDerivationDateOf", **kwargs)
class Isdestructiondateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdestructiondateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDestructionDateOf", **kwargs)
class Isdirectcomponentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectcomponentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectComponentOf", **kwargs)
class Isdirectconstituentofproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectconstituentofproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectConstituentOfProxy", **kwargs)
class Isdirectpartof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectpartof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectPartOf", **kwargs)
class Isdirectsubdivisionof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectsubdivisionof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectSubdivisionOf", **kwargs)
class Isdirectsubeventof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectsubeventof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectSubeventOf", **kwargs)
class Isdirectsubordinateto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectsubordinateto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectSubordinateTo", **kwargs)
class Isdirectlycontainedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectlycontainedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectlyContainedBy", **kwargs)
class Isdirectlyincludedin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectlyincludedin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectlyIncludedIn", **kwargs)
class Isdirectlyincludedinproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdirectlyincludedinproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDirectlyIncludedInProxy", **kwargs)
class Isdocumentaryformtypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isdocumentaryformtypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isDocumentaryFormTypeOf", **kwargs)
class Isenddateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isenddateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isEndDateOf", **kwargs)
class Isequivalentto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isequivalentto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isEquivalentTo", **kwargs)
class Iseventassociatedwith(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iseventassociatedwith relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isEventAssociatedWith", **kwargs)
class Iseventtypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iseventtypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isEventTypeOf", **kwargs)
class Isevidencedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isevidencedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isEvidencedBy", **kwargs)
class Isextentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isextentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isExtentOf", **kwargs)
class Isextenttypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isextenttypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isExtentTypeOf", **kwargs)
class Isfamilytypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isfamilytypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isFamilyTypeOf", **kwargs)
class Isfromusedateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isfromusedateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isFromUseDateOf", **kwargs)
class Isfunctionallyequivalentto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isfunctionallyequivalentto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isFunctionallyEquivalentTo", **kwargs)
class Isidentifiertypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isidentifiertypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isIdentifierTypeOf", **kwargs)
class Isincludedinproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isincludedinproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isIncludedInProxy", **kwargs)
class Isincludedintransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isincludedintransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isIncludedInTransitive", **kwargs)
class Isinstantiationassociatedwithinstantiation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isinstantiationassociatedwithinstantiation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isInstantiationAssociatedWithInstantiation", **kwargs)
class Islastupdatedateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Islastupdatedateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isLastUpdateDateOf", **kwargs)
class Ismainthingrepresentedbycontentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Ismainthingrepresentedbycontentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isMainThingRepresentedByContentOf", **kwargs)
class Ismigrationdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Ismigrationdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isMigrationDateOf", **kwargs)
class Ismodificationdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Ismodificationdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isModificationDateOf", **kwargs)
class Isorwasaccumulationdateofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasaccumulationdateofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAccumulationDateOfAllMembersOf", **kwargs)
class Isorwasaccumulationdateofmostmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasaccumulationdateofmostmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAccumulationDateOfMostMembersOf", **kwargs)
class Isorwasaccumulationdateofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasaccumulationdateofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAccumulationDateOfSomeMembersOf", **kwargs)
class Isorwasactiveatdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasactiveatdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasActiveAtDate", **kwargs)
class Isorwasactivitydateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasactivitydateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasActivityDateOf", **kwargs)
class Isorwasadjacentto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasadjacentto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAdjacentTo", **kwargs)
class Isorwasaffectedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasaffectedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAffectedBy", **kwargs)
class Isorwasagentnameof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasagentnameof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAgentNameOf", **kwargs)
class Isorwasanalogueinstantiationof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasanalogueinstantiationof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAnalogueInstantiationOf", **kwargs)
class Isorwasappellationof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasappellationof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAppellationOf", **kwargs)
class Isorwasattendedbystudent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasattendedbystudent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasAttendedByStudent", **kwargs)
class Isorwascomponentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascomponentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasComponentOf", **kwargs)
class Isorwascontainedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascontainedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasContainedBy", **kwargs)
class Isorwascontenttypeofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascontenttypeofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasContentTypeOfAllMembersOf", **kwargs)
class Isorwascontenttypeofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascontenttypeofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasContentTypeOfSomeMembersOf", **kwargs)
class Isorwascontrollerof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascontrollerof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasControllerOf", **kwargs)
class Isorwascoordinatesof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascoordinatesof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasCoordinatesOf", **kwargs)
class Isorwascorporatebodytypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascorporatebodytypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasCorporateBodyTypeOf", **kwargs)
class Isorwascreationdateofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascreationdateofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasCreationDateOfAllMembersOf", **kwargs)
class Isorwascreationdateofmostmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascreationdateofmostmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasCreationDateOfMostMembersOf", **kwargs)
class Isorwascreationdateofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwascreationdateofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasCreationDateOfSomeMembersOf", **kwargs)
class Isorwasdemographicgroupof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasdemographicgroupof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasDemographicGroupOf", **kwargs)
class Isorwasderivedfrominstantiation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasderivedfrominstantiation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasDerivedFromInstantiation", **kwargs)
class Isorwasdescribedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasdescribedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasDescribedBy", **kwargs)
class Isorwasdigitalinstantiationof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasdigitalinstantiationof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasDigitalInstantiationOf", **kwargs)
class Isorwasdocumentaryformtypeofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasdocumentaryformtypeofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasDocumentaryFormTypeOfAllMembersOf", **kwargs)
class Isorwasdocumentaryformtypeofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasdocumentaryformtypeofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasDocumentaryFormTypeOfSomeMembersOf", **kwargs)
class Isorwasemployerof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasemployerof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasEmployerOf", **kwargs)
class Isorwasenforcedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasenforcedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasEnforcedBy", **kwargs)
class Isorwasexpressedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasexpressedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasExpressedBy", **kwargs)
class Isorwasholderof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasholderof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasHolderOf", **kwargs)
class Isorwasidentifierof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasidentifierof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasIdentifierOf", **kwargs)
class Isorwasincludedin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasincludedin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasIncludedIn", **kwargs)
class Isorwasinstantiationof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasinstantiationof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasInstantiationOf", **kwargs)
class Isorwasjurisdictionof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasjurisdictionof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasJurisdictionOf", **kwargs)
class Isorwaslanguageof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslanguageof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLanguageOf", **kwargs)
class Isorwaslanguageofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslanguageofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLanguageOfAllMembersOf", **kwargs)
class Isorwaslanguageofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslanguageofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLanguageOfSomeMembersOf", **kwargs)
class Isorwasleaderof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasleaderof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLeaderOf", **kwargs)
class Isorwaslegalstatusof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslegalstatusof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLegalStatusOf", **kwargs)
class Isorwaslegalstatusofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslegalstatusofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLegalStatusOfAllMembersOf", **kwargs)
class Isorwaslegalstatusofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslegalstatusofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLegalStatusOfSomeMembersOf", **kwargs)
class Isorwaslocationof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslocationof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLocationOf", **kwargs)
class Isorwaslocationofagent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaslocationofagent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasLocationOfAgent", **kwargs)
class Isorwasmainsubjectof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasmainsubjectof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasMainSubjectOf", **kwargs)
class Isorwasmainsubjectofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasmainsubjectofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasMainSubjectOfAllMembersOf", **kwargs)
class Isorwasmainsubjectofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasmainsubjectofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasMainSubjectOfSomeMembersOf", **kwargs)
class Isorwasmainthingrepresentedbycontentofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasmainthingrepresentedbycontentofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasMainThingRepresentedByContentOfSomeMembersOf", **kwargs)
class Isorwasmanagerof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasmanagerof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasManagerOf", **kwargs)
class Isorwasmandatetypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasmandatetypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasMandateTypeOf", **kwargs)
class Isorwasmemberof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasmemberof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasMemberOf", **kwargs)
class Isorwasnameof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasnameof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasNameOf", **kwargs)
class Isorwasoccupationtypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasoccupationtypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasOccupationTypeOf", **kwargs)
class Isorwasoccupiedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasoccupiedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasOccupiedBy", **kwargs)
class Isorwasownerof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasownerof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasOwnerOf", **kwargs)
class Isorwaspartof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwaspartof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasPartOf", **kwargs)
class Isorwasparticipantin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasparticipantin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasParticipantIn", **kwargs)
class Isorwasperformedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasperformedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasPerformedBy", **kwargs)
class Isorwasphysicallocationof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasphysicallocationof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasPhysicalLocationOf", **kwargs)
class Isorwasplacenameof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasplacenameof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasPlaceNameOf", **kwargs)
class Isorwasplacetypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasplacetypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasPlaceTypeOf", **kwargs)
class Isorwasrecordstateofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasrecordstateofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasRecordStateOfAllMembersOf", **kwargs)
class Isorwasrecordstateofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasrecordstateofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasRecordStateOfSomeMembersOf", **kwargs)
class Isorwasregulatedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasregulatedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasRegulatedBy", **kwargs)
class Isorwasrepresentedbycontentofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasrepresentedbycontentofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasRepresentedByContentOfSomeMembersOf", **kwargs)
class Isorwasresponsibleforenforcing(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasresponsibleforenforcing relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasResponsibleForEnforcing", **kwargs)
class Isorwasruletypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasruletypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasRuleTypeOf", **kwargs)
class Isorwassubdivisionof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwassubdivisionof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasSubdivisionOf", **kwargs)
class Isorwassubeventof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwassubeventof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasSubeventOf", **kwargs)
class Isorwassubjectof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwassubjectof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasSubjectOf", **kwargs)
class Isorwassubjectofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwassubjectofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasSubjectOfAllMembersOf", **kwargs)
class Isorwassubjectofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwassubjectofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasSubjectOfSomeMembersOf", **kwargs)
class Isorwassubordinateto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwassubordinateto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasSubordinateTo", **kwargs)
class Isorwastitleof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwastitleof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasTitleOf", **kwargs)
class Isorwastypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwastypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasTypeOf", **kwargs)
class Isorwastypeofallmembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwastypeofallmembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasTypeOfAllMembersOf", **kwargs)
class Isorwastypeofsomemembersof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwastypeofsomemembersof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasTypeOfSomeMembersOf", **kwargs)
class Isorwasunderauthorityof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorwasunderauthorityof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrWasUnderAuthorityOf", **kwargs)
class Isorganicprovenancedateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorganicprovenancedateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrganicProvenanceDateOf", **kwargs)
class Isorganicprovenanceof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isorganicprovenanceof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isOrganicProvenanceOf", **kwargs)
class Ispartoftransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Ispartoftransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isPartOfTransitive", **kwargs)
class Isplaceassociatedwith(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isplaceassociatedwith relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isPlaceAssociatedWith", **kwargs)
class Isplaceassociatedwithagent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isplaceassociatedwithagent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isPlaceAssociatedWithAgent", **kwargs)
class Isproductiontechniquetypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isproductiontechniquetypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isProductionTechniqueTypeOf", **kwargs)
class Ispublicationdateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Ispublicationdateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isPublicationDateOf", **kwargs)
class Ispublisherof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Ispublisherof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isPublisherOf", **kwargs)
class Isreceiverof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isreceiverof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isReceiverOf", **kwargs)
class Isrecordresourceassociatedwithrecordresource(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isrecordresourceassociatedwithrecordresource relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isRecordResourceAssociatedWithRecordResource", **kwargs)
class Isrecordsettypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isrecordsettypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isRecordSetTypeOf", **kwargs)
class Isrecordstateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isrecordstateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isRecordStateOf", **kwargs)
class Isrelatedto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isrelatedto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isRelatedTo", **kwargs)
class Isreplyto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isreplyto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isReplyTo", **kwargs)
class Isrepresentationtypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isrepresentationtypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isRepresentationTypeOf", **kwargs)
class Isrepresentedbycontentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isrepresentedbycontentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isRepresentedByContentOf", **kwargs)
class Isresponsibleforissuing(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isresponsibleforissuing relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isResponsibleForIssuing", **kwargs)
class Isruleassociatedwith(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isruleassociatedwith relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isRuleAssociatedWith", **kwargs)
class Issenderof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Issenderof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isSenderOf", **kwargs)
class Issourceofinformationofrecordresource(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Issourceofinformationofrecordresource relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isSourceOfInformationOfRecordResource", **kwargs)
class Issubdivisionoftransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Issubdivisionoftransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isSubdivisionOfTransitive", **kwargs)
class Issubeventoftransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Issubeventoftransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isSubeventOfTransitive", **kwargs)
class Issubordinatetotransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Issubordinatetotransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isSubordinateToTransitive", **kwargs)
class Issuccessorof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Issuccessorof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isSuccessorOf", **kwargs)
class Istitletypeof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Istitletypeof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isTitleTypeOf", **kwargs)
class Istousedateof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Istousedateof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isToUseDateOf", **kwargs)
class Isunitofmeasurementof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Isunitofmeasurementof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isUnitOfMeasurementOf", **kwargs)
class Iswithin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Iswithin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="isWithin", **kwargs)
class Issuedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Issuedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="issuedBy", **kwargs)
class KnowingofrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a KnowingofrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="knowingOfRelation_role", **kwargs)
class KnowingrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a KnowingrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="knowingRelation_role", **kwargs)
class Knownby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Knownby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="knownBy", **kwargs)
class Knows(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Knows relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="knows", **kwargs)
class Knowsof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Knowsof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="knowsOf", **kwargs)
class LeadershiprelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a LeadershiprelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="leadershipRelation_role", **kwargs)
class Leadershipwithposition(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Leadershipwithposition relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="leadershipWithPosition", **kwargs)
class ManagementrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a ManagementrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="managementRelation_role", **kwargs)
class MandaterelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a MandaterelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="mandateRelation_role", **kwargs)
class MembershiprelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a MembershiprelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="membershipRelation_role", **kwargs)
class Membershipwithposition(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Membershipwithposition relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="membershipWithPosition", **kwargs)
class Migratedfrom(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Migratedfrom relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="migratedFrom", **kwargs)
class Migratedinto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Migratedinto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="migratedInto", **kwargs)
class MigrationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a MigrationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="migrationRelation_role", **kwargs)
class Occupiesoroccupied(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Occupiesoroccupied relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="occupiesOrOccupied", **kwargs)
class Occurredatdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Occurredatdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="occurredAtDate", **kwargs)
class OrganicorfunctionalprovenancerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a OrganicorfunctionalprovenancerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="organicOrFunctionalProvenanceRelation_role", **kwargs)
class OrganicprovenancerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a OrganicprovenancerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="organicProvenanceRelation_role", **kwargs)
class Overlapsoroverlapped(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Overlapsoroverlapped relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="overlapsOrOverlapped", **kwargs)
class OwnershiprelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a OwnershiprelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="ownershipRelation_role", **kwargs)
class PerformancerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a PerformancerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="performanceRelation_role", **kwargs)
class Performsorperformed(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Performsorperformed relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="performsOrPerformed", **kwargs)
class PlacerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a PlacerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="placeRelation_role", **kwargs)
class PositionholdingrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a PositionholdingrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="positionHoldingRelation_role", **kwargs)
class Positioniscontextofleadershiprelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Positioniscontextofleadershiprelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="positionIsContextOfLeadershipRelation", **kwargs)
class Positioniscontextofmembershiprelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Positioniscontextofmembershiprelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="positionIsContextOfMembershipRelation", **kwargs)
class PositiontogrouprelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a PositiontogrouprelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="positionToGroupRelation_role", **kwargs)
class Precededinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Precededinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="precededInSequence", **kwargs)
class Precedesinsequencetransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Precedesinsequencetransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="precedesInSequenceTransitive", **kwargs)
class Precedesintime(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Precedesintime relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="precedesInTime", **kwargs)
class Precedesorpreceded(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Precedesorpreceded relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="precedesOrPreceded", **kwargs)
class Precedesproxyinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Precedesproxyinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="precedesProxyInSequence", **kwargs)
class Proxydirectlyfollowsinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxydirectlyfollowsinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyDirectlyFollowsInSequence", **kwargs)
class Proxydirectlyfollowsproxyinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxydirectlyfollowsproxyinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyDirectlyFollowsProxyInSequence", **kwargs)
class Proxydirectlyincludes(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxydirectlyincludes relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyDirectlyIncludes", **kwargs)
class Proxydirectlyincludesproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxydirectlyincludesproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyDirectlyIncludesProxy", **kwargs)
class Proxydirectlyprecedesinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxydirectlyprecedesinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyDirectlyPrecedesInSequence", **kwargs)
class Proxydirectlyprecedesproxyinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxydirectlyprecedesproxyinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyDirectlyPrecedesProxyInSequence", **kwargs)
class Proxyfollowsinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyfollowsinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyFollowsInSequence", **kwargs)
class Proxyfollowsproxyinsequencetransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyfollowsproxyinsequencetransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyFollowsProxyInSequenceTransitive", **kwargs)
class Proxyfor(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyfor relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyFor", **kwargs)
class Proxyhasconstituent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyhasconstituent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyHasConstituent", **kwargs)
class Proxyhasconstituentproxytransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyhasconstituentproxytransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyHasConstituentProxyTransitive", **kwargs)
class Proxyhasdirectconstituent(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyhasdirectconstituent relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyHasDirectConstituent", **kwargs)
class Proxyhasdirectconstituentproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyhasdirectconstituentproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyHasDirectConstituentProxy", **kwargs)
class Proxyin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIn", **kwargs)
class Proxyinrecord(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyinrecord relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyInRecord", **kwargs)
class Proxyinrecordset(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyinrecordset relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyInRecordSet", **kwargs)
class Proxyincludes(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyincludes relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIncludes", **kwargs)
class Proxyincludesproxytransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyincludesproxytransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIncludesProxyTransitive", **kwargs)
class Proxyisconstituentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisconstituentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsConstituentOf", **kwargs)
class Proxyisconstituentofproxytransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisconstituentofproxytransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsConstituentOfProxyTransitive", **kwargs)
class Proxyisdirectconstituentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisdirectconstituentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsDirectConstituentOf", **kwargs)
class Proxyisdirectconstituentofproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisdirectconstituentofproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsDirectConstituentOfProxy", **kwargs)
class Proxyisdirectlyincludedin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisdirectlyincludedin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsDirectlyIncludedIn", **kwargs)
class Proxyisdirectlyincludedinproxy(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisdirectlyincludedinproxy relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsDirectlyIncludedInProxy", **kwargs)
class Proxyisincludedin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisincludedin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsIncludedIn", **kwargs)
class Proxyisincludedinproxytransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyisincludedinproxytransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyIsIncludedInProxyTransitive", **kwargs)
class Proxyprecedesinsequence(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyprecedesinsequence relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyPrecedesInSequence", **kwargs)
class Proxyprecedesproxyinsequencetransitive(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Proxyprecedesproxyinsequencetransitive relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="proxyPrecedesProxyInSequenceTransitive", **kwargs)
class RecordresourcegeneticrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a RecordresourcegeneticrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="recordResourceGeneticRelation_role", **kwargs)
class Recordresourcehassourceofinformation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Recordresourcehassourceofinformation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="recordResourceHasSourceOfInformation", **kwargs)
class RecordresourceholdingrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a RecordresourceholdingrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="recordResourceHoldingRelation_role", **kwargs)
class RecordresourcetoinstantiationrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a RecordresourcetoinstantiationrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="recordResourceToInstantiationRelation_role", **kwargs)
class RecordresourcetorecordresourcerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a RecordresourcetorecordresourcerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="recordResourceToRecordResourceRelation_role", **kwargs)
class Regulatesorregulated(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Regulatesorregulated relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="regulatesOrRegulated", **kwargs)
class Relationconnects(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Relationconnects relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="relationConnects", **kwargs)
class Relationhascontext(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Relationhascontext relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="relationHasContext", **kwargs)
class Relationhasdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Relationhasdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="relationHasDate", **kwargs)
class Relationhassource(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Relationhassource relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="relationHasSource", **kwargs)
class Relationhastarget(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Relationhastarget relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="relationHasTarget", **kwargs)
class RelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a RelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="relation_role", **kwargs)
class Resultedfromthemergerof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Resultedfromthemergerof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="resultedFromTheMergerOf", **kwargs)
class Resultedfromthesplitof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Resultedfromthesplitof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="resultedFromTheSplitOf", **kwargs)
class Resultsorresultedfrom(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Resultsorresultedfrom relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="resultsOrResultedFrom", **kwargs)
class Resultsorresultedin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Resultsorresultedin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="resultsOrResultedIn", **kwargs)
class Roleiscontextofcreationrelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Roleiscontextofcreationrelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="roleIsContextOfCreationRelation", **kwargs)
class RulerelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a RulerelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="ruleRelation_role", **kwargs)
class SequentialrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a SequentialrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="sequentialRelation_role", **kwargs)
class SiblingrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a SiblingrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="siblingRelation_role", **kwargs)
class SpouserelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a SpouserelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="spouseRelation_role", **kwargs)
class Studiesorstudiedat(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Studiesorstudiedat relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="studiesOrStudiedAt", **kwargs)
class StudyatrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a StudyatrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="studyAtRelation_role", **kwargs)
class TeachingrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a TeachingrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="teachingRelation_role", **kwargs)
class TemporalrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a TemporalrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="temporalRelation_role", **kwargs)
class Thingisconnectedtorelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Thingisconnectedtorelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="thingIsConnectedToRelation", **kwargs)
class Thingiscontextofrelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Thingiscontextofrelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="thingIsContextOfRelation", **kwargs)
class Thingissourceofrelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Thingissourceofrelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="thingIsSourceOfRelation", **kwargs)
class Thingistargetofrelation(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Thingistargetofrelation relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="thingIsTargetOfRelation", **kwargs)
class TyperelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a TyperelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="typeRelation_role", **kwargs)
class Wascomponentof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wascomponentof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasComponentOf", **kwargs)
class Wascontainedby(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wascontainedby relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasContainedBy", **kwargs)
class Wasincludedin(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wasincludedin relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasIncludedIn", **kwargs)
class Waslastupdatedatdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Waslastupdatedatdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasLastUpdatedAtDate", **kwargs)
class Wasmergedinto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wasmergedinto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasMergedInto", **kwargs)
class Waspartof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Waspartof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasPartOf", **kwargs)
class Wassplitinto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wassplitinto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasSplitInto", **kwargs)
class Wassubdivisionof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wassubdivisionof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasSubdivisionOf", **kwargs)
class Wassubeventof(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wassubeventof relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasSubeventOf", **kwargs)
class Wassubordinateto(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wassubordinateto relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasSubordinateTo", **kwargs)
class Wasusedfromdate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wasusedfromdate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasUsedFromDate", **kwargs)
class Wasusedtodate(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a Wasusedtodate relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wasUsedToDate", **kwargs)
class WholepartrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a WholepartrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="wholePartRelation_role", **kwargs)
class WorkrelationRole(Relation):
    """Auto-generated relation class."""

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a WorkrelationRole relation.

        Args:
            src: Source node.
            dst: Destination node.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="workRelation_role", **kwargs)
class HasAccumulationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAccumulationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_ACCUMULATIONRELATION", propagate=True, **kwargs)
class HasActivity(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasActivity weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_ACTIVITY", propagate=True, **kwargs)
class HasActivitydocumentationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasActivitydocumentationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_ACTIVITYDOCUMENTATIONRELATION", propagate=True, **kwargs)
class HasActivitytype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasActivitytype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_ACTIVITYTYPE", propagate=True, **kwargs)
class HasAgent(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAgent weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AGENT", propagate=True, **kwargs)
class HasAgentcontrolrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAgentcontrolrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AGENTCONTROLRELATION", propagate=True, **kwargs)
class HasAgenthierarchicalrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAgenthierarchicalrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AGENTHIERARCHICALRELATION", propagate=True, **kwargs)
class HasAgentname(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAgentname weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AGENTNAME", propagate=True, **kwargs)
class HasAgenttemporalrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAgenttemporalrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AGENTTEMPORALRELATION", propagate=True, **kwargs)
class HasAgenttoagentrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAgenttoagentrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AGENTTOAGENTRELATION", propagate=True, **kwargs)
class HasAppellation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAppellation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_APPELLATION", propagate=True, **kwargs)
class HasAppellationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAppellationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_APPELLATIONRELATION", propagate=True, **kwargs)
class HasAuthorityrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAuthorityrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AUTHORITYRELATION", propagate=True, **kwargs)
class HasAuthorshiprelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasAuthorshiprelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_AUTHORSHIPRELATION", propagate=True, **kwargs)
class HasCarrierextent(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasCarrierextent weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CARRIEREXTENT", propagate=True, **kwargs)
class HasCarriertype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasCarriertype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CARRIERTYPE", propagate=True, **kwargs)
class HasChildrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasChildrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CHILDRELATION", propagate=True, **kwargs)
class HasConcept(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasConcept weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CONCEPT", propagate=True, **kwargs)
class HasContenttype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasContenttype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CONTENTTYPE", propagate=True, **kwargs)
class HasCoordinates(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasCoordinates weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_COORDINATES", propagate=True, **kwargs)
class HasCorporatebody(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasCorporatebody weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CORPORATEBODY", propagate=True, **kwargs)
class HasCorporatebodytype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasCorporatebodytype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CORPORATEBODYTYPE", propagate=True, **kwargs)
class HasCorrespondencerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasCorrespondencerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CORRESPONDENCERELATION", propagate=True, **kwargs)
class HasCreationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasCreationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_CREATIONRELATION", propagate=True, **kwargs)
class HasDate(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasDate weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_DATE", propagate=True, **kwargs)
class HasDatetype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasDatetype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_DATETYPE", propagate=True, **kwargs)
class HasDemographicgroup(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasDemographicgroup weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_DEMOGRAPHICGROUP", propagate=True, **kwargs)
class HasDerivationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasDerivationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_DERIVATIONRELATION", propagate=True, **kwargs)
class HasDescendancerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasDescendancerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_DESCENDANCERELATION", propagate=True, **kwargs)
class HasDocumentaryformtype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasDocumentaryformtype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_DOCUMENTARYFORMTYPE", propagate=True, **kwargs)
class HasEvent(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasEvent weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_EVENT", propagate=True, **kwargs)
class HasEventrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasEventrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_EVENTRELATION", propagate=True, **kwargs)
class HasEventtype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasEventtype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_EVENTTYPE", propagate=True, **kwargs)
class HasExtent(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasExtent weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_EXTENT", propagate=True, **kwargs)
class HasExtenttype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasExtenttype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_EXTENTTYPE", propagate=True, **kwargs)
class HasFamily(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasFamily weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_FAMILY", propagate=True, **kwargs)
class HasFamilyrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasFamilyrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_FAMILYRELATION", propagate=True, **kwargs)
class HasFamilytype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasFamilytype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_FAMILYTYPE", propagate=True, **kwargs)
class HasFunctionalequivalencerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasFunctionalequivalencerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_FUNCTIONALEQUIVALENCERELATION", propagate=True, **kwargs)
class HasGroup(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasGroup weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_GROUP", propagate=True, **kwargs)
class HasGroupsubdivisionrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasGroupsubdivisionrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_GROUPSUBDIVISIONRELATION", propagate=True, **kwargs)
class HasIdentifier(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasIdentifier weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_IDENTIFIER", propagate=True, **kwargs)
class HasIdentifiertype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasIdentifiertype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_IDENTIFIERTYPE", propagate=True, **kwargs)
class HasInstantiation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasInstantiation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_INSTANTIATION", propagate=True, **kwargs)
class HasInstantiationextent(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasInstantiationextent weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_INSTANTIATIONEXTENT", propagate=True, **kwargs)
class HasInstantiationtoinstantiationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasInstantiationtoinstantiationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_INSTANTIATIONTOINSTANTIATIONRELATION", propagate=True, **kwargs)
class HasIntellectualpropertyrightsrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasIntellectualpropertyrightsrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_INTELLECTUALPROPERTYRIGHTSRELATION", propagate=True, **kwargs)
class HasKnowingofrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasKnowingofrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_KNOWINGOFRELATION", propagate=True, **kwargs)
class HasKnowingrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasKnowingrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_KNOWINGRELATION", propagate=True, **kwargs)
class HasLanguage(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasLanguage weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_LANGUAGE", propagate=True, **kwargs)
class HasLeadershiprelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasLeadershiprelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_LEADERSHIPRELATION", propagate=True, **kwargs)
class HasLegalstatus(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasLegalstatus weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_LEGALSTATUS", propagate=True, **kwargs)
class HasManagementrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasManagementrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_MANAGEMENTRELATION", propagate=True, **kwargs)
class HasMandate(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasMandate weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_MANDATE", propagate=True, **kwargs)
class HasMandaterelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasMandaterelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_MANDATERELATION", propagate=True, **kwargs)
class HasMandatetype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasMandatetype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_MANDATETYPE", propagate=True, **kwargs)
class HasMechanism(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasMechanism weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_MECHANISM", propagate=True, **kwargs)
class HasMembershiprelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasMembershiprelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_MEMBERSHIPRELATION", propagate=True, **kwargs)
class HasMigrationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasMigrationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_MIGRATIONRELATION", propagate=True, **kwargs)
class HasName(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasName weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_NAME", propagate=True, **kwargs)
class HasOccupationtype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasOccupationtype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_OCCUPATIONTYPE", propagate=True, **kwargs)
class HasOrganicorfunctionalprovenancerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasOrganicorfunctionalprovenancerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_ORGANICORFUNCTIONALPROVENANCERELATION", propagate=True, **kwargs)
class HasOrganicprovenancerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasOrganicprovenancerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_ORGANICPROVENANCERELATION", propagate=True, **kwargs)
class HasOwnershiprelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasOwnershiprelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_OWNERSHIPRELATION", propagate=True, **kwargs)
class HasPerformancerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPerformancerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PERFORMANCERELATION", propagate=True, **kwargs)
class HasPerson(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPerson weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PERSON", propagate=True, **kwargs)
class HasPhysicallocation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPhysicallocation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PHYSICALLOCATION", propagate=True, **kwargs)
class HasPlace(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPlace weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PLACE", propagate=True, **kwargs)
class HasPlacename(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPlacename weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PLACENAME", propagate=True, **kwargs)
class HasPlacerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPlacerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PLACERELATION", propagate=True, **kwargs)
class HasPlacetype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPlacetype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PLACETYPE", propagate=True, **kwargs)
class HasPosition(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPosition weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_POSITION", propagate=True, **kwargs)
class HasPositionholdingrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPositionholdingrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_POSITIONHOLDINGRELATION", propagate=True, **kwargs)
class HasPositiontogrouprelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasPositiontogrouprelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_POSITIONTOGROUPRELATION", propagate=True, **kwargs)
class HasProductiontechniquetype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasProductiontechniquetype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PRODUCTIONTECHNIQUETYPE", propagate=True, **kwargs)
class HasProxy(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasProxy weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_PROXY", propagate=True, **kwargs)
class HasRecord(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecord weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORD", propagate=True, **kwargs)
class HasRecordpart(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordpart weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDPART", propagate=True, **kwargs)
class HasRecordresource(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordresource weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDRESOURCE", propagate=True, **kwargs)
class HasRecordresourceextent(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordresourceextent weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDRESOURCEEXTENT", propagate=True, **kwargs)
class HasRecordresourcegeneticrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordresourcegeneticrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDRESOURCEGENETICRELATION", propagate=True, **kwargs)
class HasRecordresourceholdingrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordresourceholdingrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDRESOURCEHOLDINGRELATION", propagate=True, **kwargs)
class HasRecordresourcetoinstantiationrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordresourcetoinstantiationrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDRESOURCETOINSTANTIATIONRELATION", propagate=True, **kwargs)
class HasRecordresourcetorecordresourcerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordresourcetorecordresourcerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDRESOURCETORECORDRESOURCERELATION", propagate=True, **kwargs)
class HasRecordset(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordset weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDSET", propagate=True, **kwargs)
class HasRecordsettype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordsettype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDSETTYPE", propagate=True, **kwargs)
class HasRecordstate(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRecordstate weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RECORDSTATE", propagate=True, **kwargs)
class HasRelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RELATION", propagate=True, **kwargs)
class HasRepresentationtype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRepresentationtype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_REPRESENTATIONTYPE", propagate=True, **kwargs)
class HasRoletype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRoletype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_ROLETYPE", propagate=True, **kwargs)
class HasRule(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRule weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RULE", propagate=True, **kwargs)
class HasRulerelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRulerelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RULERELATION", propagate=True, **kwargs)
class HasRuletype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasRuletype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_RULETYPE", propagate=True, **kwargs)
class HasSequentialrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasSequentialrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_SEQUENTIALRELATION", propagate=True, **kwargs)
class HasSiblingrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasSiblingrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_SIBLINGRELATION", propagate=True, **kwargs)
class HasSpouserelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasSpouserelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_SPOUSERELATION", propagate=True, **kwargs)
class HasStudyatrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasStudyatrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_STUDYATRELATION", propagate=True, **kwargs)
class HasTeachingrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasTeachingrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_TEACHINGRELATION", propagate=True, **kwargs)
class HasTemporalrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasTemporalrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_TEMPORALRELATION", propagate=True, **kwargs)
class HasTitle(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasTitle weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_TITLE", propagate=True, **kwargs)
class HasTitletype(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasTitletype weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_TITLETYPE", propagate=True, **kwargs)
class HasType(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasType weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_TYPE", propagate=True, **kwargs)
class HasTyperelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasTyperelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_TYPERELATION", propagate=True, **kwargs)
class HasUnitofmeasurement(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasUnitofmeasurement weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_UNITOFMEASUREMENT", propagate=True, **kwargs)
class HasWholepartrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasWholepartrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_WHOLEPARTRELATION", propagate=True, **kwargs)
class HasWorkrelation(WeakRelation):
    """Auto-generated weak relation class.

    Propagate: True.
    """

    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:
        """Initialize a HasWorkrelation weak relation.

        Args:
            src: Source (parent) node.
            dst: Destination (child) node.
            propagate: Override the default propagation flag.
            **kwargs: Edge properties.
        """
        super().__init__(src=src, dst=dst, rel_type="HAS_WORKRELATION", propagate=True, **kwargs)
