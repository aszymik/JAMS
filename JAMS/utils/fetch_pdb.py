import os
import requests
import time

def get_pdb(pdb_id, output_dir, file_format='pdb'):
    """
    Download a PDB or CIF structure file from the RCSB PDB repository.

    Args:
        pdb_id (str): The 4-character PDB ID of the structure to download.
        output_dir (str): The directory where the downloaded file should be saved.
        file_format (str): The format of the structure file ('pdb' or 'cif'). Default is 'pdb'.

    Returns:
        None

    Notes:
        If the download is successful, the file is saved to the specified directory.
        Otherwise, an error message is printed to the console.
    """
    url = f'https://files.rcsb.org/download/{pdb_id.lower()}.{file_format}'
    response = requests.get(url)
    filename = f'{pdb_id.upper()}.{file_format}'
    os.makedirs(output_dir, exist_ok=True)

    if response.status_code == 200:
        with open(f'{output_dir}/{filename}', 'w') as f:
            f.write(response.text)
        print(f'PDB structure saved as {filename}')
    else:
        print(
            f"Failed to download structure for ID '{pdb_id.upper()}'. "
            f'HTTP status code: {response.status_code}'
        )

def get_pdb_batch(ids, output_dir, file_format='pdb', delay=0.5):
    """
    Download multiple PDB or CIF files from the RCSB repository.

    Args:
        ids (list of str): List of 4-character PDB IDs to download.
        output_dir (str): Directory to save the downloaded files.
        file_format (str) Format of the files ('pdb' or 'cif'). Default is 'pdb'.
        delay (float): Number of seconds to wait after each query.

    Returns:
        None
    """
    for pdb_id in ids:
        get_pdb(pdb_id, output_dir, file_format)
        time.sleep(delay) 
