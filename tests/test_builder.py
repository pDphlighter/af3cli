import pytest
import random

from af3cli.builder import InputBuilder
from af3cli.input import InputFile
from af3cli.bond import Atom, Bond
from af3cli.ligand import Ligand, LigandType
from af3cli.sequence import Sequence, SequenceType


@pytest.fixture(scope="module")
def builder():
    return InputBuilder()


@pytest.fixture(scope="module")
def sample_sequence():
    return Sequence(
        seq_type=SequenceType.PROTEIN,
        seq_str="MVKVGVNGFGRIGRLVTRAAFNS"
    )


@pytest.fixture(scope="module")
def sample_ligand():
    return Ligand(
        ligand_type=LigandType.CCD,
        ligand_str="NAC",
    )


@pytest.fixture(scope="module")
def sample_bond():
    atom1 = Atom.from_string("A:1:CA")
    atom2 = Atom.from_string("B:1:CA")
    return Bond(atom1, atom2)


def test_builder_set_name(builder):
    builder.set_name("test")
    assert builder._afinput.name == "test"


@pytest.mark.parametrize("seeds", [
    [1, 2], [1, 2, 3], [random.randint(1, 100) for _ in range(5)]
])
def test_builder_set_seeds(builder, seeds):
    builder.set_seeds(seeds)
    assert builder._afinput.seeds == seeds


def test_builder_set_version(builder):
    builder.set_version(1)
    assert builder._afinput.version == 1


def test_builder_set_dialect(builder):
    builder.set_dialect("alphafold3")
    assert builder._afinput.dialect == "alphafold3"


def test_builder_add_sequence(builder, sample_sequence):
    builder.add_sequence(sample_sequence)
    assert builder._afinput.sequences[0].seq_str == sample_sequence.seq_str
    assert builder._afinput.sequences[0].seq_type == sample_sequence.seq_type


def test_builder_add_ligand(builder, sample_ligand):
    builder.add_ligand(sample_ligand)
    assert builder._afinput.ligands[0].ligand_str == sample_ligand.ligand_str
    assert builder._afinput.ligands[0].ligand_type == sample_ligand.ligand_type


def test_builder_add_bond(builder, sample_bond):
    builder.add_bonded_atom_pair(sample_bond)
    assert builder._afinput.bonded_atoms[0].atom1.eid == sample_bond.atom1.eid
    assert builder._afinput.bonded_atoms[0].atom1.resid == sample_bond.atom1.resid
    assert builder._afinput.bonded_atoms[0].atom1.name == sample_bond.atom1.name
    assert builder._afinput.bonded_atoms[0].atom2.eid == sample_bond.atom2.eid
    assert builder._afinput.bonded_atoms[0].atom2.resid == sample_bond.atom2.resid
    assert builder._afinput.bonded_atoms[0].atom2.name == sample_bond.atom2.name


def test_builder_user_ccd(builder):
    builder.add_user_ccd("ccdString")
    assert builder._afinput.user_ccd == "ccdString"


def test_builder_build(builder):
    afinput = builder.build()
    assert isinstance(afinput, InputFile)
    assert afinput.seeds is not None
    assert len(afinput.sequences) > 0
    assert len(afinput.ligands) > 0
    assert len(afinput.bonded_atoms) > 0
