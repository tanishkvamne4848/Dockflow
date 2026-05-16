# Dockflow
Automates the lengthy process of docking ligands one at a time with Autodock vina.

DockFlow is an automated molecular docking pipeline for Linux / WSL built around:

- AutoDock Vina
- RDKit
- PDBFixer
- fpocket
- Open Babel

It automates:

1. Protein repair and cleaning
2. Pocket detection
3. Ligand tautomer generation
4. Ligand 3D preparation
5. AutoDock Vina docking
6. Score extraction
7. Full result export
8. Top hit export

MD refinement is intentionally kept manual.

## Features

- CLI command support:
  - `dockflow run`
  - `dockflow check`
- CSV ligand input
- Automatic tautomer generation
- Parallel docking
- Progress bar and step display
- Error-safe execution
- `results.csv` for all ligands
- `top_hits.csv` for best ligands

## Project Structure

```text
dockflow/
├── setup.py
├── requirements.txt
├── config.yaml
├── README.md
│
├── src/
│   ├── cli.py
│   ├── pipeline/
│   │   └── workflow.py
│   ├── utils/
│   │   ├── system.py
│   │   ├── io.py
│   │   ├── logger.py
│   │   └── ranking.py
│   └── core/
│       ├── protein.py
│       ├── pocket.py
│       ├── ligand.py
│       ├── docking.py
│       └── scoring.py
```

## System Requirements

### Python
Recommended:
- Python 3.9+

### Python packages
Installed via:

```bash
pip install -r requirements.txt
```

### System tools (install manually)
Required external tools:

- AutoDock Vina
- Open Babel
- fpocket
- AutoDockTools (`prepare_receptor4.py`)

Example for WSL / Ubuntu:

```bash
sudo apt update
sudo apt install openbabel fpocket
```

Install AutoDock Vina and AutoDockTools separately if not already available.

## Installation

Inside project root:

```bash
bash scripts/install_dockflow.sh
```

Verify installation:

```bash
dockflow --help
dockflow check
```

## Input Files

### Protein
A receptor PDB file, for example:

```text
protein.pdb
```

### Ligands
A CSV file with at least a `smiles` column.

Example:

```csv
id,smiles
lig1,CCO
lig2,CC(=O)O
lig3,c1ccccc1
```

Notes:
- `smiles` column is required
- `id` column is optional
- if `id` is missing, DockFlow auto-generates ligand names

## Run DockFlow

Basic usage:

```bash
dockflow run -pro protein.pdb -lig ligands.csv
```

Custom output folder:

```bash
dockflow run -pro protein.pdb -lig ligands.csv -out results
```

Custom config:

```bash
dockflow run -pro protein.pdb -lig ligands.csv -out results -c config.yaml
```

## Output Structure

Example output folder:

```text
results/
├── receptor/
│   ├── clean.pdb
│   └── receptor.pdbqt
├── ligands/
│   ├── lig_0_t0.pdb
│   ├── lig_0_t0.pdbqt
│   └── ...
├── docking/
│   ├── out_lig_0_t0.pdbqt
│   └── ...
├── logs/
│   ├── lig_0_t0.txt
│   └── ...
├── results.csv
└── top_hits.csv
```

## Important Notes

- Docking score is not proof of biological activity
- More negative score generally indicates stronger predicted binding
- Pocket #1 from fpocket is used by default
- MD refinement is intentionally manual
- Some ligands may fail due to invalid SMILES or failed embedding

## Troubleshooting

### `dockflow: command not found`
Run:

```bash
pip install -e .
```

### `vina not found`
Install AutoDock Vina and ensure it is in your PATH.

### `prepare_receptor4.py not found`
Install AutoDockTools and ensure the script is available in PATH.

### `obabel not found`
Install Open Babel:

```bash
sudo apt install openbabel
```

### `fpocket not found`
Install fpocket:

```bash
sudo apt install fpocket
```
