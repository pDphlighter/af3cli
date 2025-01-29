"""
Example:
Human CDK2 (uniprot entry P24941) in complex with different Ligands
    https://doi.org/10.1016/j.chembiol.2018.10.015
        associated RCSB entries: 6GUB, 6GUC, 6GUE, 6GUF, 6GUH, 6GUK
"""


from af3cli import InputBuilder, ProteinSequence, SMILigand


# CDK2
CDK2_SEQUENCE_STR = (
    "GPGSMENFQKVEKIGEGTYGVVYKARNKLTGEVVALKKIRLDTETEGVPSTAIREISLLKELN"
    "HPNIVKLLDVIHTENKLYLVFEFLHQDLKKFMDASALTGIPLPLIKSYLFQLLQGLAFCHSHR"
    "VLHRDLKPQNLLINTEGAIKLADFGLARAFGVPVRTYTHEVVTLWYRAPEILLGCKYYSTAVD"
    "IWSLGCIFAEMVTRRALFPGDSEIDQLFRIFRTLGTPDEVVWPGVTSMPDYKPSFPKWARQDF"
    "SKVVPPLDEDGRSLLSQMLHYDPNKRISAKAALAHPFFQDVTKPVPHLRL"
)

# Ligand dict, canonical SMILES from OpenEye (OEToolkits)
ligands = {
    "6GUB":"CN1CC[C@@H]([C@H](C1)O)c2c(cc(c3c2OC(=CC3=O)c4ccccc4Cl)O)O",
    "6GUC":"COc1ccc2c(c1)/C(=C/c3cnc[nH]3)/C(=O)N2",
    "6GUE":"Cc1ncc(n1C(C)C)c2ccnc(n2)Nc3ccc(cc3)S(=O)(=O)C",
    "6GUF":"CCn1cnc2c1nc(nc2Nc3cccc(c3)Cl)N[C@@H]4CCCC[C@H]4N",
    "6GUK":"CCn1cnc2c1nc(nc2Nc3cccc(c3)Cl)N[C@@H]4CCCC[C@@H]4N"
}

# Create CDK2 protein sequence object
cdk2_sequence = ProteinSequence(CDK2_SEQUENCE_STR)


for k,v in ligands.items():
    builder = InputBuilder()
    builder.set_name(f"paper_screening_{k}")
    builder.add_sequence(cdk2_sequence)
    builder.add_ligand(SMILigand(v))
    builder.build().write(f"paper_screening_{k}.json")

