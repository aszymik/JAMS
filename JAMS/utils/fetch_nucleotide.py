import os
import requests
from typing import List

def get_nucleotide(
    record_id: str,
    email: str,
    rettype: str = "fasta",
    retmode: str = "text",
    output_dir: str = "."
) -> str:
    """
    Download a single nucleotide record from NCBI E-utilities and save to file.

    Args:
        record_id: Accession (e.g. 'NM_001200.2')
        email: Email address required by NCBI
        rettype: Format (e.g. 'fasta', 'gb', 'gbwithparts')
        retmode: Mode ('text' or 'xml')
        output_dir: Directory for saving the file

    Returns:
        Path to the saved file
    """
    return get_nucleotide_batch([record_id], email, rettype, retmode, output_dir)


def get_nucleotide_batch(
    record_ids: List[str],
    email: str,
    rettype: str = "fasta",
    retmode: str = "text",
    output_dir: str = "."
) -> str:
    """
    Download multiple nucleotide records from NCBI E-utilities and save to a single file.

    Args:
        record_ids: List of accessions (e.g. ['NM_001200.2', 'NM_000546.6'])
        email: Email address required by NCBI
        rettype: Format (e.g. 'fasta', 'gb', 'gbwithparts')
        retmode: Mode ('text' or 'xml')
        output_dir: Directory for saving the file

    Returns:
        Path to the saved file
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    ids_str = ",".join(record_ids)
    params = {
        "db": "nucleotide",
        "id": ids_str,
        "rettype": rettype,
        "retmode": retmode,
        "email": email
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)
    ext = "fasta" if rettype == "fasta" else "gb"
    filename = f"{'_'.join(record_ids)[:100]}.{ext}"
    out_path = os.path.join(output_dir, filename)

    with open(out_path, "w") as f:
        f.write(r.text)

    return out_path
