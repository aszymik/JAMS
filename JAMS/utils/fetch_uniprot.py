import os
import requests

def get_uniprot(uniprot_id, outdir="uniprot_fasta"):
    """
    Fetches the original FASTA sequence from UniProt and saves it to a file.

    Args:
        uniprot_id (str): UniProt protein ID (e.g. "P12345")
        outdir (str): Directory to save the FASTA file
    """
    base_url = "https://rest.uniprot.org/uniprotkb/"
    fasta_url = f"{base_url}{uniprot_id}.fasta"
    os.makedirs(outdir, exist_ok=True)

    response = requests.get(fasta_url)

    if response.status_code == 200:
        fasta_path = os.path.join(outdir, f"{uniprot_id}.fasta")
        with open(fasta_path, "w") as f:
            f.write(response.text)
        print(f"Saved: {fasta_path}")
    else:
        print(f"Error downloading FASTA for {uniprot_id}: status {response.status_code}")