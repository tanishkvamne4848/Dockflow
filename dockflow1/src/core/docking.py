import os

from utils.system import run_cmd


def dock(ligand_name, center, config, output_dir):
    """Run AutoDock Vina for a prepared ligand."""
    receptor_pdbqt = os.path.join(output_dir, "receptor", "receptor.pdbqt")
    ligand_pdbqt = os.path.join(output_dir, "ligands", f"{ligand_name}.pdbqt")
    out_pose = os.path.join(output_dir, "docking", f"out_{ligand_name}.pdbqt")
    log_file = os.path.join(output_dir, "logs", f"{ligand_name}.txt")

    size_x = config.get("grid", {}).get("size_x", 20)
    size_y = config.get("grid", {}).get("size_y", 20)
    size_z = config.get("grid", {}).get("size_z", 20)
    exhaustiveness = config.get("vina", {}).get("exhaustiveness", 8)
    num_modes = config.get("vina", {}).get("num_modes", 9)

    cmd = [
        "vina",
        "--receptor", receptor_pdbqt,
        "--ligand", ligand_pdbqt,
        "--center_x", str(center[0]),
        "--center_y", str(center[1]),
        "--center_z", str(center[2]),
        "--size_x", str(size_x),
        "--size_y", str(size_y),
        "--size_z", str(size_z),
        "--exhaustiveness", str(exhaustiveness),
        "--num_modes", str(num_modes),
        "--out", out_pose,
    ]

    run_cmd(cmd, f"Docking failed for {ligand_name}", log_file=log_file)
    return log_file, out_pose
