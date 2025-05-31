import time
from fetch_uniprot import get_uniprot

def get_uniprot_batch(ids, output_dir="uniprot_fasta", delay=0.5):
    for uniprot_id in ids:
        get_uniprot(uniprot_id, output_dir)
        time.sleep(delay) 