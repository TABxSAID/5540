# >> This script This script handles Stage II: Data Processing. <<

import pandas as pd

# Load raw data
df = pd.read_csv('../data_raw/students_performance.csv')

# Report missing values for each column
missing_report = df.isnull().sum()
print("Missing values per column before processing:")
print(missing_report)

# Drop rows with >50% missing values
df = df.dropna(thresh=len(df.columns) * 0.5)

# Get numeric and categorical columns 
num_cols = [col for col in df.select_dtypes(include=['number']).columns]
cat_cols = [col for col in df.columns if col not in num_cols]

# Impute missing values: replace numerical ones with the mean and categorical ones with the mode.
for col in num_cols:
    if df[col].isnull().any():
        df[col].fillna(df[col].mean(), inplace=True)

for col in cat_cols:
    if df[col].isnull().any():
        mode_val = df[col].mode()[0]
        df[col].fillna(mode_val, inplace=True)

# Add overall_avg column
df['overall_avg'] = (df['math score'] + df['reading score'] + df['writing score']) / 3

# Save the cleaned data to a new file
df.to_csv('../data_clean/clean_data.csv', index=False)

# Finishing self note
print("Cleaned data saved!")
