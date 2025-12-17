"""
Create Age Distribution Histogram for Sample Data

Summary of Prompts Used to Create This Figure:
1. "make another figure that shows the distribution of age for the sample data"

Authors: 
- Nathanael Rosenheim
- LLM: Claude Sonnet 4

Date Created: December 17, 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

# Load the sample data
csv_path = 'pdfcb_00c_sampledata.csv'
df = pd.read_csv(csv_path)

# Remove missing age values
df_clean = df.dropna(subset=['age'])

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Create histogram of age distribution
n_bins = 20  # Adjust number of bins as needed
counts, bins, patches = ax.hist(df_clean['age'], bins=n_bins, 
                               edgecolor='black', alpha=0.7, 
                               color='steelblue')

# Customize the plot
ax.set_xlabel('Age (Years)', fontsize=12)
ax.set_ylabel('Number of Respondents', fontsize=12)
ax.set_title('Age Distribution of Survey Respondents', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Add some statistics as text
mean_age = df_clean['age'].mean()
median_age = df_clean['age'].median()
total_responses = len(df_clean)

# Add statistics box
stats_text = f'Total Responses: {total_responses:,}\n'
stats_text += f'Mean Age: {mean_age:.1f} years\n'
stats_text += f'Median Age: {median_age:.1f} years'

# Position the text box in upper right
ax.text(0.98, 0.98, stats_text, transform=ax.transAxes,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
        fontsize=10)

# Improve layout
plt.tight_layout()

# Save the figure
output_path = 'pdfcb_00g_age_dist.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Age distribution histogram saved to: {output_path}")

# Add provenance information
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_filename = os.path.basename(csv_path)
provenance_text = f"Provenance: {data_filename} | {timestamp} | Made with the help of Claude Sonnet4 in VS Code Agent Mode"

# Position provenance at bottom-left
plt.figtext(0.02, -0.02, provenance_text, fontsize=8, style='italic', alpha=0.7)

# Save final version with provenance
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print("Age distribution histogram created successfully!")