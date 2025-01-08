import pytest

from af3cli.sequence import SequenceType, Sequence
from af3cli.sequence import TemplateType, Template
from af3cli.sequence import ResidueModification, NucleotideModification
from af3cli.sequence import MSA


@pytest.mark.parametrize("seq_type,seq_type_value", [
    (SequenceType.PROTEIN, "protein"),
    (SequenceType.RNA, "rna"),
    (SequenceType.DNA, "dna")
])
def test_residue_type(seq_type, seq_type_value):
    assert SequenceType(seq_type).value == seq_type_value


@pytest.mark.parametrize("template_type,template_type_value",[
    (TemplateType.STRING, "mmcif"),
    (TemplateType.FILE, "mmcifPath")
])
def test_template_type(template_type, template_type_value):
    assert TemplateType(template_type).value == template_type_value


@pytest.mark.parametrize("template_type,mmcif,qidx,tidx", [
    (TemplateType.STRING, "data_ ...", [1, 2, 3, 4], [4, 6, 7, 8]),
    (TemplateType.FILE, "/path_to_file", [1, 2, 3, 4], [4, 6, 7, 8]),
])
def test_template_init(template_type, mmcif, qidx, tidx):
    template = Template(template_type, mmcif, qidx, tidx)
    assert template.template_type == template_type
    assert template.mmcif == mmcif
    assert template.qidx == qidx
    assert template.tidx == tidx


@pytest.mark.parametrize("template_type,mmcif,qidx,tidx", [
    (TemplateType.STRING, "data_ ...", [1, 2, 3, 4], [4, 6, 7, 8]),
    (TemplateType.FILE, "/path_to_file", [1, 2, 3, 4], [4, 6, 7, 8]),
])
def test_template_to_dict(template_type, mmcif, qidx, tidx):
    template = Template(template_type, mmcif, qidx, tidx)
    tdict = template.to_dict()
    assert isinstance(tdict, dict)
    assert template_type.value in tdict.keys()
    assert "queryIndices" in tdict.keys()
    assert "templateIndices" in tdict.keys()
    assert tdict[template_type.value] == mmcif
    assert tdict["queryIndices"] == qidx
    assert tdict["templateIndices"] == tidx


@pytest.mark.parametrize("mtype,mpos", [
    ("HY3", 1), ("P1L", 5)
])
def test_residue_mod(mtype, mpos):
    modification = ResidueModification(mtype, mpos)
    assert modification.mod_str == mtype
    assert modification.mod_pos == mpos


@pytest.mark.parametrize("mtype,mpos", [
    ("HY3", 1), ("P1L", 5)
])
def test_residue_mod_dict(mtype, mpos):
    modification = ResidueModification(mtype, mpos)
    mdict = modification.to_dict()
    assert isinstance(mdict, dict)
    assert "ptmType" in mdict.keys()
    assert "ptmPosition" in mdict.keys()
    assert mdict["ptmType"] == mtype
    assert mdict["ptmPosition"] == mpos


@pytest.mark.parametrize("mtype,mpos", [
    ("6OG", 1), ("6MA", 2), ("2MG", 5), ("5MC", 10)
])
def test_nucleotide_mod(mtype, mpos):
    modification = NucleotideModification(mtype, mpos)
    assert modification.mod_str == mtype
    assert modification.mod_pos == mpos


@pytest.mark.parametrize("mtype,mpos", [
    ("6OG", 1), ("6MA", 2), ("2MG", 5), ("5MC", 10)
])
def test_nucleotide_mod_dict(mtype, mpos):
    modification = NucleotideModification(mtype, mpos)
    mdict = modification.to_dict()
    assert isinstance(mdict, dict)
    assert "modificationType" in mdict.keys()
    assert "basePosition" in mdict.keys()
    assert mdict["modificationType"] == mtype
    assert mdict["basePosition"] == mpos


@pytest.mark.parametrize("seq_type,seq_str,seq_id,seq_mods",[
    (SequenceType.PROTEIN, "MVKVGVNGF", ["A", "B"],
     [ResidueModification("HY3", 1),
      ResidueModification("P1L", 5)]),
    (SequenceType.RNA, "AUGUGUAU", ["A", "B"], []),
    (SequenceType.DNA, "GACCTCT", None,
     [NucleotideModification("6OG", 1),
      NucleotideModification("6MA", 2)])
])
def test_sequence_init_mod(seq_type, seq_str, seq_id, seq_mods):
    seq = Sequence(seq_type, seq_str, seq_id=seq_id, seq_mod=seq_mods)
    assert seq.seq_type == seq_type
    assert seq.seq_str == seq_str
    assert seq.get_id() == seq_id
    assert seq.seq_mod == seq_mods
    if seq_id is not None:
        assert seq.num == len(seq_id)
    else:
        assert seq.num == 1


