# Base-Rate Fallacy in Intrusion Detection

This project demonstrates the **base-rate fallacy** in Intrusion Detection Systems (IDS) using Bayes’ theorem and a simple Python simulation.

## Topic

**The Base-Rate Fallacy in Intrusion Detection: A Bayesian Analysis of False Alerts in Rare-Event Classification**

## Objective

To analyse how attack prevalence, true-positive rate, and false-positive rate affect the probability that an IDS alert represents a genuine attack.

## Key Idea

In real networks, attacks are rare compared with normal events. Therefore, even an IDS with high accuracy and high recall may generate many false alerts.

## Main Result

Using the following assumptions:

- Attack prevalence: 0.1%
- True-positive rate: 99%
- False-positive rate: 1%

The theoretical alert precision is approximately:

```text
9.02%
```

This means that only about 9.02% of IDS alerts represent genuine attacks.

## Technologies Used

- Python 3
- NumPy
- pandas
- Matplotlib

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python ids_base_rate_demo.py
```

## Output

The program displays:

1. Confusion-matrix values: TP, TN, FP, and FN.
2. Accuracy, precision, recall, and F1-score.
3. A comparison between simulated precision and Bayesian theoretical precision.
4. A graph showing the effect of false-positive rate on alert precision.

The results are saved in the `output/` folder:

- `simulation_results.csv`
- `precision_vs_fpr.png`

## Project Structure

```text
base-rate-fallacy-intrusion-detection/
├── ids_base_rate_demo.py
├── README.md
├── requirements.txt
└── output/
    ├── precision_vs_fpr.png
    └── simulation_results.csv
```

## Conclusion

High accuracy does not guarantee reliable IDS alerts when attacks are rare. The attack base rate and false-positive rate determine how much trust should be placed in an alert.