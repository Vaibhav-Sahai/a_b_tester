import datasets
import pandas as pd
import typing

output_dir = "data"

def load_dataset_pd(dataset_name: str) -> pd.DataFrame:
    dataset = datasets.load_dataset(dataset_name, split = "train")
    return pd.DataFrame(dataset)

if __name__ == "__main__":
    dataset_name = "preference-agents/enron-top-senders-train"
    df = load_dataset_pd(dataset_name)
    # print(df.head())
    # Save the DataFrame to CSV
    # df.to_csv(f"data/data.csv", index=False)
    # print(df.head())
