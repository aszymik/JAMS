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
