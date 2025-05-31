import re

def deconv(id_list):
    """
    Rozdziela listę identyfikatorów na listy odpowiadające bazom danych:
    UniProt, PDB, Nucleotide (GenBank + RefSeq), Assembly

    Args:
        id_list (list of str): Mieszana lista identyfikatorów

    Returns:
        dict: Słownik z kluczami 'uniprot', 'pdb', 'nucleotide', 'assembly', 'unknown'
    """
    result = {
        'uniprot': [],
        'pdb': [],
        'nucleotide': [],
        'assembly': [],
        'unknown': []
    }

    for _id in id_list:
        if re.fullmatch(r"[OPQ][0-9][A-Z0-9]{3}[0-9]", _id) or re.fullmatch(r"[A-NR-Z][0-9]{5}", _id):
            result['uniprot'].append(_id)
        elif re.fullmatch(r"[A-Za-z0-9]{4}", _id):
            result['pdb'].append(_id)
        elif _id.startswith("GCF_") or _id.startswith("GCA_"):
            result['assembly'].append(_id)
        elif re.fullmatch(r"(?:[A-Z]{2}_[0-9]+(?:\.[0-9]+)?)|(?:[A-Z]{1,2}[0-9]{5,6}(?:\.[0-9]+)?)", _id):
            result['nucleotide'].append(_id)
        else:
            result['unknown'].append(_id)

    return result

test_ids = [
    "P01308",        # UniProt
    "Q8N158",        # UniProt
    "1A2B",          # PDB
    "4HHB",          # PDB
    "NM_000546",     # Nucleotide
    "NC_000001.11",  # Nucleotide
    "XM_123456",     # Nucleotide (RefSeq)
    "U49845",        # Nucleotide (GenBank)
    "AY123456.1",    # Nucleotide (GenBank z wersją)
    "GCF_000001405.39",  # Assembly
    "GCA_000001635.9",   # Assembly
    "M12345.1",
    "XYZ1234",       # ❌ Niepoprawny
    "123",           # ❌ Za krótki
    "ABCD5",         # ❌ Nieregularny
    "NM_ABCDE",      # ❌ Błędny Nucleotide
]

sorted_ids = deconv(test_ids)

for category, ids in sorted_ids.items():
    print(f"{category.upper()}: {ids}")
