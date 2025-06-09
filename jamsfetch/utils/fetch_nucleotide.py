import os
import requests
from typing import Union, List

def get_nucleotide(
    record_ids: Union[str, List[str]],
    output_dir: str = ".",
    email: str = "",
    rettype: str = "fasta",
    retmode: str = "text",
) -> str:
    """
    Fetch nucleotide sequence(s) from NCBI and save to file.

    Args:
        record_ids: Accession or list of accessions (e.g. 'NM_001200.2' or ['NM_001200.2', 'NM_000546.6'])
        email: Email address required by NCBI
        rettype: Format ('fasta', 'gb', etc.)
        retmode: Mode ('text' or 'xml')
        output_dir: Output directory

    Returns:
        Path to the saved file
    """
    if isinstance(record_ids, str):
        record_ids = [record_ids]

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nucleotide",
        "id": ",".join(record_ids),
        "rettype": rettype,
        "retmode": retmode,
        "email": email,
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)
    ext = "fasta" if rettype == "fasta" else rettype
    filename = f"{'_'.join(record_ids)[:100]}.{ext}"
    out_path = os.path.join(output_dir, filename)

    with open(out_path, "w") as f:
        f.write(r.text)

    return out_path
