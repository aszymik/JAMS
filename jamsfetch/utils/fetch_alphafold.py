import os
import requests
from Bio.PDB import PDBParser, MMCIFIO

def _pdb_to_cif(pdb_path, cif_path):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_path)
    io = MMCIFIO()
    io.set_structure(structure)
    io.save(cif_path)

def get_alphafold(uniprot_id, output_dir='structures/', format='pdb'):
    """
    Downloads the predicted structure for a UniProt ID from AlphaFold DB.

    Args:
        uniprot_id (str): The UniProt ID (e.g., P12345).
        output_dir (str): Directory to save the downloaded structure.
        format (str): Desired output format: 'pdb' or 'cif'.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdb_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    pdb_path = os.path.join(output_dir, f"{uniprot_id}_AF.pdb")
    cif_path = os.path.join(output_dir, f"{uniprot_id}_AF.cif")

    response = requests.get(pdb_url)
    if response.status_code == 200 and 'HEADER' in response.text:
        with open(pdb_path, 'w') as f:
            f.write(response.text)
        print(f"✅ Downloaded AlphaFold PDB for {uniprot_id} to {pdb_path}")
        
        if format == 'cif':
            _pdb_to_cif(pdb_path, cif_path)
            os.remove(pdb_path)
            print(f"🔄 Converted to CIF and removed original PDB: {cif_path}")
    else:
        print(f"❌ AlphaFold structure not found for UniProt ID: {uniprot_id}")
    
get_alphafold("P12345", output_dir="test_dir", format="cif")