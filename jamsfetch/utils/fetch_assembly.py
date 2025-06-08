import requests
import warnings
import os
import subprocess
import gzip

def get_assembly(
        organism=None,
        ids=None,
        bioproject=None,
        output_dir="data/",
        data_type="genomic", # genomic or protein
        n=1,
        unzip=True,
        reference_only=False
    ):
    reports = _get_reports(
        organism=organism,
        ids=ids,
        bioproject=bioproject,
        n=n,
        reference_only=reference_only,
    )
    if n > len(reports): warnings.warn(f"{n=} higher then number of avaible genomes, {len(reports)} will be downoaded")
    
    if organism:
        reports = reports[:n]

    os.makedirs(output_dir, exist_ok=True)
    for r in reports:
        query, filename = _build_query(_get_ids(r), data_type)
        download_command = f"wget {query} -P {output_dir}"

        try:
            subprocess.run(download_command.split(), check=True)

            if filename.endswith(".gz") and unzip == True:
                with gzip.open(f"{output_dir}/{filename}", "rb") as zip_f:
                    content = zip_f.read().decode("utf-8")
                    with open(f"{output_dir}/{filename}.fasta", "w") as unzip_f:
                        unzip_f.write(content)

                os.remove(f"{output_dir}/{filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during download or unzip: {e}")
    

def _get_reports(
        organism=None,
        ids=None,
        bioproject=None,
        n=1,
        reference_only=False,
    ):

    assert any([organism, ids, bioproject]), "No identifier was passed, please pass either id(s), organism, gcf,gca or bioproject id"

    reference_only = "true" if reference_only else "false"
    if organism:
        query = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/{organism}/dataset_report?filters.reference_only={reference_only}&page_size={n}"
    elif ids:
        if isinstance(ids, str):
            ids = ids.replace("GCA", "GCF")
        elif isinstance(ids, list):
            ids = '%2C'.join([i.replace("GCA", "GCF") for i in ids])
        query = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/{ids}/dataset_report?filters.reference_only={reference_only}"
    elif bioproject:
        if isinstance(bioproject, list):
            bioproject = '%2C'.join(bioproject)
        query = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/bioproject/{bioproject}/dataset_report?filters.reference_only={reference_only}&filters.assembly_source=refseq"


    response = requests.get(query)
    assert response.status_code == 200, f"Unsuccessful connection, status code: {response.status_code}"

    metadata_json = response.json()

    return  metadata_json['reports']


def _get_ids(report):
        assert report.get('assembly_info', {}).get('assembly_name', None) is not None, "assembly_name name is missing"

        return {
        'GCF': report.get('accession'),
        'GCA': report.get('paired_accession'),
        'Assembly_Name': report.get('assembly_info', {}).get('assembly_name', None),
        'BioProject': report.get('assembly_info', {}).get('bioproject_accession', None),
    }

def _build_query(id_dict, mode):

    ext = "fna" if mode == "genomic" else "faa"

    query_base = "https://ftp.ncbi.nlm.nih.gov/genomes/all/"
    record = f"{id_dict['GCF'][:3]}/{id_dict['GCF'][4:7]}/{id_dict['GCF'][7:10]}/{id_dict['GCF'][10:13]}/{id_dict['GCF']}_{id_dict['Assembly_Name']}/"
    protein_filename = f"{id_dict['GCF']}_{id_dict['Assembly_Name']}_{mode}.{ext}.gz"

    return query_base + record + protein_filename, protein_filename
