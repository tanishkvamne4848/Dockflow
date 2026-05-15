import os
import pandas as pd


def export_top_hits(results_dict, output_dir, top_n=10):
    """Export top docking hits into top_hits.csv"""
    if not results_dict:
        return

    valid_results = []
    for ligand, score in results_dict.items():
        if score is None or score == "NA":
            continue
        try:
            score = float(score)
            valid_results.append((ligand, score))
        except Exception:
            continue

    if not valid_results:
        return

    valid_results.sort(key=lambda x: x[1])
    top_hits = valid_results[:top_n]
    df = pd.DataFrame(top_hits, columns=["Ligand", "Best Score"])
    output_path = os.path.join(output_dir, "top_hits.csv")
    df.to_csv(output_path, index=False)
    print(f"Top {len(top_hits)} hits saved → {output_path}")
