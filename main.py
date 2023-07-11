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

def make_magic(graph: dict, costs: dict, odd_vertices:list):
    odd_costs = {}
    paths = {}

    # compute the shortest distances between pairs of odd vertices
    for i in range(len(odd_vertices)):
        for j in range(i + 1, len(odd_vertices)):
            v1 = odd_vertices[i]
            v2 = odd_vertices[j]
            odd_costs[(v1, v2)], paths[(v1, v2)] = dijkstra(graph, costs, v1, v2)
            reversed_path = paths[(v1, v2)][::-1]
            odd_costs[(v2, v1)], paths[(v2, v1 )] = odd_costs[(v1, v2)], reversed_path

    # min weight perfect matching algorithm to find pairs of odd vertices to connect
    def find_min_weight_perfect_matching(costs):
        return




    edges_to_add = find_min_weight_perfect_matching(costs)

    # Add the matched edges to the original graph to create an Eulerian graph
    for (v1, v2) in edges_to_add:
        graph[v1].append(v2)
        graph[v2].append(v1)

    # Return the modified graph (now an Eulerian graph)
    return graph
def findCPP(graph, costs):
    for vertex, edges in graph.items():
        print(vertex, "->", edges)
    odd_vertices = find_odd_vertices(graph)
    if (odd_vertices):
        # pair them somehow (add new dublicating edges) and see what's going to be cheaper

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

import heapq

def dijkstra(graph, costs, start_vertex, end_vertex):
    distances = {}  # for cur known distances
    previous_vertices = {}  # to know path


    for vertex in graph:
        distances[vertex] = float('inf')
        previous_vertices[vertex] = None

    distances[start_vertex] = 0

    priority_queue = [(0, start_vertex)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # if the current distance is greater than known
        if current_distance > distances[current_vertex]:
            continue

        # check if we reached the end_vertex
        if current_vertex == end_vertex:
            break

        # look for the neighbors of the current_vertex
        for neighbor in graph[current_vertex]:
            weight = costs[(current_vertex, neighbor)]

            # possible distance with this neighbour
            possible_distance = distances[current_vertex] + weight

            # update the distance and previous_vertex if the new distance is smaller
            if possible_distance < distances[neighbor]:
                distances[neighbor] = possible_distance
                previous_vertices[neighbor] = current_vertex

                # add the neighbor to the priority queue
                heapq.heappush(priority_queue, (possible_distance, neighbor))

    # build the shortest path from start_vertex to end_vertex
    shortest_path = []
    current_vertex = end_vertex
    while current_vertex is not None:
        shortest_path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    shortest_path.reverse()  # reverse the shortest path to get the correct order

    return distances[end_vertex], shortest_path


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


graph, costs = read_graph_from_csv("C:/Users/chorn/PycharmProjects/CPP-Chinese-postman-problem/graphs/graphs_4_2/file_1.csv")
odd_vertices = find_odd_vertices(graph)
make_magic(graph, costs, odd_vertices)
# distance, path = dijkstra(graph, costs, "A", "A")
print("gjdkfg")
# "C:/Users/chorn/PycharmProjects/CPP-Chinese-postman-problem/graphs/graphs_4_2/file_1.csv"