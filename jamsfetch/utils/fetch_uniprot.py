import os
import requests

def get_uniprot(uniprot_ids, outdir="uniprot_fasta"):
    """
    Fetches the original FASTA sequence from UniProt and saves it to a file.

    Args:
        uniprot_ids (str or list): UniProt ID or list of UniProt IDs (e.g., 'P12345' or ['P12345', 'Q9Y6K9']).
        outdir (str): Directory to save the FASTA file
    """
    base_url = "https://rest.uniprot.org/uniprotkb/"
    os.makedirs(outdir, exist_ok=True)

    if isinstance(uniprot_ids, str):
        uniprot_ids = [uniprot_ids]

    for uniprot_id in uniprot_ids:    
        fasta_url = f"{base_url}{uniprot_id}.fasta"
        response = requests.get(fasta_url)

        if response.status_code == 200:
            fasta_path = os.path.join(outdir, f"{uniprot_id}.fasta")
            with open(fasta_path, "w") as f:
                f.write(response.text)
            print(f"Saved: {fasta_path}")
        else:
            print(f"Error downloading FASTA for {uniprot_id}: status {response.status_code}")