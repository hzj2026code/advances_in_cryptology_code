import pandas as pd


WEIGHT_SETS = [
    {
        "scenario": "storage_or_bandwidth_sensitive",
        "signature_bytes": 0.5,
        "sign_avg_ms": 0.3,
        "verify_avg_ms": 0.2,
    },
    {
        "scenario": "signing_efficiency_sensitive",
        "signature_bytes": 0.3,
        "sign_avg_ms": 0.5,
        "verify_avg_ms": 0.2,
    },
    {
        "scenario": "user_verification_sensitive",
        "signature_bytes": 0.3,
        "sign_avg_ms": 0.2,
        "verify_avg_ms": 0.5,
    },
]


def normalize_lower_is_better(series):
    min_value = series.min()
    max_value = series.max()
    if max_value == min_value:
        return series * 0
    return (series - min_value) / (max_value - min_value)


def main():
    df = pd.read_csv("results/benchmark_results.csv")

    df["norm_signature_bytes"] = normalize_lower_is_better(df["signature_bytes"])
    df["norm_sign_avg_ms"] = normalize_lower_is_better(df["sign_avg_ms"])
    df["norm_verify_avg_ms"] = normalize_lower_is_better(df["verify_avg_ms"])

    all_rows = []

    for weights in WEIGHT_SETS:
        scenario = weights["scenario"]
        temp = df.copy()

        temp["score"] = (
            weights["signature_bytes"] * temp["norm_signature_bytes"]
            + weights["sign_avg_ms"] * temp["norm_sign_avg_ms"]
            + weights["verify_avg_ms"] * temp["norm_verify_avg_ms"]
        )

        temp["scenario"] = scenario
        temp = temp.sort_values("score")

        for rank, (_, row) in enumerate(temp.iterrows(), start=1):
            all_rows.append({
                "scenario": scenario,
                "rank": rank,
                "parameter_set": row["parameter_set"],
                "score": row["score"],
                "signature_bytes": row["signature_bytes"],
                "sign_avg_ms": row["sign_avg_ms"],
                "verify_avg_ms": row["verify_avg_ms"],
            })

    result = pd.DataFrame(all_rows)
    output = "results/parameter_selection_scores.csv"
    result.to_csv(output, index=False, encoding="utf-8-sig")

    print(f"Experiment 4 finished: {output}")

    best = result[result["rank"] == 1]
    print("\nRecommended parameter set for each scenario:")
    print(best[["scenario", "parameter_set", "score"]])


if __name__ == "__main__":
    main()
