import os
from jamsfetch.utils import get_uniprot

def test_valid_uniprot(tmp_path):
    get_uniprot("P12345", outdir=tmp_path)
    path = tmp_path / "P12345.fasta"
    assert path.exists()
    assert path.read_text().startswith(">")

def test_invalid_uniprot(tmp_path):
    get_uniprot("BADID", outdir=tmp_path)
    assert len(os.listdir(tmp_path)) == 0
