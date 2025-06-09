import os
from jamsfetch.utils import get_assembly

def test_valid_organism(tmp_path):
    get_assembly(organism="Escherichia coli", output_dir=tmp_path, data_type="genomic", n=1)
    assert len(os.listdir(tmp_path)) > 0

def test_invalid_organism(tmp_path):
    get_assembly(organism="organismus_fakeus", output_dir=tmp_path, data_type="genomic", n=1)
    assert len(os.listdir(tmp_path)) == 0
