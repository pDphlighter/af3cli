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


class MSA(DictMixin):
    """
    Manages paired and unpaired Multiple Sequence Alignment (MSA) data.
    These are only available for protein and RNA sequences and not for
    DNA sequences. A check will be performed in the `Sequence` class.

    Attributes
    ----------
    paired : str or None
        Paired MSA data or its file path.
    unpaired : str or None
        Unpaired MSA data or its file path.
    paired_is_path : bool
        Indicates whether `paired` represents a file path.
    unpaired_is_path : bool
        Indicates whether `unpaired` represents a file path.
    """
    def __init__(
        self,
        paired: str | None = None,
        unpaired: str | None = None,
        paired_is_path: bool = False,
        unpaired_is_path: bool = False,
    ):
        self.paired: str | None = paired
        self.unpaired: str | None = unpaired
        self.paired_is_path: bool = paired_is_path
        self.unpaired_is_path: bool = unpaired_is_path

    def to_dict(self) -> dict:
        """
        Converts the attributes of the object into a dictionary representation
        to automatically generate the corresponding fields in the AlphaFold3 input.

        Returns
        -------
        dict
            A dictionary containing key-value pairs derived from the object's
            attributes. The keys can include 'pairedMsaPath', 'pairedMsa',
            'unpairedMsaPath', or 'unpairedMsa', depending on the values and
            conditions of the attributes.
        """
        tmp_dict = {}
        if self.paired is not None:
            if self.paired_is_path:
                tmp_dict["pairedMsaPath"] = self.paired
            else:
                tmp_dict["pairedMsa"] = self.unpaired
        if self.unpaired is not None:
            if self.unpaired_is_path:
                tmp_dict["unpairedMsaPath"] = self.unpaired
            else:
                tmp_dict["unpairedMsa"] = self.unpaired
        return tmp_dict

    def __str__(self) -> str:
        display_paired = "paired" if self.paired is not None else ""
        display_unpaired = "unpaired" if self.unpaired is not None else ""
        return f"MSA({display_paired}, {display_unpaired})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
