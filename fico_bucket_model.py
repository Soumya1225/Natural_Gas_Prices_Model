import pandas as pd

# Load data
df = pd.read_csv("data/loan_data.csv")


def create_rating_map(num_buckets=10):

    data = df.copy()

    # Create equal-frequency buckets
    data["Bucket"] = pd.qcut(
        data["fico_score"],
        q=num_buckets,
        duplicates="drop"
    )

    summary = (
        data.groupby("Bucket")
        .agg(
            Min_FICO=("fico_score", "min"),
            Max_FICO=("fico_score", "max"),
            Borrowers=("fico_score", "count"),
            Defaults=("default", "sum")
        )
        .reset_index()
    )

    summary["PD"] = (
        summary["Defaults"] /
        summary["Borrowers"]
    )

    summary["Rating"] = range(
        1,
        len(summary) + 1
    )

    return summary
