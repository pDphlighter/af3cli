from .mixin import DictMixin
from .ligand import Ligand
from .bond import Bond
from .sequence import Sequence
from .seqid import IDRegister


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
        self.bonded_atoms: list[Bond] = []
        self.sequences: list[Sequence] = []

        self._id_register: IDRegister = IDRegister()

    def _register_ids(self) -> None:
        """
        Registers unique IDs for sequences and ligands in the internal ID register.

        This method iterates through the objects stored in sequences and ligands,
        checking if each entry is already registered. If an entry is not yet
        registered, it retrieves the associated IDs by calling its `get_id`
        method. Each ID from the returned list is then registered into the
        internal `IDRegister`. Once the IDs are registered, the entry's
        `is_registered` attribute is set to `True`.

        Raises
        ------
        AttributeError
            If an item in sequences or ligands does not have `is_registered` or
            `get_id` attributes.
        """
        for seqtype in [self.sequences, self.ligands]:
            for entry in seqtype:
                if entry.is_registered:
                    continue
                seq_ids = entry.get_id()
                if seq_ids is not None:
                    for seq_id in seq_ids:
                        self._id_register.register(seq_id)
                        entry.is_registered = True


    def _assign_ids(self) -> None:
        """
        Assign unique IDs to sequences and ligands that do not already have an ID.

        This method iterates over sequences and ligands, checking if they have an ID.
        If IDs are missing, it generates unique IDs for entries within each type and
        assigns these IDs.
        """
        for seqtype in [self.sequences, self.ligands]:
            for entry in seqtype:
                if entry.get_id() is None:
                    seq_ids = [self._id_register.generate() for _ in range(entry.num)]
                    entry.set_id(seq_ids)


    def _prepare(self) -> None:
        self._register_ids()
        self._assign_ids()

    def to_dict(self) -> dict:
        pass