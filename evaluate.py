from collections import Counter

def compare_resulte(own_result, ref_result):

    if own_result and ref_result is not None:
        # On compte le nombre de resluat pour chaque mot identique et on le place dans un dico
        # de type { non : occurrence}
        c_own = Counter(own_result)
        c_ref = Counter(ref_result)
        # La bibli permet de comparer les resultat et prend le plus petit present en value 
        intersection = c_own & c_ref
        true_positif = sum(intersection.values)

        total_own = len(c_own)
        total_ref = len( c_ref)

        precision = true_positif / total_own if total_own > 0 else 0
        recall = true_positif/ total_ref if total_ref >0 else 0
        f1_score= 2(precision * recall) /(precision + recall) if (precision+recall) > 0 else 0

        dico_final = {
            "Precision_model": round(precision*100, 2),
            "Precision_ref": round(recall*100 , 2),
            "F1_score": round(f1_score *100 , 2),
            "Total_Token_own": total_own,
            "Total_Token_ref":total_ref
        }
        return dico_final

