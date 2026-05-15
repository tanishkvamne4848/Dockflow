import os
import logging

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

from utils.system import run_cmd


def generate_tautomers(smiles, max_tautomers=3):
    """Generate top-ranked tautomers for a ligand SMILES."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []

    enumerator = rdMolStandardize.TautomerEnumerator()
    tautomers = list(enumerator.Enumerate(mol))

    scored = []
    for tautomer in tautomers:
        try:
            score = enumerator.ScoreTautomer(tautomer)
            scored.append((score, tautomer))
        except Exception:
            continue

    scored.sort(reverse=True, key=lambda x: x[0])
    return [mol for _, mol in scored[:max_tautomers]]


def prepare_ligands(smiles, base_name, config, output_dir):
    """Prepare dockable ligand files from a SMILES string."""
    ligand_dir = os.path.join(output_dir, "ligands")
    os.makedirs(ligand_dir, exist_ok=True)

    max_tautomers = config.get("ligand", {}).get("max_tautomers", 3)
    tautomers = generate_tautomers(smiles, max_tautomers=max_tautomers)
    ligand_names = []

    for i, mol in enumerate(tautomers):
        try:
            mol = Chem.AddHs(mol)
            embed_status = AllChem.EmbedMolecule(mol, randomSeed=42)
            if embed_status != 0:
                raise ValueError("3D embedding failed")

            try:
                AllChem.UFFOptimizeMolecule(mol)
            except Exception:
                logging.warning(f"UFF optimization failed for {base_name}_t{i}")

            ligand_name = f"{base_name}_t{i}"
            pdb_path = os.path.join(ligand_dir, f"{ligand_name}.pdb")
            pdbqt_path = os.path.join(ligand_dir, f"{ligand_name}.pdbqt")

            Chem.MolToPDBFile(mol, pdb_path)
            run_cmd(
                ["obabel", pdb_path, "-O", pdbqt_path],
                f"Ligand conversion failed for {ligand_name}",
            )
            ligand_names.append(ligand_name)
        except Exception as e:
            logging.error(f"Ligand preparation failed for {base_name}_t{i}: {e}")

    return ligand_names
