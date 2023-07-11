import os
import random
import string
import csv


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
        filename = f"file_{i + 1}.csv"  # Construct the filename for each CSV file
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


def findCPP(graph, costs):
    for vertex, edges in graph.items():
        print(vertex, "->", edges)
    odd_vertices = find_odd_vertices(graph)
    if (odd_vertices):
        # 1.find odds
        # 2. pair them somehow (add new dublicating edges) and see what's going to be cheaper
        # return is only for now, later i'll remove it
        print("ODD VERTICES")
        return

    eulerian_cycle, cost = find_eulerian_cycle(graph, costs)
    print("Eulerian Cycle:", "->".join(eulerian_cycle))

    return
def find_odd_vertices(graph: dict) -> list:
    odd_vertices = []
    for vertex, connected_vertices in graph.items():
        if len(connected_vertices) % 2 == 1:
            odd_vertices.append(vertex)
    return odd_vertices




def read_graph_from_csv(file_path):
    graph = {}
    costs = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header row
        for row in reader:
            vertex1, vertex2, trail, distance = [item.strip() for item in row]
            if vertex1 not in graph:
                graph[vertex1] = []
            if vertex2 not in graph:
                graph[vertex2] = []
            costs[(vertex1, vertex2)] = int(distance)
            costs[(vertex2, vertex1)] = int(distance)
            graph[vertex1].append(vertex2)
            graph[vertex2].append(vertex1)
    return graph, costs


def find_eulerian_cycle(graph, costs):
    stack = []
    cycle = []
    cost = 0
# choose start vertex (1)
    start_vertex = list(graph.keys())[0]

    stack.append(start_vertex)
    while stack:
        current_vertex = stack[-1]

        # find unvisited edges (2)
        unvisited_edges = [(current_vertex, next_vertex) for next_vertex in graph[current_vertex] if (((current_vertex, next_vertex) not in cycle) or ((next_vertex, current_vertex) not in cycle))]
        if unvisited_edges:
            next_vertex = unvisited_edges[0][1]
            stack.append(next_vertex)
            graph[current_vertex].remove(next_vertex)
            graph[next_vertex].remove(current_vertex)
        else:
           # push the vertex we stuck to the eulerian cycle
            cycle.append(current_vertex)
            stack.pop()

    for i in range(len(cycle) - 1):
        cost += costs[(cycle[i], cycle[i+1])]

    return cycle, cost



def readGraphs():
    parent_directory = 'graphs'  # parent directory name

    # iterate over all directories
    for directory in os.listdir(parent_directory):
        directory_path = os.path.join(parent_directory, directory)  # Full directory path

        # check if the item is a directory
        if os.path.isdir(directory_path):
            print(f"STARTING NEW DIRECTORY{directory}")
            # iterate over files in the directory
            for filename in os.listdir(directory_path):
                if filename.endswith('.csv'):  # check if the file is a csv
                    file_path = os.path.join(directory_path, filename)  # full file path

                    # do everything we need
                    # THIS SHOULD WORK ONLY IF GRAPHS ARE EULErIAN SO WE WILL CHANge IT
                    print(f"Processing file '{filename}' in directory '{directory}':")
                    try:
                        graph, costs = read_graph_from_csv(file_path)
                        findCPP(graph, costs)
                    except Exception:
                        print("graph is not eulerian i guess")
                        pass
                    print()

    return




readGraphs()
