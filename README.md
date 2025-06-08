# 🧬 JAMS-Fetch

**JAMS-Fetch** (_Joint Automated Multi-source Sequence Fetcher_) is a Python package. It automates the retrieval of sequence and structure data from major bioinformatics databases using a unified, user-friendly interface.

Supported databases:
- **NCBI Nucleotide**
- **NCBI Genome Assembly**
- **UniProt**
- **RCSB PDB**

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

ids = ["P12345", "NM_001200.2", "1A2B", "GCF_000001405.39"]
fetch_fasta(
    id_list=ids,
    output_dir="downloads/",
    assembly_data_type="genomic"  # or "protein"
)
```

## 🔧 Advanced Usage

Use the following source-specific functions when you need greater control over what and how data is downloaded.

### ⛁ Uniprot

### ⛁ NCBI Nucleotide

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

---
Upcoming capabilities:
* Testing - Staszek
* UniProta to PDB mapping (https://github.com/iriziotis/Uniprot-PDB-mapper)
