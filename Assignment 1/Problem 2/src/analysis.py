# >> This script handles Stage III: Data Analysis. <<

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import matplotlib.colors as mcolors

# Load cleaned data
data_df = pd.read_csv('../data_clean/clean_data.csv')

# Figures size
figsize = (8, 6)
dpi = 100

# Colors
cyan = '#72D6C9'
pink = '#F58CA6'
gray_bg = '#F5F5F5'
text_color = '#222222'

# Global styling
plt.style.use('default')
plt.rcParams.update({
    'axes.facecolor': gray_bg,
    'axes.edgecolor': text_color,
    'axes.labelcolor': text_color,
    'xtick.color': text_color,
    'ytick.color': text_color,
    'text.color': text_color,
    'axes.grid': True,
    'grid.color': '#CCCCCC',
    'grid.alpha': 0.5,
    'figure.facecolor': gray_bg,
})


# V1: Boxplot
df_m = pd.melt(data_df, id_vars='gender', value_vars=['reading score', 'math score'],var_name='Score Type', value_name='Score')
palette = {'reading score': cyan, 'math score': pink}
plt.figure(figsize=figsize)
sns.boxplot(x='gender', y='Score', hue='Score Type', data=df_m, palette=palette)
plt.title('Reading and Math Scores by Gender')
plt.xlabel('Gender')
plt.ylabel('Score')
plt.legend(title='Score Type')
plt.savefig('../figures/v1_gender_scores_boxplot.png')
plt.close()


# V2: Violin plot
fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)
ax.set_axisbelow(True)
groups = ['none', 'completed']
scores = [data_df[data_df['test preparation course'] == g]['math score'] for g in groups]

violins = ax.violinplot(scores, showmeans=True, showmedians=False)

for i, pc in enumerate(violins['bodies']):
    pc.set_facecolor(cyan if i == 0 else pink)
    pc.set_edgecolor(text_color)
    pc.set_alpha(0.7)

ax.set_title('Math Score Distribution by Test Preparation')
ax.set_xlabel('Test Preparation Course')
ax.set_ylabel('Math Score')
ax.set_xticks([1, 2])
ax.set_xticklabels(['None', 'Completed'])
plt.savefig('../figures/v2_prep_impact_violin.png')
plt.close()

# V3: Bar chart
fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)
ax.set_axisbelow(True)
lunch_means = data_df.groupby('lunch')['overall_avg'].mean()
lunch_colors = [cyan, pink]
lunch_means.plot(kind='bar', ax=ax, color=lunch_colors)
ax.set_title('Mean Overall Average by Lunch Type')
ax.set_xlabel('Lunch Type')
ax.set_ylabel('Mean Average Score')
plt.savefig('../figures/v3_lunch_avg_bar.png')
plt.close()

# V4: Heatmap
fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)

scores_corr = data_df[['math score', 'reading score', 'writing score']].corr()
custom_cmap = mcolors.LinearSegmentedColormap.from_list('cyan_pink', [cyan, 'white', pink])

im = ax.imshow(scores_corr, cmap=custom_cmap, vmin=0, vmax=1)

ax.set_xticks(np.arange(len(scores_corr.columns)))
ax.set_yticks(np.arange(len(scores_corr.columns)))
ax.set_xticklabels(scores_corr.columns, rotation=45, ha='right')
ax.set_yticklabels(scores_corr.columns)

for i in range(len(scores_corr)):
    for j in range(len(scores_corr)):
        ax.text(j, i, f'{scores_corr.iloc[i, j]:.2f}', ha='center', va='center', color=text_color)

ax.set_title('Correlation Heatmap of Exam Scores')
fig.colorbar(im, ax=ax)
plt.savefig('../figures/v4_scores_corr_heatmap.png')
plt.close()

# V5: Scatter plot with trend lines
fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)
ax.set_axisbelow(True)
prep_colors = {'none': cyan, 'completed': pink}
for group_name, group_data in data_df.groupby('test preparation course'):
    x = group_data['reading score']
    y = group_data['math score']
    ax.scatter(x, y, label=f'{group_name} (n={len(group_data)})', alpha=0.5, color=prep_colors[group_name])
    
    # Trend line
    x_sorted = np.sort(x)
    slope, intercept = linregress(x, y)[:2]
    ax.plot(x_sorted, slope * x_sorted + intercept, linestyle='--', color=prep_colors[group_name], label=f'{group_name} trend')

ax.set_title('Math vs Reading Scores by Test Prep')
ax.set_xlabel('Reading Score')
ax.set_ylabel('Math Score')
ax.legend()
plt.savefig('../figures/v5_math_reading_scatter.png')
plt.close()

# interpretations
with open('../reports/findings.md', 'w') as f:
    f.write('# A - Gender Differences in Math and Reading Scores\n\nBoxplots show that males slightly outperform females in math (median 69 vs. 64), while females lead in reading (73 vs. 65). Score spread is similar in math, but females have more consistent reading scores. Some female math outliers suggest room for support. These trends hint at subject-based strengths, possibly influenced by interests or teaching styles.\n\n')
    f.write('# B - Impact of Test Preparation on Math Scores\n\nStudents who completed test prep score higher in math (median 70 vs. 64). Their scores are also more consistent. Violin plots show a denser high-score cluster. With 36% completing prep, the benefit is clear. Prep seems to help, though motivation might also play a role.\n\n')
    f.write('# C - Lunch Type and Average Performance\n\nStudents with standard lunch average 71 overall, compared to 60 for those on free/reduced lunch. This 11-point gap suggests a link between nutrition (or socioeconomic status) and performance. The trend holds across subjects. Support programs could help narrow the gap.\n\n')
    f.write('# D - Correlations Among Subject Scores\n\nReading and writing are highly correlated (0.95), with math also showing strong links (0.82 with reading, 0.80 with writing). High scores tend to cluster together. This suggests students strong in one area often do well in others, though math stands out as slightly more distinct.\n\n')
    f.write('# E - Math vs Reading Association by Test Prep\n\nMath and reading scores are strongly correlated (0.82) regardless of prep status. But prep students score higher overall. The trend lines are parallel, meaning prep boosts scores without changing the overall relationship between subjects.\n')

# Finishing self note
print("Figures and findings saved!")
