import requests

pdb_id = '9E2J'
filename = '9E2J.pdb'
file_format = 'pdb'  # pdb or cif

url = f'https://files.rcsb.org/download/{pdb_id.lower()}.{file_format}'
response = requests.get(url)

if response.status_code == 200:
    with open(filename, 'w') as f:
        f.write(response.text)
    print(f'PDB structure saved as {filename}')
else:
    print(f"Failed to download structure for ID '{pdb_id.upper()}'. HTTP status code: {response.status_code}")