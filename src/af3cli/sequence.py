from enum import StrEnum

from .mixin import DictMixin


class SequenceType(StrEnum):
    """
    Represents the types of sequences.

    This enumeration defines constants for types of available sequences
    in the AlphaFold3 input file.
    """
    PROTEIN: str = "protein"
    RNA: str = "rna"
    DNA: str = "dna"


class TemplateType(StrEnum):
    """
    Represents both types of templates that can be used for
    protein sequences.

    Attributes
    ----------
    FILE : str
        Represents a file-based template with an absolute or relative
        path to the input file.
    STRING : str
        Represents a string-based template for inline use of the
        mmCIF file.
    """
    FILE: str = "mmcifPath"
    STRING: str = "mmcif"


class Template(DictMixin):
    """
    Manages structural templates for protein sequences. The `mmcif` attribute
    is either a string or a file path, depending on the template type.

    Attributes
    ----------
    template_type : TemplateType
        The type of template, indicating a string or file-based template.
    mmcif : str
        The mmCIF formatted string of the template or a file path.
    qidx : list of int
        List of query indices that correspond to specific positions in
        the query structure.
    tidx : list of int
        List of template indices that map to the positions in the template
        structure.
    """
    def __init__(
        self,
        template_type: TemplateType,
        mmcif: str,
        qidx: list[int],
        tidx: list[int]
    ):
        self.template_type: TemplateType = template_type
        self.mmcif: str = mmcif
        self.qidx: list[int] = qidx
        self.tidx: list[int] = tidx

    def to_dict(self):
        """
        Converts the attributes of the object into a dictionary representation
        to automatically generate the corresponding fields in the AlphaFold3 input.

        Returns
        -------
        dict
            A dictionary containing key-value pairs derived from the object's
            attributes. The keys can include 'mmcifPath', 'mmcif',
            'queryIndices', and 'templateIndices', depending on the values and
            conditions of the attributes.
        """
        return {
            self.template_type.value: self.mmcif,
            "queryIndices": self.qidx,
            "templateIndices": self.tidx
       }

    def __str__(self) -> str:
        return f"Template({self.template_type.value})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.template_type.name})>"
