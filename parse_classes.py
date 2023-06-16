import ast
import os
import csv
import argparse

def get_full_name(node):
    names = []
    while isinstance(node, ast.Attribute):
        names.insert(0, node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        names.insert(0, node.id)
    return ".".join(names)

def traverse_files(directories, csv_writer):
    for directory in directories:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith('.py'):
                    fullpath = os.path.join(dirpath, filename)
                    parse_classes(fullpath, csv_writer)

def parse_classes(py_file, csv_writer):
    with open(py_file, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    base_name = get_full_name(base)
                    csv_writer.writerow([node.name, base_name])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traverse directories for Python files and parse class names")
    parser.add_argument("dirs", nargs='+', help="Directories to traverse")
    args = parser.parse_args()

    with open("output.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Class Name", "Base Class Name"])  # Write header
        traverse_files(args.dirs, writer)
