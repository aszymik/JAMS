import os
from jamsfetch.utils import get_pdb

def test_valid_pdb(tmp_path):
    get_pdb(["1TUP"], output_dir=tmp_path, file_format="pdb", unzip=True)
    files = os.listdir(tmp_path)
    assert any(f.endswith(".pdb") for f in files)

def test_invalid_pdb(tmp_path):
    get_pdb(["XXXX"], output_dir=tmp_path, file_format="pdb", unzip=True)
    assert len(os.listdir(tmp_path)) == 0
