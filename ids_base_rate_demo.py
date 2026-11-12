import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def bayes_precision(prevalence, tpr, fpr):
    """Calculate theoretical alert precision using Bayes' theorem."""
    benign = 1 - prevalence
    numerator = tpr * prevalence
    denominator = numerator + fpr * benign
    return numerator / denominator


def simulate_ids(n, prevalence, tpr, fpr, seed=42):
    """Simulate an IDS and calculate confusion-matrix metrics."""
    rng = np.random.default_rng(seed)

    actual_attack = rng.random(n) < prevalence
    alert = np.zeros(n, dtype=bool)

    attack_indices = actual_attack
    benign_indices = ~actual_attack

    alert[attack_indices] = rng.random(attack_indices.sum()) < tpr
    alert[benign_indices] = rng.random(benign_indices.sum()) < fpr

    tp = int(np.sum(actual_attack & alert))
    fn = int(np.sum(actual_attack & ~alert))
    fp = int(np.sum(~actual_attack & alert))
    tn = int(np.sum(~actual_attack & ~alert))

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    accuracy = (tp + tn) / n
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )

    return {
        "Events": n,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1,
        "Theoretical Precision": bayes_precision(prevalence, tpr, fpr),
    }


def main():
    # Main demonstration
    result = simulate_ids(
        n=1_000_000,
        prevalence=0.001,
        tpr=0.99,
        fpr=0.01,
        seed=42,
    )

    print("Main Demonstration Results")
    print(pd.Series(result))
    print()

    # Effect of false-positive rate
    fprs = [0.0001, 0.001, 0.005, 0.01]
    results = []

    for i, fpr in enumerate(fprs):
        r = simulate_ids(
            n=1_000_000,
            prevalence=0.001,
            tpr=0.99,
            fpr=fpr,
            seed=100 + i,
        )
        results.append({
            "False Positive Rate": fpr,
            "Simulated Precision": r["Precision"],
            "Theoretical Precision": r["Theoretical Precision"],
        })

    df = pd.DataFrame(results)
    print("Effect of False-Positive Rate")
    print(df)

    # Save results
    csv_path = OUTPUT_DIR / "simulation_results.csv"
    df.to_csv(csv_path, index=False)

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(
        df["False Positive Rate"] * 100,
        df["Simulated Precision"] * 100,
        "o-",
        label="Simulated Precision",
    )
    plt.plot(
        df["False Positive Rate"] * 100,
        df["Theoretical Precision"] * 100,
        "s--",
        label="Bayesian Precision",
    )
    plt.xlabel("False-Positive Rate (%)")
    plt.ylabel("Alert Precision (%)")
    plt.title("Effect of False-Positive Rate on IDS Alert Precision")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    image_path = OUTPUT_DIR / "precision_vs_fpr.png"
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Results saved to: {csv_path}")
    print(f"Graph saved to: {image_path}")


if __name__ == "__main__":
    main()