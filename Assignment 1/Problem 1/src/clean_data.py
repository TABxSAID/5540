# >> This script This script handles Stage II: Data Processing. <<

import pandas as pd

# Load raw data
df = pd.read_csv('../data_raw/raw_data.csv')

# a. Unit standardization
# Converting height from inches to meters
df['Height_m'] = df['Height'] * 0.0254

# Converting weight from pounds to kg
df['Weight_kg'] = df['Weight'] * 0.45359237

# b. Feature engineering
# BMI calculation
df['BMI'] = round(df['Weight_kg'] / (df['Height_m'] ** 2), 2)

# Function to assign age groups based on the ranges given
def get_age_group(age):
    if age < 30:
        return '<30'
    elif 30 <= age <= 45:
        return '30-45'
    elif 46 <= age <= 60:
        return '46-60'
    else:
        return '>60'

# Assign the age group each row
df['AgeGroup'] = df['Age'].apply(get_age_group)

# c. Categorical to numeric encoding
# Binary for frailty
df['Frailty_binary'] = df['Frailty'].map({'Y': 1, 'N': 0}).astype('int8')

# One-hot encode age groups
age_dummies = pd.get_dummies(df['AgeGroup'], prefix='AgeGroup', dtype=int)
df = pd.concat([df, age_dummies], axis=1)

# Drop unnecessary columns
df = df.drop(['Height', 'Weight', 'Frailty', 'AgeGroup'], axis=1)

# Save the cleaned data to a new file
df.to_csv('../data_clean/clean_data.csv', index=False)

# Finishing self note
print(f"Cleaned data saved!")
