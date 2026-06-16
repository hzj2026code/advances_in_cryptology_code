import pandas as pd
import matplotlib.pyplot as plt


def bar_plot(df, x, y, title, ylabel, output):
    plt.figure(figsize=(10, 5))
    plt.bar(df[x], df[y])
    plt.xticks(rotation=30, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output, dpi=200)
    plt.close()


def main():
    bench = pd.read_csv("results/benchmark_results.csv")
    scenario = pd.read_csv("results/scenario_costs.csv")

    bar_plot(
        bench,
        "parameter_set",
        "signature_bytes",
        "Signature Size Comparison",
        "Signature size / bytes",
        "figures/signature_size.png",
    )

    bar_plot(
        bench,
        "parameter_set",
        "sign_avg_ms",
        "Average Signing Time Comparison",
        "Signing time / ms",
        "figures/sign_time.png",
    )

    bar_plot(
        bench,
        "parameter_set",
        "verify_avg_ms",
        "Average Verification Time Comparison",
        "Verification time / ms",
        "figures/verify_time.png",
    )

    scenario_1000 = scenario[scenario["file_count"] == 1000]

    bar_plot(
        scenario_1000,
        "parameter_set",
        "total_signature_mb",
        "Total Signature Size for 1000 Files",
        "Total signature size / MB",
        "figures/total_signature_1000_files.png",
    )

    bar_plot(
        scenario_1000,
        "parameter_set",
        "total_sign_seconds",
        "Total Signing Time for 1000 Files",
        "Total signing time / seconds",
        "figures/total_sign_time_1000_files.png",
    )

    print("Figures generated in figures/")


if __name__ == "__main__":
    main()
