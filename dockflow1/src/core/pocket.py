import os

from utils.system import run_cmd


def detect_pocket(clean_pdb, output_dir):
    """Detect binding pocket using fpocket and calculate center coordinates."""
    receptor_dir = os.path.join(output_dir, "receptor")
    run_cmd(["fpocket", "-f", clean_pdb], "fpocket failed")

    base_name = os.path.splitext(os.path.basename(clean_pdb))[0]
    pocket_file = os.path.join(receptor_dir, f"{base_name}_out", "pockets", "pocket1_atm.pdb")

    if not os.path.exists(pocket_file):
        raise FileNotFoundError(f"Pocket file not found: {pocket_file}")

    x = y = z = n = 0
    with open(pocket_file) as f:
        for line in f:
            if line.startswith("ATOM"):
                parts = line.split()
                x += float(parts[6])
                y += float(parts[7])
                z += float(parts[8])
                n += 1

    if n == 0:
        raise ValueError("No atoms found in detected pocket")

    return (x / n, y / n, z / n)
