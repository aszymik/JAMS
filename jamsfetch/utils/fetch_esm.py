import os
import requests
from .fetch_alphafold import _pdb_to_cif

def get_esm(esm_ids, output_dir="structures/", file_format="pdb"):
    """
    Downloads predicted protein structure for a given ESM Atlas ID (e.g., MGYP000740062793).

    Args:
        esm_ids (str or list): ESM Atlas ID or list of ESM Atlas IDs (must start with 'MGYP').
        output_dir (str): Directory to save the downloaded .pdb files.
        file_format (str): Desired output file_format: 'pdb' or 'cif'.
    """
    if isinstance(esm_ids, str):
        esm_ids = [esm_ids]

    os.makedirs(output_dir, exist_ok=True)

    for esm_id in esm_ids:

        if not esm_id.startswith("MGYP"):
            print(f"❌ Invalid ESM Atlas ID: {esm_id}")

        os.makedirs(output_dir, exist_ok=True)
        pdb_path = os.path.join(output_dir, f"{esm_id}.pdb")

        url = f"https://api.esmatlas.com/fetchPredictedStructure/{esm_id}.pdb"

        try:
            print(f"⬇️ Downloading ESM structure for {esm_id}...")
            r = requests.get(url, allow_redirects=True, timeout=30)
            r.raise_for_status()

            # Write to file
            with open(pdb_path, "wb") as f:
                f.write(r.content)
            print(f"✅ Downloaded ESM structure for {esm_id} to {pdb_path}")

            if file_format == 'cif':
                cif_path = os.path.join(output_dir, f"{esm_id}.cif")
                _pdb_to_cif(pdb_path, cif_path)
                os.remove(pdb_path)
                print(f"🔄 Converted to CIF and removed original PDB: {cif_path}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download {esm_id}: {e}")