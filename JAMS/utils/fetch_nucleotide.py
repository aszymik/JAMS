import os
import requests

def fetch_ncbi_record(
    record_id: str,
    email: str,
    db: str = "nucleotide",
    rettype: str = "fasta",
    retmode: str = "text",
    output_dir: str = "."
) -> str:
    """
    Download a record from NCBI E-utilities and save to file.

    Args:
        record_id: Accession (e.g. 'NM_001200.2')
        email: Email address required by NCBI
        db: Database (e.g. 'nucleotide', 'protein')
        rettype: Format (e.g. 'fasta', 'gb', 'gbwithparts')
        retmode: Mode ('text' or 'xml')
        output_dir: Directory for saving the file

    Returns:
        Path to the saved file
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": db,
        "id": record_id,
        "rettype": rettype,
        "retmode": retmode,
        "email": email
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)
    ext = "fasta" if rettype == "fasta" else "gb"
    out_path = os.path.join(output_dir, f"{record_id}.{ext}")

    with open(out_path, "w") as f:
        f.write(r.text)

    return out_path
