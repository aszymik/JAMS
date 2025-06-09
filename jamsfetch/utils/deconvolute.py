import re

def deconv(id_list, verbose=True):
    """
    Splits a list of identifiers into sublists corresponding to different biological databases:
    UniProt, PDB, Nucleotide (GenBank + RefSeq), Assembly

    Args:
        id_list (list of str): A mixed list of biological identifiers.

    Returns:
        dict: A dictionary with the keys 'uniprot', 'pdb', 'nucleotide', 'assembly', 'esm' and 
              'unknown', each containing a list of matching IDs. Also prints a warning for 
              unrecognized IDs and displays sorted identifiers by category.
    """

    result = {
        'uniprot': [],
        'pdb': [],
        'nucleotide': [],
        'assembly': [],
        'esm': [],
        'unknown': []
    }

    for _id in id_list:
        if re.fullmatch(r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}", _id) or re.fullmatch(r"[A-NR-Z][0-9]{5}", _id):
            result['uniprot'].append(_id)
        elif re.fullmatch(r"[A-Za-z0-9]{4}", _id):
            result['pdb'].append(_id)
        elif _id.startswith("GCF_") or _id.startswith("GCA_"):
            result['assembly'].append(_id)
        elif re.fullmatch(r"(?:[A-Z]{2}_[0-9]+(?:\.[0-9]+)?)|(?:[A-Z]{1,2}[0-9]{5,6}(?:\.[0-9]+)?)", _id):
            result['nucleotide'].append(_id)
        elif re.fullmatch(r"MGYP[0-9]{9,}", _id):
            result['esm'].append(_id)
        else:
            result['unknown'].append(_id)

    if result['unknown']:
        print("⚠️ Warning: The following identifiers do not match any known format and will not be processed:")
        for uid in sorted(result['unknown']):
            print(f"  - {uid}")
            
    if verbose:
        print("\n📋 Sorted identifiers by category:")
        for category, ids in result.items():
            if category != "unknown":
                print(f"\n{category.capitalize()} ({len(ids)}):")
                for uid in sorted(ids):
                    print(f"  - {uid}")

    return result

