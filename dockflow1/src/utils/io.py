import csv
import os


def load_ligands_csv(path):
    """
    Load ligand CSV file.
    Expected format: id,smiles
    """
    ligands = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"Ligand file not found: {path}")

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty")

        if "smiles" not in [col.lower() for col in reader.fieldnames]:
            raise ValueError("CSV must contain 'smiles' column")

        field_map = {col.lower(): col for col in reader.fieldnames}
        smiles_col = field_map["smiles"]
        id_col = field_map.get("id")

        for i, row in enumerate(reader):
            smiles = row.get(smiles_col, "").strip()
            if not smiles:
                continue

            ligand_id = row.get(id_col, "").strip() if id_col else ""
            if not ligand_id:
                ligand_id = f"lig_{i}"

            ligands.append((ligand_id, smiles))

    if not ligands:
        raise ValueError("No valid ligands found in CSV")

    return ligands


def load_existing_results(path):
    if not os.path.exists(path):
        return {}

    existing = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Ligand")
            score = row.get("Best Score")
            if name:
                existing[name] = score
    return existing
