"""
Example:
Human SIRT2 Histone Deacetylase
    - Protein Data Bank (PDB) Entry: 1J8F
    - Reference: https://www.rcsb.org/structure/1J8F
This simplified demonstration uses one monomer with one associated zinc ion for clarity.

This script provides a Python implementation as an alternative to the af3cli input bash script.
"""

import pprint
from af3cli import InputBuilder, Sequence, SequenceType, Ligand, LigandType

# Define constants
FILENAME = "example_1J8F_python.py"
JOB_NAME = "example_1J8F_py_job"
INPUT_SEQUENCE_TYPE = SequenceType.PROTEIN
INPUT_SEQUENCE_STR = (
    "GEADMDFLRNLFSQTLSLGSQKERLLDELTLEGVARYMQSERCRRVICLVGAGISTSAGIPDFRSPSTGLYDN"
    "LEKYHLPYPEAIFEISYFKKHPEPFFALAKELYPGQFKPTICHYFMRLLKDKGLLLRCYTQNIDTLERIAGLE"
    "QEDLVEAHGTFYTSHCVSASCRHEYPLSWMKEKIFSEVTPKCEDCQSLVKPDIVFFGESLPARFFSCMQSDFL"
    "KVDLLLVMGTSLQVQPFASLISKAPLSTPRLLINKEKAGQSDPFLGMIMGLGGGMDFDSKKAYRDVAWLGECD"
    "QGCLALAELLGWKKELEDLVRREHASIDAQS"
)
LIGAND_TYPE = LigandType.CCD
ZINC_ION_CCD ="ZN"

# Create protein sequence object
sequence = Sequence(seq_type=INPUT_SEQUENCE_TYPE, seq_str=INPUT_SEQUENCE_STR)

# Create ligand object
ligand = Ligand(ligand_type=LIGAND_TYPE, ligand_str=ZINC_ION_CCD)

# Build input configuration for the job
input_builder = InputBuilder()
input_builder.set_name(JOB_NAME)
input_builder.add_sequence(sequence)
input_builder.add_ligand(ligand)
internal_input = input_builder.build()

# Uncomment following line to generate output as JSON file
#internal_input.write(FILENAME)

print_json_via_debug = pprint.PrettyPrinter(indent=4)
print_json_via_debug.pprint(internal_input.to_dict())