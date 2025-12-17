import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Read the sample data
df = pd.read_csv('sample_data/pdfcb_00c_sampledata.csv')

# Remove missing values for the histogram
df_clean = df[['satscore', 'weight', 'region']].dropna()

print(f"Creating weighted histogram for {len(df_clean)} valid satisfaction responses")
print(f"Missing values: {df['satscore'].isna().sum()}")

# Create the histogram
plt.figure(figsize=(8, 4), dpi=150)  # Good size for footer image

# Define region colors and labels
region_colors = {'1': '#1f77b4', '2': '#ff7f0e', '3': '#2ca02c', '4': '#d62728'}
region_labels = {1: 'North', 2: 'South', 3: 'East', 4: 'West'}

# Create bins for categorical data
bins = np.arange(0.5, 6.5, 1)  # Bins centered on 1,2,3,4,5

# Calculate weighted counts by region for grouped histogram
weighted_counts_by_region = {}
weighted_percentages_by_region = {}

for region in sorted(df_clean['region'].unique()):
    region_data = df_clean[df_clean['region'] == region]
    region_total_weight = region_data['weight'].sum()
    
    weighted_counts = []
    weighted_percentages = []
    
    for score in range(1, 6):
        weight_sum = region_data[region_data['satscore'] == score]['weight'].sum()
        percentage = (weight_sum / region_total_weight) * 100 if region_total_weight > 0 else 0
        
        weighted_counts.append(weight_sum)
        weighted_percentages.append(percentage)
    
    weighted_counts_by_region[region] = weighted_counts
    weighted_percentages_by_region[region] = weighted_percentages

# Create grouped bar chart with percentages
bar_width = 0.2
x = np.arange(1, 6)  # Satisfaction scores 1-5
regions = sorted(weighted_percentages_by_region.keys())

bars = []
for i, region in enumerate(regions):
    percentages = weighted_percentages_by_region[region]
    offset = (i - 1.5) * bar_width  # Center the grouped bars
    bar = plt.bar(x + offset, percentages, bar_width,
                  color=region_colors[str(region)], alpha=0.8,
                  label=region_labels[region], edgecolor='white', linewidth=0.5)
    bars.append(bar)

# Customize the plot
plt.xlabel('Satisfaction Rating', fontsize=12)
plt.ylabel('Percentage', fontsize=12)
plt.title('Weighted Satisfaction Score Distribution by Region', 
          fontsize=14, fontweight='bold')

# Set x-axis ticks and labels
plt.xticks([1, 2, 3, 4, 5], 
           ['Very\nDissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very\nSatisfied'],
           fontsize=10)

# Add legend
plt.legend(title='Region', loc='upper left', framealpha=0.9)

# Customize grid and layout
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Calculate max value for y-axis scaling
max_percentage = max([max(percentages) for percentages in weighted_percentages_by_region.values()])
plt.ylim(0, min(max_percentage * 1.1, 100))  # Cap at 100% or add 10% space

# Add provenance note
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_filename = "pdfcb_00c_sampledata.csv"
provenance_text = f"Provenance: {data_filename} | {current_datetime} | Made with the help of Claude Sonnet4 in VS Code Agent Mode"

plt.figtext(0.05, 0, provenance_text, fontsize=6, style='italic', 
           color='gray', ha='left', va='bottom')

# Calculate weighted statistics
weights = df_clean['weight']
scores = df_clean['satscore']
weighted_mean = (scores * weights).sum() / weights.sum()
total_weighted_responses = weights.sum()

# For weighted median, need to sort and find cumulative weighted position
sorted_df = df_clean.sort_values('satscore')
cumulative_weights = sorted_df['weight'].cumsum()
median_position = total_weighted_responses / 2
weighted_median = sorted_df[cumulative_weights >= median_position]['satscore'].iloc[0]

# Make layout tight and clean
plt.tight_layout()

# Save the image
output_path = 'sample_data/pdfcb_00e_sampleimage.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

# Close the plot to free memory
plt.close()

print(f"Weighted histogram saved as: {output_path}")

# Print detailed statistics
print(f"\nWeighted Satisfaction Score Statistics:")
print(f"Weighted Mean: {weighted_mean:.2f}")
print(f"Weighted Median: {weighted_median:.1f}")
print(f"Total Weighted Responses: {total_weighted_responses:.0f}")
print(f"Total Unweighted Responses: {len(df_clean)}")

print(f"\nWeighted Percentages by Score and Region:")
for score in range(1, 6):
    print(f"\nScore {score}:")
    for region in sorted(df_clean['region'].unique()):
        percentage = weighted_percentages_by_region[region][score-1]
        print(f"  {region_labels[region]}: {percentage:.1f}%")

print(f"\nRegion Totals (should all be 100%):")
for region in sorted(df_clean['region'].unique()):
    total_pct = sum(weighted_percentages_by_region[region])
    region_weight = df_clean[df_clean['region'] == region]['weight'].sum()
    print(f"Region {region} ({region_labels[region]}): {total_pct:.1f}% | Total Weight: {region_weight:.0f}")