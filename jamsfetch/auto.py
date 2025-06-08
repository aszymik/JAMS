import os
from typing import List
from .utils.deconvolute import deconv
from .utils.fetch_assembly import get_assembly
from .utils.fetch_pdb import get_pdb, download_pdb_files
from .utils.fetch_uniprot import get_uniprot, get_uniprot_batch

def fetch_fasta(id_list: List[str],
                output_dir: str,
                assembly_data_type:str="genomic",
                ) -> None:
    """
    Main function that fetches FASTA sequences for a given list of IDs from various databases.

    Args:
        id_list (List[str]): A mixed list of identifiers from different databases.
        output_dir (str): Path to the output directory.
        assembly_data_type (str): Data type to download from Genome assembly. Either genomic or portein.
        Allows to specify if user wants to download genome or proteom.
    """
    assert assembly_data_type in ['genomic', 'protein'], f"assembly_data_type parameter need to be either genomic or protein. Got {assembly_data_type}"
    os.makedirs(output_dir, exist_ok=True)
    categorized_ids = deconv(id_list)

    uniprot_ids = categorized_ids.get('uniprot', [])
    if uniprot_ids:
        print(f"➡️ Downloading amino acid seuqences from Uniprot for: {" ".join(uniprot_ids)}")
        try:
            if get_uniprot_batch:
                get_uniprot_batch(uniprot_ids, output_dir)
            else:
                for uid in uniprot_ids:
                    get_uniprot(uid, output_dir)
        except Exception as e:
            print(f"❌ UniProt fetch failed: {e}")

    pdb_ids = categorized_ids.get('pdb', [])
    if pdb_ids:
        try:
            if download_pdb_files:
                download_pdb_files(pdb_ids, output_dir)
            else:
                for pid in pdb_ids:
                    get_pdb(pid, output_dir)
        except Exception as e:
            print(f"❌ PDB fetch failed: {e}")

    nucleotide_ids = categorized_ids.get('nucleotide', [])
    if nucleotide_ids:
        print(f"➡️ Downloading nucleotide sequences from NCBI:nucleotide for: {" ".join(nucleotide_ids)}")
    for nid in nucleotide_ids:
        try:
            get_assembly(nid, output_dir)
        except Exception as e:
            print(f"❌ Nucleotide fetch failed for {nid}: {e}")

    assembly_ids = categorized_ids.get('assembly', [])
    if assembly_ids: 
        print(f"➡️ Downloading {'proteom(s)' if assembly_data_type == "protein(s)" else "genome"} from Genome Assembly for: {" ".join(assembly_ids)}")
    for aid in assembly_ids:
        try:
            get_assembly(ids=aid, output_dir=output_dir, data_type=assembly_data_type)
        except Exception as e:
            print(f"❌ Assembly fetch failed for {aid}: {e}")

    print("✅ Finished fetching all FASTA sequences.")


def fetch_struct(id_list: List[str], output_dir: str):
    """
    Fetches PDB structures only, from a mixed list of IDs.

    Args:
        id_list (List[str]): List of identifiers (can be mixed types).
        output_dir (str): Path to the output directory for PDB files.
    """
    os.makedirs(output_dir, exist_ok=True)
    categorized_ids = deconv(id_list)
    pdb_ids = categorized_ids.get('pdb', [])

    if not pdb_ids:
        print("ℹ️ No valid PDB IDs found.")
        return

    print(f"➡️ Downloading PDB structures for: {' '.join(pdb_ids)}")
    try:
        if download_pdb_files:
            download_pdb_files(pdb_ids, output_dir)
        else:
            for pid in pdb_ids:
                get_pdb(pid, output_dir)
    except Exception as e:
        print(f"❌ PDB fetch failed: {e}")

    print("✅ Finished downloading PDB structures.")
