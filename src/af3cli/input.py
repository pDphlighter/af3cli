from .mixin import DictMixin
from .ligand import Ligand


class InputFile(DictMixin):
    """
    Represents an input file configuration for an AlphaFold3 job, including
    metadata, sequences and ligands. This class facilitates the preparation
    and conversion of input data to dictionary format for further
    processing or serialization as JSON file.

    Attributes
    ----------
    name : str
        Name of the job.
    version : int
        Version of the input file format.
    dialect : str
        Input file dialect.
    seeds : list of int
        List of seed integers.
    user_ccd : str or None
        Custom CCD structural data provided by the user, if any.
    """
    def __init__(
        self,
        name: str = "job",
        version: int = 1,
        dialect: str = "alphafold3",
        seeds: list[int] | None = None,
        user_ccd: str | None = None,
    ):
        self.name: str = name
        self.version: int = version
        self.dialect: str = dialect
        self.user_ccd: str = user_ccd

        if seeds is None:
            seeds = [1]
        self.seeds: list[int] = seeds

        self.ligands: list[Ligand] = []

    def to_dict(self) -> dict:
        pass
