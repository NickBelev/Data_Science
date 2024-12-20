import csv
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

# Dictionary to store frequencies: {month (int): {descriptor: count}}
descriptor_freq = defaultdict(lambda: defaultdict(int))

# Open the CSV file
with open('nyc_311_trim.csv', 'r') as file:
    reader = csv.reader(file)
    
    # Iterate through each row (each row is a list of values)
    for row in reader:
        # Extract the necessary fields using indices (0-based)
        complaint_date = row[1]   # Date Created
        complaint_type = row[5]   # Complaint Type
        descriptor = row[6]       # Descriptor
        
        # Only process rows where complaint type starts with "Noise"
        if complaint_type.startswith("Noise"):
            # Extract the month as an integer from the date (assumes format 'MM/DD/YYYY HH:MM:SS AM/PM')
            month = int(complaint_date.split()[0].split('/')[0])  # Gets MM part as integer
            
            # Increment the counter for this descriptor in the given month
            descriptor_freq[month][descriptor] += 1

# Month names for plotting
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Get all unique descriptors
descriptors = set()
for month in descriptor_freq:
    descriptors.update(descriptor_freq[month].keys())
descriptors = sorted(list(descriptors))

# Prepare data for the plot
num_months = len(descriptor_freq)
x = np.arange(len(descriptors))  # the label locations
width = 0.08  # the width of the bars

# Create the plot
fig, ax = plt.subplots(figsize=(15, 8))

# Plot bars for each month
for i, month in enumerate(sorted(descriptor_freq.keys())):
    freqs = [descriptor_freq[month].get(descriptor, 0) for descriptor in descriptors]
    ax.bar(x + i * width, freqs, width, label=month_names[month - 1])

# Add labels, title, and custom x-axis tick labels
ax.set_xlabel('Noise Descriptors')
ax.set_ylabel('Frequency')
ax.set_title('Monthly Frequencies of Noise Complaint Descriptors')
ax.set_xticks(x + width * (num_months - 1) / 2)
ax.set_xticklabels(descriptors, rotation=90)
ax.legend()

fig.tight_layout()
plt.show()
