<p align="center">
    <img src="images/logo.png" alt="" width="50%"/>
</p>

**JAMS-Fetch** (_Joint Automated Multi-source Sequence Fetcher_) is a Python package. It automates the retrieval of sequence and structure data from major bioinformatics databases using a unified, user-friendly interface.

Supported databases:
- **NCBI Nucleotide**
- **NCBI Genome Assembly**
- **UniProt**
- **RCSB PDB**
- **AlphaFold DB**
- **ESM Metagenomic Atlas**

Whether you're working with DNA sequences, protein sequences, or molecular structures, JAMS-Fetch simplifies the download process and saves files in standard formats.

---

## 🚀 Features

- 🧠 Automatically detects the correct source based on ID format.
- ⚙️ Unified API for batch FASTA sequence downloading.
- 🔍 Separate functions for advanced, source-specific queries.
- 💾 Saves sequences and structures in appropriate formats (FASTA, PDB, CIF).
- 📁 Organizes downloads into user-defined directories.

---

## 📦 Installation

```bash
pip install jamsfetch
```

---

### 🚀 Quick Start

Use `fetch_fasta()` to automatically download sequences or structure files from multiple sources with a single list of IDs:

```python
from jamsfetch import fetch_fasta

ids = ["P12345", "NM_001200.2", "GCF_000006945"]
fetch_fasta(
    id_list=ids,
    output_dir="downloads/",
    assembly_data_type="genomic"  # or "protein"
)
```
To download 3D protein structures, either experimentally determined or predicted, use `fetch_structure()`:
```python
from jamsfetch import fetch_structure

ids = ["Q8WXF3", "1A2B"]       # UniProt, PDB and ESM IDs are accepted
fetch_structure(
    id_list=ids,
    output_dir="downloads/",
    file_format="pdb",          # or "cif"
    source="experimental"       # or "predicted"
)
```

## 🔧 Advanced Usage

Use the following source-specific functions when you need greater control over what and how data is downloaded.

### ⛁ Uniprot

Download the original FASTA file(s) from UniProt:

```python
from jamsfetch.utils import get_uniprot

get_uniprot(
    uniprot_ids='P12345',           # specify a single UniProt ID or a list of IDs
    outdir="uniprot_fasta",         # specify output directory for FASTA files
)
```

### ⛁ NCBI Nucleotide
Download nucleotide sequences (e.g. mRNA, genomic fragments) using NCBI accession numbers:
```python
from jamsfetch.utils import get_nucleotide

get_nucleotide(
    record_ids=["NM_001200.2", "NM_000546.6"],  # single ID or list of IDs
    output_dir="nucleotide_fasta/",            # output directory
    email="your_email@example.com",            # required by NCBI E-utilities
    rettype="fasta",                           # 'fasta' for sequence only, or 'gb' for GenBank format
    retmode="text"                             # usually 'text'
)
```
### ⛁ NCBI Genome Assembly

Download genomic or protein data for specific organisms or id(s):

```python
from jamsfetch.utils import get_assembly

get_assembly(
    organism="Homo sapiens",         # specify an organism name
    ids=None,                        # or use specific assembly IDs
    bioproject=None,                 # or BioProject
    output_dir="genomes/",           # specify output directory
    data_type="genomic",             # "genomic" or "protein"
    n=1,                             # if organism was passed, number of genome/proteoms to download
    unzip=True,                  
    reference_only=True              # Only reference genomes if True
)
```

### ⛁ PDB

Download desired protein structures:

```python
from jamsfetch.utils import get_pdb

get_pdb(
    pdb_ids=['1TUP', '9E2J'],       # specify a single ID or a list of IDs
    output_dir="structures/",       # specify output directory
    file_format="pdb",              # or "cif"
    unzip=True                      # whether to unzip or leave .gz files
)
```

### ⛁ AlphaFold DB

Download AlphaFold-predicted protein structures:

```python
from jamsfetch.utils import get_alphafold

get_alphafold(
    uniprot_ids='P12345',           # specify a single ID or a list of IDs
    output_dir="structures/",       # specify output directory
    file_format="pdb",              # or "cif"
)
```

### ⛁ ESM Metagenomic Atlas

Download ESMFold-predicted protein structures:
```python
from jamsfetch.utils import get_esm

get_esm(
    esm_ids='MGYP000740062793',     # specify a single ID or a list of IDs
    output_dir="structures/",       # specify output directory
    file_format="pdb",              # or "cif"
)
```
---
## 🧪 Tests

Optional tests are available in the `tests/` directory. To run them:

```bash
pip install .[test]
pytest
```

This will run a series of integration tests for all supported sources. Invalid IDs are also tested to ensure proper error handling.
