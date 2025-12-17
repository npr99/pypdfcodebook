"""
Create Regional Distribution Pie Charts for Sample Data
Side-by-side comparison of unweighted vs weighted data

Summary of Prompts Used to Create This Figure:
1. "make a pie chart based on the region data. Make two pie charts side by side. 
   One with the unweighted data and one with the weighted data."
2. "drop the total count boxes. Give the figure one title with sub titles for Weighted and Unweighted"
3. "match the color code from figure 1"

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

# Remove missing region values (if any)
df_clean = df.dropna(subset=['region'])

# Create figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Define region colors and labels
region_colors = {'1': '#1f77b4', '2': '#ff7f0e', '3': '#2ca02c', '4': '#d62728'}
region_labels = {1: 'North', 2: 'South', 3: 'East', 4: 'West'}

# Chart 1: Unweighted data (raw counts)
unweighted_counts = df_clean['region'].value_counts().sort_index()
labels_unweighted = [region_labels.get(int(region), f'Region {region}') for region in unweighted_counts.index]

# Create color list matching the region order
colors_ordered = [region_colors[str(region)] for region in unweighted_counts.index]

# Create pie chart 1
wedges1, texts1, autotexts1 = ax1.pie(unweighted_counts.values, 
                                      labels=labels_unweighted,
                                      autopct='%1.1f%%',
                                      colors=colors_ordered,
                                      startangle=90,
                                      textprops={'fontsize': 10})

ax1.set_title('Unweighted (Sample)', fontsize=12, fontweight='bold')

# Chart 2: Weighted data
weighted_counts = df_clean.groupby('region')['weight'].sum().sort_index()
labels_weighted = [region_labels.get(int(region), f'Region {region}') for region in weighted_counts.index]

# Create color list for weighted chart (same order)
colors_ordered_weighted = [region_colors[str(region)] for region in weighted_counts.index]

# Create pie chart 2
wedges2, texts2, autotexts2 = ax2.pie(weighted_counts.values,
                                      labels=labels_weighted,
                                      autopct='%1.1f%%', 
                                      colors=colors_ordered_weighted,
                                      startangle=90,
                                      textprops={'fontsize': 10})

ax2.set_title('Weighted (Population)', fontsize=12, fontweight='bold')

# Add overall title
fig.suptitle('Regional Survey Distribution', 
             fontsize=16, fontweight='bold', y=0.95)

# Improve layout
plt.tight_layout()

# Save the figure
output_path = 'pdfcb_00h_region_dist.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Regional distribution pie charts saved to: {output_path}")

# Add provenance information
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_filename = os.path.basename(csv_path)
provenance_text = f"Provenance: {data_filename} | {timestamp} | Made with the help of Claude Sonnet4 in VS Code Agent Mode"

# Position provenance at bottom
plt.figtext(0.02, 0.02, provenance_text, fontsize=8, style='italic', alpha=0.7)

# Save final version with provenance
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print("Regional distribution pie charts created successfully!")