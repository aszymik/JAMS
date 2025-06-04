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
pip install jams-fetch
```

Co musimy zrobić:
* testowanie - Staszek
* główna funkcja get_structure (póki co wywołuje get_pdb) 
* dodać warning przy złym id - Michał
* ✅ dodać informację, czy sekwencja jest nukleotydowa czy aminokwasowa - Asia (nie dodawałam do pdb, bo ten fragment będzie przenoszony do innej funkcji)
* ✅ argument czy sekwencje nukleotydowe czy aminokwasowe do funkcji get_genome - Asia
* przygotować kod jako paczkę - Ania & Asia
* mapowanie ID - np. z UniProta do PDB (https://github.com/iriziotis/Uniprot-PDB-mapper)
