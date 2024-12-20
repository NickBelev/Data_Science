import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Dictionary to store frequencies: {location_type: count}
location_freq = defaultdict(int)

# Open the CSV file
with open('nyc_311_trim.csv', 'r') as file:
    reader = csv.reader(file)
    
    # Iterate through each row (each row is a list of values)
    for row in reader:
        # Extract the necessary fields using indices (0-based)
        complaint_type = row[5]   # Complaint Type
        descriptor = row[6]       # Descriptor
        location_type = row[7]    # Location Type
        
        # Only process rows where complaint type is "Rodent" and descriptor is "Rat Sighting"
        if complaint_type == "Rodent" and descriptor == "Rat Sighting":
            # Increment the counter for this location type
            location_freq[location_type] += 1

# Prepare data for the plot
location_types = sorted(location_freq.keys())
frequencies = [location_freq[loc] for loc in location_types]

# Create the bar chart
plt.figure(figsize=(12, 8))
plt.bar(location_types, frequencies)
plt.xticks(rotation=90)
plt.xlabel('Location Type')
plt.ylabel('Frequency of Rat Sightings')
plt.title('Rat Sightings by Location Type in NYC (2020)')
plt.tight_layout()

# Show the plot
plt.show()
