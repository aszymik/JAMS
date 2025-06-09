import os
from jamsfetch.utils import get_nucleotide

def test_valid_ncbi_id(tmp_path):
    result = get_nucleotide("NM_001200.2", output_dir=tmp_path, email="test@example.com")
    assert result is not None
    assert os.path.exists(result)
    assert open(result).read().startswith(">")

def test_invalid_ncbi_id(tmp_path):
    result = get_nucleotide("INVALID_ID", output_dir=tmp_path, email="test@example.com")
    assert result is None
