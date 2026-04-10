""
Author: Harshdip Girde
""

import pandas as pd  
import os           

file_path = "data/trends_20260406.json" 

try:
    df = pd.read_json(file_path)  # json load
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print("Error loading file:", e)
    exit()


df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")


df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")


df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")


df["title"] = df["title"].str.strip()


if not os.path.exists("data"):
    os.makedirs("data")  

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False) 

print(f"\nSaved {len(df)} rows to {output_file}")

print("\nStories per category:")
print(df["category"].value_counts())  
