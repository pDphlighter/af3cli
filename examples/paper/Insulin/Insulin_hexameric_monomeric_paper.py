import pprint
from af3cli import InputBuilder, ProteinSequence, CCDLigand


insulin_system = InputBuilder()
insulin_system.set_name("insulin_job")
insulin_system.add_sequence(ProteinSequence("GIVEQCCTSICSLYQLENYCN", num=6))
insulin_system.add_sequence(ProteinSequence("FVNQHLCGSHLVEALYLVCGERGFFYTPKA", num=6))
insulin_system.add_ligand(CCDLigand(["ZN"]))

build_json = insulin_system.build()
#build_json.write("insulin.json")

print_json_via_debug = pprint.PrettyPrinter(indent=4)
print_json_via_debug.pprint(build_json.to_dict())