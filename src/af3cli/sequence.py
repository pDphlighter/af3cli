from enum import StrEnum


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
