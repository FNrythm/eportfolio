import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

# Set style for better visualizations
plt.style.use('default')
sns.set_theme()

# Load the dataset
df = pd.read_csv('../../Unit02 auto-mpg (1).csv')

# Handle missing values in horsepower
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')

# 1. Display dataset head
print("First few rows of the dataset:")
print(df.head())

# Save the head display as an image
plt.figure(figsize=(12, 4))
plt.axis('off')
plt.table(cellText=df.head().values,
         colLabels=df.columns,
         cellLoc='center',
         loc='center')
plt.tight_layout()
plt.savefig('../../images/auto_mpg_head.png', bbox_inches='tight', dpi=300)
plt.close()

# 2. Missing values analysis
print("\nMissing values analysis:")
print(df.isnull().sum())

# Create missing values heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.tight_layout()
plt.savefig('../../images/missing_values.png', dpi=300)
plt.close()

# 3. Skewness and kurtosis
numerical_cols = df.select_dtypes(include=[np.number]).columns
skewness = df[numerical_cols].skew()
kurt = df[numerical_cols].kurtosis()

print('\nSkewness:')
print(skewness)
print('\nKurtosis:')
print(kurt)

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Plot skewness
sns.barplot(x=skewness.index, y=skewness.values, ax=axes[0])
axes[0].set_title('Skewness of Numerical Variables')
axes[0].tick_params(axis='x', rotation=45)

# Plot kurtosis
sns.barplot(x=kurt.index, y=kurt.values, ax=axes[1])
axes[1].set_title('Kurtosis of Numerical Variables')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('../../images/statistics.png', dpi=300)
plt.close()

# 4. Correlation Heatmap
# Exclude 'car name' column for correlation analysis
numeric_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(10, 7))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('../../images/correlation_heatmap.png', dpi=300)
plt.close()

# 5. Scatter plots
sns.pairplot(numeric_df)
plt.savefig('../../images/scatter_plots.png', dpi=300)
plt.close()

# 6. Replace categorical values with numerical values
print("\nOriginal 'origin' values:")
print(df['origin'].unique())

# Replace origin values
df['origin'] = df['origin'].replace({'USA': 1, 'Europe': 2, 'Japan': 3})

print("\nTransformed 'origin' values:")
print(df['origin'].unique())

# Create visualization of the transformation
plt.figure(figsize=(10, 6))
sns.countplot(x='origin', data=df)
plt.title('Distribution of Car Origins')
plt.xlabel('Origin (1: USA, 2: Europe, 3: Japan)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('../../images/transformed_data.png', dpi=300)
plt.close() 