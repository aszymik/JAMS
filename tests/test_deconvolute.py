from jamsfetch.utils.deconvolute import deconv

def test_deconv_classification():
    ids = [
        "P12345",                    # UniProt
        "NM_001200.2",               # NCBI Nucleotide
        "GCF_000001635.27",          # Assembly
        "1TUP",                      # PDB
        "MGYP000740062793",          # ESM
    ]
    result = deconv(ids)
    assert result["uniprot"] == ["P12345"]
    assert result["nucleotide"] == ["NM_001200.2"]
    assert result["assembly"] == ["GCF_000001635.27"]
    assert result["pdb"] == ["1TUP"]
    assert result["esm"] == ["MGYP000740062793"]
