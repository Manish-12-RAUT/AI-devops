import pandas as pd

DATASET_PATH = "data/raw/logs.csv"

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nClass distribution:")
print(df["label"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSample records:")
print(df.head(10))