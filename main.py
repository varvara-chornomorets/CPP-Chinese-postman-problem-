import csv
import os
import random
import string

def generate_graphs(num_vertices, num_graphs):
    def generate_node_labels():
        alphabet = string.ascii_uppercase
        index = 0
        while True:
            if index < len(alphabet):
                yield alphabet[index]
            else:
                yield alphabet[index // len(alphabet) - 1] + alphabet[index % len(alphabet)]
            index += 1

    node_labels = generate_node_labels()
    nodes_list = [next(node_labels) for _ in range(num_vertices)]
    parent_directory = 'graphs'  # Parent directory name
    directory = os.path.join(parent_directory, f'graphs_{num_vertices}_{num_graphs}')  # Directory name

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    def dfs(graph, start):
        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                if node in graph:
                    stack.extend(graph[node] - visited)

        return visited

    def is_connected(graph, nodes):
        visited = dfs(graph, nodes[0])
        return len(visited) == len(nodes)

    for i in range(num_graphs):
        filename = f"file_{i+1}.csv"  # Construct the filename for each CSV file
        filepath = os.path.join(directory, filename)  # Create the full filepath

        graph = {}  # Initialize an empty graph
        edges_added = 0

        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['node1', 'node2', 'trail', 'distance'])

            while edges_added < num_vertices or not is_connected(graph, nodes_list):
                node1 = random.choice(nodes_list)
                node2 = random.choice(nodes_list)
                trail = f'trail_{edges_added + 1}'  # Generate trail label
                distance = random.randint(1, 10)  # Random distance between 1 and 10

                # Avoid duplicate edges
                if node1 == node2 or (node1 in graph and node2 in graph[node1]):
                    continue

                writer.writerow([node1, node2, trail, distance])

                # Build the graph
                if node1 not in graph:
                    graph[node1] = set()
                if node2 not in graph:
                    graph[node2] = set()
                graph[node1].add(node2)
                graph[node2].add(node1)

                edges_added += 1

        print(f"CSV file '{filename}' is connected with {edges_added} edges.")

# how to use generator
generate_graphs(4, 2)
def readGraphs():
    parent_directory = 'graphs'  # Parent directory name

    # Iterate over directories within the parent directory
    for directory in os.listdir(parent_directory):
        directory_path = os.path.join(parent_directory, directory)  # Full directory path

        # Check if the item in the parent directory is a directory
        if os.path.isdir(directory_path):
            print(f"STARTING NEW DIRECTORY{directory}")
            # Iterate over files within the directory
            for filename in os.listdir(directory_path):
                if filename.endswith('.csv'):  # Check if the file is a CSV file
                    file_path = os.path.join(directory_path, filename)  # Full file path

                    # Open and read the file
                    with open(file_path, 'r') as file:
                        # Read the file content
                        content = file.read()

                    # Process the file content as needed
                    print(f"Processing file '{filename}' in directory '{directory}':")
                    print(content)
                    print()

    return
readGraphs()



