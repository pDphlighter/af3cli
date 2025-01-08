from enum import StrEnum

from .mixin import DictMixin


class LigandType(StrEnum):
    """
    Enumeration of possible ligand types.

    Attributes
    ----------
    SMILES : str
        Ligand representation using SMILES string notation.
    CCD: str
        Ligand representation using CCD codes.
    """
    SMILES: str = "smiles"
    CCD: str = "ccdCodes"


class Ligand(DictMixin):
    """
    Represents a ligand with associated type.

    Attributes
    ----------
    ligand_str : list of str or str
        The string representation(s) of the ligand.
    ligand_type : LigandType
        The type of the ligand entry.
    """
    def __init__(
        self,
        ligand_type: LigandType,
        ligand_str: list[str] | str,
    ):
        super().__init__(None)
        self.ligand_str: list[str] | str  = ligand_str
        self.ligand_type: LigandType = ligand_type

    def to_dict(self) -> dict:
        pass
