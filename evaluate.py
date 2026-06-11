from collections import Counter


def compare_results(own_result, ref_result):
    """Compare model results with reference results using precision, recall and F1."""
    if own_result is None or ref_result is None:
        return None

    # On compte le nombre de resultats pour chaque mot identique et on le place dans un dictionnaire
    # de type { non : occurrence}
    own_counts = Counter(own_result)
    ref_counts = Counter(ref_result)
    # La bibli permet de comparer les resultat et prend le plus petit present en value

    intersection = own_counts & ref_counts
    # print (intersection)
    true_positive = sum(intersection.values())

    total_own = len(own_result)
    total_ref = len(ref_result)

    precision = true_positive / total_own if total_own > 0 else 0
    recall = true_positive / total_ref if total_ref > 0 else 0

    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    result = {
        "Precision_model": round(precision * 100, 2),
        "Precision_ref": round(recall * 100, 2),
        "F1_score": round(f1_score * 100, 2),
        "Total_Token_own": total_own,
        "Total_Token_ref": total_ref,
    }

    return result
