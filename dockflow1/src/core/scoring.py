def get_all_scores(log_file):
    """Extract all docking scores from a Vina log file."""
    scores = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    int(parts[0])
                    score = float(parts[1])
                    scores.append(score)
                except ValueError:
                    continue
    return scores


def get_best_score(log_file):
    """Extract the best (lowest / most negative) docking score."""
    scores = get_all_scores(log_file)
    if not scores:
        return None
    return min(scores)
