import os
import ast
import sys
from collections import defaultdict


def get_imports(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:  # Exclude relative imports
                imports.add(node.module.split('.')[0])

    return imports


def is_standard_library(module):
    return module in sys.stdlib_module_names


def main():
    current_dir = os.getcwd()
    all_files = [f for f in os.listdir(current_dir) if f.endswith('.py')]
    all_imports = defaultdict(set)
    local_modules = {os.path.splitext(f)[0] for f in all_files}

    print("Scanning .py files in the current directory...")
    for file in all_files:
        print(f"\nProcessing {file}:")
        file_imports = get_imports(file)
        print(f"  Imports found: {', '.join(file_imports)}")
        for imp in file_imports:
            all_imports[imp].add(file)

    print("\nRemoving local imports...")
    non_local_imports = {imp: files for imp, files in all_imports.items() if imp not in local_modules}
    print(f"Imports after removing local modules: {', '.join(non_local_imports.keys())}")

    print("\nRemoving standard library imports...")
    external_imports = {imp: files for imp, files in non_local_imports.items() if not is_standard_library(imp)}
    print(f"Final list of external imports: {', '.join(external_imports.keys())}")

    print("\nExternal packages required:")
    for package, files in sorted(external_imports.items()):
        print(f"- {package} (found in: {', '.join(files)})")

    # Save to possible_requirements.txt
    with open('possible_requirements.txt', 'w') as f:
        for package, files in sorted(external_imports.items()):
            f.write(f"{package} (found in: {', '.join(files)})\n")

    print(f"\nSaved external packages to possible_requirements.txt")


if __name__ == "__main__":
    main()