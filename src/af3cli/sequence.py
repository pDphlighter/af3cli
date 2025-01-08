from enum import StrEnum
from abc import ABCMeta

from .mixin import DictMixin
from .exception import AFTemplateError
from .seqid import IDRecord


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


class Modification(DictMixin, metaclass=ABCMeta):
    """
    Represents a modification with specific CCD code and position.

    Attributes
    ----------
    mod_str : str
        The CCD code representing the type or name of the modification.
    mod_pos : int
        The position of the modification within its given context.
    """
    def __init__(self, mod_str: str, mod_pos: int):
        self.mod_str: str = mod_str
        self.mod_pos: int = mod_pos


class ResidueModification(Modification):
    """
    Represents a specific modification at a specific residue position of
    protein sequences.

    Attributes
    ----------
    mod_str : str
        The CCD code representing the type of the modification
        (e.g., phosphorylation, methylation).
    mod_pos : int
        An integer representing the position of the modification
        within the sequence.
    """
    def __init__(self, mod_str: str, mod_pos: int):
        super().__init__(mod_str, mod_pos)

    def to_dict(self):
        return {
            "ptmType": self.mod_str,
            "ptmPosition": self.mod_pos
        }

    def __str__(self) -> str:
        return f"ResidueModification({self.mod_str}, {self.mod_pos})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class NucleotideModification(Modification):
    """
    Represents a specific modification at a specific residue position of
    nucleotide sequences.

    Attributes
    ----------
    mod_str : str
        Type of the nucleotide modification.
    mod_pos : int
        Position of the modification in the nucleotide sequence.
    """
    def __init__(self, mod_str: str, mod_pos: int):
        super().__init__(mod_str, mod_pos)

    def to_dict(self):
        return {
            "modificationType": self.mod_str,
            "basePosition": self.mod_pos
        }

    def __str__(self) -> str:
        return f"NucleotideModification({self.mod_str}, {self.mod_pos})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class Sequence(IDRecord, DictMixin):
    """
    Represents a sequence with templates and modifications.

    The Sequence class is used to store any sequence data with associated
    modifications, templates, and multiple sequence alignment (MSA).
    It provides functionality for validation of sequence attributes,
    This class extends `_IDRecord` to automatically handle sequence IDs.

    Attributes
    ----------
    seq_type : SequenceType
        The type of the sequence (e.g., Protein, DNA, RNA).
    seq_str : str
        The string representation of the sequence.
    msa : MSA or None
        The multiple sequence alignment (MSA) information, if available.
    seq_mod : list of Modification
        Modifications associated with the sequence.
    templates : list of Template
        Templates associated with the sequence. Supported only for protein sequences.
    num : int
        The number of sequences associated with the sequence ID.
    _seq_id : list[str] or None
        The sequence ID(s) associated with the sequence. These can be
        either specified as a list of strings or will be automatically
        assigned by `IDRegister`.
    """
    def __init__(
        self,
        seq_type: SequenceType,
        seq_str: str,
        num: int | None = None,
        seq_id: list[str] | None = None,
        seq_mod: list[Modification] | None = None,
        templates: list[Template] | None = None,
        msa: MSA | None = None,
    ):
        super().__init__(None)
        self.seq_str: str = seq_str
        self.seq_type: SequenceType = seq_type
        self.msa: MSA | None = msa

        if seq_mod is None:
            seq_mod = []
        self.seq_mod: list[Modification] = seq_mod

        if seq_type != SequenceType.PROTEIN and templates is not None:
            raise AFTemplateError("Templates are only supported for proteins.")

        if templates is None:
            templates = []
        self.templates: list[Template] = templates

        # can be overwritten if seq_id is specified
        if num is None:
            self.num: int = 1
        else:
            self.num: int = num

        if seq_id is not None:
            self._seq_id: list[str] = seq_id
            if num is None:
                self.num: int = len(seq_id)
            elif len(seq_id) != num:
                raise ValueError((f"Sequence ID length ({len(seq_id)}) does "
                                  f"not match sequence number ({num})."))

    def to_dict(self) -> dict:
        """
         Convert the object to a dictionary representation.

         This method creates and returns a dictionary representation of the object,
         including its identifier, sequence string, modifications, templates, and,
         the multiple sequence alignment (MSA). It is used to generate the sequence
         entries in the AlphaFold3 input file.

         Returns
         -------
         dict
             A dictionary representation of the object.
         """
        content = dict()
        content["id"] = self.get_id()
        content["sequence"] = self.seq_str
        if len(self.seq_mod):
            content["modifications"] = [m.to_dict() for m in self.seq_mod]
        if len(self.templates):
            content["templates"] = [t.to_dict() for t in self.templates]
        if self.msa is not None:
            content |= self.msa.to_dict()
        return {self.seq_type.value: content}

    def __str__(self) -> str:
        display_template = "T" if len(self.templates) else ""
        display_mod = "M" if len(self.seq_mod) else ""
        display_msa = "MSA" if self.msa is not None else ""
        display_flags = ",".join(
            v for v in [display_template, display_mod, display_msa] if v
        )
        return f"{self.seq_type.name}({len(self.seq_str)})[{display_flags}]"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.seq_type.name})>"