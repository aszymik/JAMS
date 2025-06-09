import os
from typing import List
from .utils.deconvolute import deconv
from .utils.fetch_assembly import get_assembly
from .utils.fetch_pdb import get_pdb, _map_uniprot_to_pdb
from .utils.fetch_uniprot import get_uniprot
from .utils.fetch_nucleotide import get_nucleotide
from .utils.fetch_alphafold import get_alphafold
from .utils.fetch_esm import get_esm

def fetch_fasta(id_list: List[str],
                output_dir: str,
                assembly_data_type: str = "genomic",
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
        print(f"➡️ Downloading amino acid seuqences from Uniprot for: {', '.join(uniprot_ids)}")
        try:
            get_uniprot(uniprot_ids, output_dir)
        except Exception as e:
            print(f"❌ UniProt fetch failed: {e}")

    pdb_ids = categorized_ids.get('pdb', [])
    if pdb_ids:
        print(f"❌ The following IDs are PDB IDs: {', '.join(pdb_ids)}. Please use fetch_structure function to download structures.")

    nucleotide_ids = categorized_ids.get('nucleotide', [])
    if nucleotide_ids:
        print(f"➡️ Downloading nucleotide sequences from NCBI:nucleotide for: {', '.join(nucleotide_ids)}")
        
    for nid in nucleotide_ids:
        try:
            get_nucleotide(record_ids=nid, output_dir=output_dir)
        except Exception as e:
            print(f"❌ Nucleotide fetch failed for {nid}: {e}")

    assembly_ids = categorized_ids.get('assembly', [])
    if assembly_ids: 
        print(f"➡️ Downloading {'proteom(s)' if assembly_data_type == 'protein(s)' else 'genome'} from Genome Assembly for: {', '.join(assembly_ids)}")
    for aid in assembly_ids:
        try:
            get_assembly(ids=aid, output_dir=output_dir, data_type=assembly_data_type)
        except Exception as e:
            print(f"❌ Assembly fetch failed for {aid}: {e}")

    print("✅ Finished fetching all FASTA sequences.")


def fetch_structure(id_list: List[str], 
                    output_dir: str,
                    file_format: str = "pdb",
                    source: str = "experimental",
                    ) -> None:
    """
    Fetches protein structures using mixed list of PDB or UniProt IDs from 
    PDB (experimentally verified structures) or AlphaFold DB (predicted 
    structures).

    Args:
        id_list (List[str]): List of PDB or UniProt identifiers.
        output_dir (str): Directory to store fetched structures.
        file_format (str): Format of the structure file ('pdb' or 'cif'). Default is 'pdb'.
        source (str): Source to get structures from ('experimental'/'exp' for PDB and 
        'predicted'/'pred' for AlphaFold / ESM predicted structures). 
    """
    os.makedirs(output_dir, exist_ok=True)
    categorized_ids = deconv(id_list)
    pdb_ids = set(categorized_ids.get('pdb', []))
    uniprot_ids = categorized_ids.get('uniprot', [])
    esm_ids = categorized_ids.get('esm', [])

    if source.lower() == "experimental" or source.lower() == "exp":
        if esm_ids:
            print(f"ℹ️ {', '.join(esm_ids)} are ESM predicted structures and the chosen source is 'experimental'. If you want to download these structures, specify 'predicted' as source.")

        # Map UniProt to PDB
        for uid in uniprot_ids:
            new_ids = _map_uniprot_to_pdb(uid)
            if new_ids:
                print(f"\nℹ️ {uid} mapped to the following PDB IDs: {', '.join(new_ids)}.")
                pdb_ids.update(new_ids)

        if not pdb_ids:
            print("\nℹ️ No valid PDB IDs (direct or via UniProt) found.")
            return

        print(f"\nDownloading PDB structures for: {', '.join(sorted(pdb_ids))}")
        try:
            get_pdb(sorted(pdb_ids), output_dir, file_format)
        except Exception as e:
            print(f"❌ PDB fetch failed: {e}")

        print("✅ Finished downloading PDB structures.")
    
    elif source.lower() == "predicted" or source.lower() == "pred":
        if pdb_ids:
            print(f"ℹ️ {', '.join(pdb_ids)} are PDB experimental structures and the chosen source is 'predicted'. If you want to download these structures, specify 'experimental' as source.")

        if not uniprot_ids and not esm_ids:
            print("ℹ️ No valid UniProt and ESM IDs found.")
            return
        
        if uniprot_ids:
            try:
                get_alphafold(uniprot_ids, output_dir, file_format)
            except Exception as e:
                print(f"❌ AlphaFold fetch failed: {e}")

        if esm_ids:
            try:
                get_esm(esm_ids, output_dir, file_format)
            except Exception as e:
                print(f"❌ ESM fetch failed: {e}")

    else:
        print(f"❌ Invalid source. Accepted values are experimental (exp) and predicted (pred)")
