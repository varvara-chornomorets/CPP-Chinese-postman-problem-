import csv
import os
import random

nodes_list = ['A', 'B', 'C', 'D', 'E']  # List of nodes
num_files = 5  # Number of CSV files to create
directory = 'graphs'  # Directory name

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(num_files):
    filename = f"file_{i+1}.csv"  # Construct the filename for each CSV file
    filepath = os.path.join(directory, filename)  # Create the full filepath

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['node1', 'node2', 'trail', 'distance'])

        # Generate random data rows
        for j in range(10):
            node1 = random.choice(nodes_list)
            node2 = random.choice(nodes_list)
            trail = chr(97 + j)  # Convert 0-9 to 'a'-'j'
            distance = random.randint(1, 10)  # Random distance between 1 and 10

            writer.writerow([node1, node2, trail, distance])

    print(f"CSV file '{filename}' created successfully.")
