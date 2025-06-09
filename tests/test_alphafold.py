import os
from jamsfetch.utils import get_alphafold

def test_valid_alphafold(tmp_path):
    get_alphafold("Q8WXF3", output_dir=tmp_path, file_format="pdb")
    files = os.listdir(tmp_path)
    assert any(f.endswith(".pdb") for f in files)

def test_invalid_alphafold(tmp_path):
    get_alphafold("INVALID", output_dir=tmp_path, file_format="pdb")
    assert len(os.listdir(tmp_path)) == 0
