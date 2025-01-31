from af3cli import InputBuilder, SMILigand
from af3cli.__main__ import read_fasta_file

# Ligand dict, canonical SMILES from OpenEye (OEToolkits)
ligands = {
    "6GUB":"CN1CC[C@@H]([C@H](C1)O)c2c(cc(c3c2OC(=CC3=O)c4ccccc4Cl)O)O",
    "6GUC":"COc1ccc2c(c1)/C(=C/c3cnc[nH]3)/C(=O)N2",
    "6GUE":"Cc1ncc(n1C(C)C)c2ccnc(n2)Nc3ccc(cc3)S(=O)(=O)C",
    "6GUF":"CCn1cnc2c1nc(nc2Nc3cccc(c3)Cl)N[C@@H]4CCCC[C@H]4N",
    "6GUK":"CCn1cnc2c1nc(nc2Nc3cccc(c3)Cl)N[C@@H]4CCCC[C@@H]4N"
}

for k,v in ligands.items():
    builder = InputBuilder()
    builder.set_name(f"screening_{k}_job")
    builder.add_sequence(
        read_fasta_file("CDK2.fasta")[0]
    )
    builder.add_ligand(SMILigand(v))
    builder.build().write(f"paper_screening_{k}.json")
