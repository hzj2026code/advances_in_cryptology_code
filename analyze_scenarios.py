import pandas as pd


TASK_SIZES = [100, 1000, 10000]


def main():
    df = pd.read_csv("results/benchmark_results.csv")
    rows = []

    for _, row in df.iterrows():
        for file_count in TASK_SIZES:
            rows.append({
                "parameter_set": row["parameter_set"],
                "file_count": file_count,
                "total_signature_kb": row["signature_bytes"] * file_count / 1024,
                "total_signature_mb": row["signature_bytes"] * file_count / 1024 / 1024,
                "total_sign_seconds": row["sign_avg_ms"] * file_count / 1000,
                "total_verify_seconds": row["verify_avg_ms"] * file_count / 1000,
            })

    result = pd.DataFrame(rows)
    output = "results/scenario_costs.csv"
    result.to_csv(output, index=False, encoding="utf-8-sig")

    print(f"Experiment 3 finished: {output}")
    print(result)


if __name__ == "__main__":
    main()
