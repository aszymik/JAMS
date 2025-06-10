import os
from jamsfetch import fetch_fasta, fetch_structure

def test_fetch_fasta_mixed(tmp_path):
    ids = ["P12345", "NM_001200.2", "GCF_000001635.27"]
    fetch_fasta(id_list=ids, output_dir=tmp_path)

    files = list(tmp_path.iterdir())
    assert len(files) >= 2
    for f in files:
        assert f.exists()
        assert f.stat().st_size > 0

def test_fetch_structure_mixed(tmp_path):
    ids = ["1TUP", "Q8WXF3", "MGYP000740062793"]
    fetch_structure(id_list=ids, output_dir=tmp_path, source="predicted")

    files = list(tmp_path.iterdir())
    assert len(files) >= 2
    for f in files:
        assert f.exists()
        assert f.stat().st_size > 0
