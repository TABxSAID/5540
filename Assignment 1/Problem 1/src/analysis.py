# >> This script handles Stage III: Data Analysis. <<

import pandas as pd

# Load cleaned data
df = pd.read_csv('../data_clean/clean_data.csv')

# Get numeric columns but exclude AgeGroup and Frailty_binary columns
numeric_cols = [col for col in df.select_dtypes(include=['number']).columns if not col.startswith('AgeGroup_') and col != 'Frailty_binary']

# Calculate mean, median, and standard deviation
summary = df[numeric_cols].agg(['mean', 'median', 'std']).transpose()

# Correlation between grip strength and binary frailty
correlation = df['Grip_strength'].corr(df['Frailty_binary'])

# Save the findings to markdown
with open('../reports/findings.md', 'w') as f:
    f.write('# Summary Statistics\n\n')
    f.write(summary.to_markdown())
    f.write('\n\n# Correlation between Grip Strength and Frailty\n\n')
    f.write(f'The correlation coefficient is {correlation:.4f}.\n')

# Finishing self note
print("Findings saved!")