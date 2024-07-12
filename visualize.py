import pandas as pd
import matplotlib.pyplot as plt
import mplcursors  # Import mplcursors for hover functionality

# Load data from Excel
filename = 'crawled_data.xlsx'
data_df = pd.read_excel(filename, sheet_name='URLs')

# Filter and count error codes
error_counts = data_df['Status Code'].value_counts()

# Sort error codes by count (optional)
error_counts = error_counts.sort_index()

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(error_counts.index.astype(str), error_counts, color='skyblue')

# Add labels to the bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=8)

# Customize plot details
ax.set_title('Error Codes Distribution')
ax.set_xlabel('Error Code')
ax.set_ylabel('Count')
ax.set_xticklabels(error_counts.index.astype(str), rotation=45)
ax.grid(True)

# Enable cursor-based hovering
mplcursors.cursor(hover=True)

plt.tight_layout()
plt.show()
