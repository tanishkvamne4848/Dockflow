import argparse
import os
from pipeline.workflow import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        prog="dockflow",
        description="Automated molecular docking pipeline (Vina + RDKit + PDBFixer)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run docking pipeline")
    run_parser.add_argument("-pro", "--protein", required=True, help="Path to protein PDB file")
    run_parser.add_argument("-lig", "--ligands", required=True, help="Path to ligand CSV file (must contain smiles column)")
    run_parser.add_argument("-out", "--output", default="dockflow_output", help="Output directory")
    run_parser.add_argument("-c", "--config", default="config.yaml", help="Path to config file")

    subparsers.add_parser("check", help="Check system dependencies")

    args = parser.parse_args()

    if args.command == "run":
        if not os.path.exists(args.protein):
            raise FileNotFoundError(f"Protein file not found: {args.protein}")
        if not os.path.exists(args.ligands):
            raise FileNotFoundError(f"Ligand file not found: {args.ligands}")
        if not os.path.exists(args.config):
            raise FileNotFoundError(f"Config file not found: {args.config}")

        # ✅ NEW: create protein-based subfolder
        protein_name = os.path.splitext(os.path.basename(args.protein))[0]
        final_output_dir = os.path.join(args.output, protein_name)

        os.makedirs(final_output_dir, exist_ok=True)

        print(f"\n📁 Saving results in: {final_output_dir}\n")

        run_pipeline(
            protein_path=args.protein,
            ligand_path=args.ligands,
            output_dir=final_output_dir,  # ✅ changed here
            config_path=args.config,
        )

    elif args.command == "check":
        check_dependencies()


def check_dependencies():
    print("\nChecking system dependencies...\n")
    tools = ["vina", "obabel", "fpocket", "prepare_receptor4.py"]
    missing = False

    for tool in tools:
        if os.system(f"which {tool} > /dev/null 2>&1") != 0:
            print(f"❌ Missing: {tool}")
            missing = True
        else:
            print(f"✔ Found: {tool}")

    if missing:
        print("\n⚠ Some dependencies are missing. Install before running dockflow.\n")
    else:
        print("\n✔ All dependencies satisfied.\n")


if __name__ == "__main__":
    main()
