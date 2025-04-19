import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import os

# Set Seaborn style
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.2)

# Load the datasets
pop_df = pd.read_csv('Global_Population.csv')
gdp_df = pd.read_csv('Global_GDP.csv')

# Get years that are present in both datasets (from 2000 to 2020)
years = [str(year) for year in range(2000, 2021)]

# Clean the data
for df in [pop_df, gdp_df]:
    df[years] = df[years].apply(pd.to_numeric, errors='coerce')
    df[years] = df[years].apply(lambda row: row.fillna(row.mean()), axis=1)

# Calculate means for each country
pop_df['mean_population'] = pop_df[years].mean(axis=1)
gdp_df['mean_gdp'] = gdp_df[years].mean(axis=1)

# Merge datasets using Country Name
merged_df = pd.merge(
    pop_df[['Country Name', 'mean_population']], 
    gdp_df[['Country Name', 'mean_gdp']], 
    on='Country Name'
)

# Remove any rows with missing values
merged_df = merged_df.dropna()

# Calculate correlation
corr, p_value = pearsonr(merged_df['mean_population'], merged_df['mean_gdp'])

# Create directory for images if it doesn't exist
os.makedirs('assets/images', exist_ok=True)

# Correlation Plot
plt.figure(figsize=(12, 8))
sns.scatterplot(data=merged_df, x='mean_population', y='mean_gdp', alpha=0.6)
plt.title('Correlation between Population and GDP', fontsize=14, pad=20)
plt.xlabel('Mean Population (2000-2020)', fontsize=12)
plt.ylabel('Mean GDP in USD (2000-2020)', fontsize=12)

# Format axis labels
plt.ticklabel_format(style='plain', axis='both')

# Add correlation information
plt.text(0.05, 0.95, 
         f'Correlation: {corr:.2f}\np-value: {p_value:.2e}',
         transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('assets/images/correlation_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Regression Plot
plt.figure(figsize=(12, 8))
sns.regplot(data=merged_df, x='mean_population', y='mean_gdp', 
            scatter_kws={'alpha':0.6}, line_kws={'color': 'red'})

plt.title('Linear Regression: Population vs GDP', fontsize=14, pad=20)
plt.xlabel('Mean Population (2000-2020)', fontsize=12)
plt.ylabel('Mean GDP in USD (2000-2020)', fontsize=12)

# Format axis labels
plt.ticklabel_format(style='plain', axis='both')

# Calculate regression statistics
X = merged_df['mean_population'].values.reshape(-1, 1)
y = merged_df['mean_gdp'].values
reg = LinearRegression().fit(X, y)
r2 = reg.score(X, y)
slope = reg.coef_[0]
intercept = reg.intercept_

# Add regression information
plt.text(0.05, 0.95,
         f'R² = {r2:.2f}\ny = {slope:.2f}x + {intercept:.2e}',
         transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('assets/images/regression_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Print statistics for verification
print("\nAnalysis Results:")
print("-----------------")
print(f"Number of countries analyzed: {len(merged_df)}")
print(f"Correlation coefficient: {corr:.2f}")
print(f"P-value: {p_value:.2e}")
print(f"R² score: {r2:.2f}")
print(f"Regression coefficient: {slope:.2f}")
print(f"Intercept: {intercept:.2e}") 