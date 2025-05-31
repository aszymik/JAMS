import os
from typing import List
from pathlib import Path
from utils.deconvolute import deconv
from utils.fetch_assembly import get_assembly
from utils.fetch_pdb import get_pdb, get_pdb_batch
from utils.fetch_uniprot import get_uniprot, get_uniprot_batch

def fetch_fasta(id_list: List[str], output_dir: str):
    """
    Main function that fetches FASTA sequences for a given list of IDs from various databases.

    Args:
        id_list (List[str]): A mixed list of identifiers from different databases.
        output_dir (str): Path to the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    categorized_ids = deconv(id_list)

    uniprot_ids = categorized_ids.get('uniprot', [])
    if uniprot_ids:
        try:
            if get_uniprot_batch:
                get_uniprot_batch(uniprot_ids, output_dir)
            else:
                for uid in uniprot_ids:
                    get_uniprot(uid, output_dir)
        except Exception as e:
            print(f"❌ UniProt fetch failed: {e}")

    pdb_ids = categorized_ids.get('pdb', [])
    if pdb_ids:
        try:
            if get_pdb_batch:
                get_pdb_batch(pdb_ids, output_dir)
            else:
                for pid in pdb_ids:
                    get_pdb(pid, output_dir)
        except Exception as e:
            print(f"❌ PDB fetch failed: {e}")

    nucleotide_ids = categorized_ids.get('nucleotide', [])
    for nid in nucleotide_ids:
        try:
            get_assembly(nid, output_dir)
        except Exception as e:
            print(f"❌ Nucleotide fetch failed for {nid}: {e}")

    assembly_ids = categorized_ids.get('assembly', [])
    for aid in assembly_ids:
        try:
            get_assembly(ids=aid, output_dir=output_dir)
        except Exception as e:
            print(f"❌ Assembly fetch failed for {aid}: {e}")

    print("✅ Finished fetching all FASTA sequences.")
