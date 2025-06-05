import os
from typing import List
from utils.deconvolute import deconv
from utils.fetch_pdb import get_pdb, download_pdb_files

def fetch_struct(id_list: List[str], output_dir: str):
    """
    Fetches PDB structures only, from a mixed list of IDs.

    Args:
        id_list (List[str]): List of identifiers (can be mixed types).
        output_dir (str): Path to the output directory for PDB files.
    """
    os.makedirs(output_dir, exist_ok=True)
    categorized_ids = deconv(id_list)
    pdb_ids = categorized_ids.get('pdb', [])

    if not pdb_ids:
        print("ℹ️ No valid PDB IDs found.")
        return

    print(f"➡️ Downloading PDB structures for: {' '.join(pdb_ids)}")
    try:
        if download_pdb_files:
            download_pdb_files(pdb_ids, output_dir)
        else:
            for pid in pdb_ids:
                get_pdb(pid, output_dir)
    except Exception as e:
        print(f"❌ PDB fetch failed: {e}")

    print("✅ Finished downloading PDB structures.")


fetch_struct(
    id_list=["P12345", "1ABC", "Q9H9K5", "4HHB", "BAD_ID"],
    output_dir="pdb_structures"
)