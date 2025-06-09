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

        try:
            response = requests.get(fasta_url, timeout=10)
            response.raise_for_status()  # raise HTTPError for bad responses

            fasta_path = os.path.join(outdir, f"{uniprot_id}.fasta")
            with open(fasta_path, "w") as f:
                f.write(response.text)
            print(f"Saved: {fasta_path}")

        except requests.exceptions.HTTPError:
            print(f"Could not download FASTA for {uniprot_id}: issue on the database side, please check the ID or try again later.")
        except requests.exceptions.RequestException:
            print(f"Network issue occurred while downloading {uniprot_id}, please try again later.")
        except Exception:
            print(f"An unexpected error occurred for {uniprot_id}, please try again later.")