@pytest.mark.parametrize("seq_type,seq_str,seq_id,templates",[
    (SequenceType.PROTEIN, "MVKVGVNGF", ["A", "B"],
     [Template(TemplateType.STRING, "data", [1, 2, 3, 4], [4, 6, 7, 8]),
      Template(TemplateType.FILE, "/path", [1, 2, 3, 4], [4, 6, 7, 8])]
    ),
    (SequenceType.PROTEIN, "MVKVGVNGF", ["A", "B"],
     [Template(TemplateType.STRING, "data", [1, 2], [4, 6])]
    ),
])
def test_sequence_init_template(seq_type, seq_str, seq_id, templates):
    seq = Sequence(seq_type, seq_str, seq_id=seq_id, templates=templates)
    assert seq.seq_type == seq_type
    assert seq.seq_str == seq_str
    assert seq.get_id() == seq_id
    assert len(seq.templates) == len(templates)


@pytest.mark.parametrize("paired,unpaired,pispath,unpispath", [
    (None, None, False, False),
    ("test", None, False, False),
    (None, "test", False, False),
    ("test", "test", True, False),
    ("test", "test", False, True),
    ("test", "test", True, True),
])
def test_msa_init(paired, unpaired, pispath, unpispath):
    msa = MSA(paired, unpaired, pispath, unpispath)
    assert msa.paired == paired
    assert msa.unpaired == unpaired
    assert msa.paired_is_path == pispath
    assert msa.unpaired_is_path == unpispath


@pytest.mark.parametrize("paired,unpaired,pispath,unpispath", [
    (None, None, False, False),
    ("test", None, False, False),
    (None, "test", False, False),
    ("test", "test", True, False),
    ("test", "test", False, True),
    ("test", "test", True, True),
])
def test_msa_to_dict(paired, unpaired, pispath, unpispath):
    msa = MSA(paired, unpaired, pispath, unpispath)
    tmp_dict = msa.to_dict()
    if paired is not None:
        if pispath:
            assert "pairedMsaPath" in tmp_dict.keys()
            assert "pairedMsa" not in tmp_dict.keys()
        else:
            assert "pairedMsaPath" not in tmp_dict.keys()
            assert "pairedMsa" in tmp_dict.keys()

    if unpaired is not None:
        if unpispath:
            assert "unpairedMsaPath" in tmp_dict.keys()
            assert "unpairedMsa" not in tmp_dict.keys()
        else:
            assert "unpairedMsaPath" not in tmp_dict.keys()
            assert "unpairedMsa" in tmp_dict.keys()


@pytest.mark.parametrize("seq_type,seq_str,seq_id,msa",[
    (SequenceType.PROTEIN, "MVKVGVNGF", "A", None),
    (SequenceType.PROTEIN, "MVKVGVNGF", ["A", "B"],
     MSA(paired="test")
    ),
    (SequenceType.PROTEIN, "MVKVGVNGF", "A",
     MSA(paired="test", paired_is_path=True)
    ),
    (SequenceType.PROTEIN, "MVKVGVNGF", ["A", "B"],
     MSA(paired="test", unpaired="test")
    ),
    (SequenceType.RNA, "MVKVGVNGF", "C",
     MSA(unpaired="test", unpaired_is_path=True)
    ),
    (SequenceType.PROTEIN, "MVKVGVNGF", ["A"],
     MSA(paired="test", unpaired="test", unpaired_is_path=True)
    ),
    (SequenceType.PROTEIN, "MVKVGVNGF", ["A"],
     MSA(paired="test", unpaired="test", paired_is_path=True, unpaired_is_path=True)
    ),
])
def test_sequence_init_msa(seq_type, seq_str, seq_id, msa):
    seq = Sequence(seq_type, seq_str, seq_id=seq_id, msa=msa)
    assert seq.seq_type == seq_type
    assert seq.seq_str == seq_str
    assert seq.get_id() == seq_id
    tmp_dict = seq.to_dict()[seq_type.value]
    if msa is None:
        assert seq.msa is None
        assert "pairedMsa" not in tmp_dict.keys()
        assert "unpairedMsa" not in tmp_dict.keys()
        return
    if msa.paired_is_path:
        assert "pairedMsaPath" in tmp_dict.keys()
        assert "pairedMsa" not in tmp_dict.keys()
    if msa.unpaired_is_path:
        assert "unpairedMsaPath" in tmp_dict.keys()
        assert "unpairedMsa" not in tmp_dict.keys()
