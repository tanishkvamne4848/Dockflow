import os

from pdbfixer import PDBFixer
from openmm.app import PDBFile

from utils.system import run_cmd


def prepare_protein(input_pdb, output_dir):
    """Prepare receptor structure for docking."""
    receptor_dir = os.path.join(output_dir, "receptor")
    os.makedirs(receptor_dir, exist_ok=True)

    clean_pdb = os.path.join(receptor_dir, "clean.pdb")
    receptor_pdbqt = os.path.join(receptor_dir, "receptor.pdbqt")

    fixer = PDBFixer(filename=input_pdb)
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.removeHeterogens(False)
    fixer.addMissingHydrogens(pH=7.4)

    with open(clean_pdb, "w") as f:
        PDBFile.writeFile(fixer.topology, fixer.positions, f)

    run_cmd(
        [
    os.path.expanduser("~/mgltools_x86_64Linux2_1.5.7/bin/pythonsh"),
    os.path.expanduser("~/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py"),
    "-r", clean_pdb,
    "-o", receptor_pdbqt
],
        "Receptor conversion to PDBQT failed",
    )

    return clean_pdb
