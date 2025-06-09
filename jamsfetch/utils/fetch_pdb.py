import os
import requests
import gzip
import shutil
from typing import Union

def get_pdb(
    pdb_ids: Union[str, list],
    output_dir: str = "structures/",
    file_format: str = "pdb",
    unzip: bool = True
):
    """
    Download one or multiple PDB or CIF structure files from the RCSB repository.

    Args:
        pdb_ids (str or list): A single 4-character PDB ID or a list of IDs.
        output_dir (str): Directory to save downloaded files.
        file_format (str): Format of the structure file ('pdb' or 'cif'). Default is 'pdb'.
        unzip (bool): Whether to unzip .gz files after downloading. Default is True.

    Returns:
        None
    """
    if isinstance(pdb_ids, str):
        pdb_ids = [pdb_ids]

    base_url = "https://files.rcsb.org/download"
    os.makedirs(output_dir, exist_ok=True)

    for pdb_id in pdb_ids:
        pdb_id = pdb_id.upper()
        gz_filename = f"{pdb_id}.{file_format}.gz"
        url = f"{base_url}/{gz_filename}"
        gz_path = os.path.join(output_dir, gz_filename)

        try:
            # Download .gz structure file
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(gz_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {gz_filename}")

            # Optionally unzip
            if unzip:
                unzipped_filename = f"{pdb_id}.{file_format}"
                unzipped_path = os.path.join(output_dir, unzipped_filename)
                with gzip.open(gz_path, "rb") as f_in, open(unzipped_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                os.remove(gz_path)
                print(f"Unzipped: {unzipped_filename}")

        except requests.HTTPError as e:
            print(f"Failed to download {url}: {e}")
        except Exception as e:
            print(f"Unexpected error with ID '{pdb_id.upper()}': {e}")

def _map_uniprot_to_pdb(uniprot_id):
    """
    Maps a UniProt ID to associated PDB IDs using UniProt API.

    Returns a list of associated PDB IDs (can be empty).
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        xrefs = data.get('uniProtKBCrossReferences', [])
        pdb_ids = [x['id'].upper() for x in xrefs if x['database'] == 'PDB']
        return pdb_ids
    except Exception as e:
        print(f"❌ Failed to map UniProt ID {uniprot_id} to PDB: {e}")
        return []