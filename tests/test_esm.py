import os
from jamsfetch.utils import get_esm

def test_valid_esm(tmp_path):
    get_esm("MGYP000740062793", output_dir=tmp_path, file_format="pdb")
    files = os.listdir(tmp_path)
    assert any(f.endswith(".pdb") for f in files)

def test_invalid_esm(tmp_path):
    get_esm("BADID", output_dir=tmp_path, file_format="pdb")
    assert len(os.listdir(tmp_path)) == 0
