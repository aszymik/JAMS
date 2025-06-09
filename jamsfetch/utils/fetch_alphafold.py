import os
import requests
from Bio.PDB import PDBParser, MMCIFIO

def _pdb_to_cif(pdb_path, cif_path):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_path)
    io = MMCIFIO()
    io.set_structure(structure)
    io.save(cif_path)

def get_alphafold(uniprot_ids, output_dir="structures/", file_format="pdb"):
    """
    Downloads predicted structure(s) from AlphaFold DB.

    Args:
        uniprot_ids (str or list): UniProt ID or list of UniProt IDs (e.g., 'P12345' or ['P12345', 'Q9Y6K9']).
        output_dir (str): Directory to save the downloaded structure(s).
        file_format (str): Desired output file_format: 'pdb' or 'cif'.

    Returns:
        list: List of paths to downloaded structure files (PDB or CIF).
    """
    if isinstance(uniprot_ids, str):
        uniprot_ids = [uniprot_ids]

    os.makedirs(output_dir, exist_ok=True)

    for uniprot_id in uniprot_ids:
        pdb_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
        pdb_path = os.path.join(output_dir, f"{uniprot_id}_AF.pdb")

        try:
            response = requests.get(pdb_url)
            if response.status_code == 200 and 'HEADER' in response.text:
                with open(pdb_path, 'w') as f:
                    f.write(response.text)
                print(f"✅ Downloaded AlphaFold PDB for {uniprot_id} to {pdb_path}")

                if file_format == 'cif':
                    cif_path = os.path.join(output_dir, f"{uniprot_id}_AF.cif")
                    _pdb_to_cif(pdb_path, cif_path)
                    os.remove(pdb_path)
                    print(f"🔄 Converted to CIF and removed original PDB: {cif_path}")

            else:
                print(f"❌ AlphaFold structure not found for UniProt ID: {uniprot_id}")
        except Exception as e:
            print(f"⚠️ Error processing {uniprot_id}: {e}")