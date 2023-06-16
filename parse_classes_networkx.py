import ast
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt

def get_full_name(node):
    names = []
    while isinstance(node, ast.Attribute):
        names.insert(0, node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        names.insert(0, node.id)
    return ".".join(names)

def traverse_files(directory, graph, output_file):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                fullpath = os.path.join(dirpath, filename)
                parse_classes(fullpath, graph, output_file)

def parse_classes(py_file, graph, output_file):
    with open(py_file, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                graph.add_node(node.name)
                for base in node.bases:
                    base_name = get_full_name(base)
                    graph.add_edge(base_name, node.name)  # Reverse the order here
                    output_file.write(f'Class: {node.name}, Base Class: {base_name}\n')

def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color='r', arrows=True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide directory paths as command-line arguments.")
        sys.exit(1)

    G = nx.DiGraph()
    with open("output.txt", "w") as f:  # replace "output.txt" with your desired output file path
        for directory in sys.argv[1:]:
            traverse_files(directory, G, f)
    visualize_graph(G)