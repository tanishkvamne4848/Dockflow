import csv
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
from tqdm import tqdm

from utils.io import load_existing_results, load_ligands_csv
from utils.logger import log_error, log_step, log_success, setup_logger
from utils.ranking import export_top_hits
from utils.system import run_cmd

from core.protein import prepare_protein
from core.pocket import detect_pocket
from core.ligand import prepare_ligands
from core.docking import dock
from core.scoring import get_best_score


def run_pipeline(protein_path, ligand_path, output_dir, config_path):
    setup_logger()

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/logs", exist_ok=True)
    os.makedirs(f"{output_dir}/receptor", exist_ok=True)
    os.makedirs(f"{output_dir}/ligands", exist_ok=True)
    os.makedirs(f"{output_dir}/docking", exist_ok=True)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    results_path = f"{output_dir}/results.csv"
    existing_results = load_existing_results(results_path)

    log_step("Protein preparation")
    try:
        clean_protein = prepare_protein(protein_path, output_dir)
        log_success("Protein prepared")
    except Exception as e:
        log_error(f"Protein failed: {e}")
        return

    log_step("Pocket detection")
    try:
        center = detect_pocket(clean_protein, output_dir)
        log_success(f"Pocket center: {center}")
    except Exception as e:
        log_error(f"Pocket detection failed: {e}")
        return

    log_step("Loading ligands")
    ligands = load_ligands_csv(ligand_path)
    log_success(f"{len(ligands)} ligands loaded")

    pending_ligands = [(n, s) for n, s in ligands if n not in existing_results]
    if existing_results:
        log_success(f"Resuming: {len(existing_results)} done, {len(pending_ligands)} remaining")

    results = {name: existing_results.get(name) for name, _ in ligands}

    log_step("Docking started")

    def process(entry):
        name, smiles = entry
        try:
            logging.info(f"Processing {name}")
            ligand_list = prepare_ligands(smiles, name, config, output_dir)
            if not ligand_list:
                return name, None

            best_score = None
            best_name = None

            for lig in ligand_list:
                log_file, _ = dock(lig, center, config, output_dir)
                score = get_best_score(log_file)
                if score is None:
                    continue
                if best_score is None or score < best_score:
                    best_score = score
                    best_name = lig

            if best_score is not None and best_score <= config["filters"]["score_threshold"] and best_name:
                try:
                    run_cmd(
                        [
                            "obabel",
                            f"{output_dir}/docking/out_{best_name}.pdbqt",
                            "-O",
                            f"{output_dir}/docking/{best_name}_pose.pdbqt",
                            "-m",
                        ],
                        "Pose split failed",
                    )
                except Exception as e:
                    logging.error(f"Pose extraction failed for {best_name}: {e}")

            return name, best_score
        except Exception as e:
            logging.error(f"{name} crashed: {e}")
            return name, None

    if pending_ligands:
        with ThreadPoolExecutor(max_workers=config["runtime"]["max_workers"]) as exe:
            futures = {exe.submit(process, entry): entry[0] for entry in pending_ligands}
            pbar = tqdm(total=len(futures), desc="Docking", dynamic_ncols=True)

            for future in as_completed(futures):
                ligand_name = futures[future]
                try:
                    name, score = future.result()
                    results[name] = score
                    pbar.set_postfix({"Current": ligand_name, "Score": score})
                except Exception as e:
                    results[ligand_name] = None
                    pbar.set_postfix({"Error": ligand_name})
                    logging.error(f"Thread error for {ligand_name}: {e}")
                pbar.update(1)

            pbar.close()

    log_success("Docking completed")

    log_step("Saving results")
    with open(results_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ligand", "Best Score"])
        for name in sorted(results.keys()):
            score = results[name]
            writer.writerow([name, score if score is not None else "NA"])

    export_top_hits(results, output_dir, top_n=config.get("runtime", {}).get("top_n", 10))
    log_success("Pipeline finished successfully")
