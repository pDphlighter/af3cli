import pytest

from af3cli.seqid import num_to_letters, IDRegister


@pytest.mark.parametrize("num,letters", [
    (1, "A"), (2, "B"), (3, "C"), (26, "Z"),
    (27, "AA"), (28, "AB"), (52, "AZ"), (53, "BA"),
    (703, "AAA"), (704, "AAB")
])
def test_num_to_letters(num, letters):
    assert num_to_letters(num) == letters


@pytest.fixture(scope="module")
def register():
    return IDRegister()


@pytest.mark.parametrize("letter", [
    "A", "B", "C", "D"
])
def test_id_register(register, letter):
    assert register.generate() == letter


@pytest.mark.parametrize("letter", [
    "F", "G", "H", "I"
])
def test_id_register_fill(register, letter):
    register.register(letter)
    assert letter in register._registered_ids
    assert register._count == 4


@pytest.mark.parametrize("letter", [
    "E", "J", "K", "L", "M"
])
def test_id_register_filled(register, letter):
    assert register.generate() == letter


@pytest.mark.parametrize("letter", [
    "N", "NN", "NNN", "NNNN"
])
def test_id_register_multiple_letters(register, letter):
    register.register(letter)
    assert letter in register._registered_ids
