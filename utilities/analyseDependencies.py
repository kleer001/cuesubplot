"""
This script analyzes the import dependencies of a given file, recursively following local imports
to build a complete dependency tree. It supports multiple programming languages and identifies
unused files in the current directory.

Supported Languages:
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- Go (.go)
- Ruby (.rb)
- PHP (.php)
- C# (.cs)
- C++ (.cpp)
- Swift (.swift)
- Kotlin (.kt)
- Rust (.rs)
- Scala (.scala)
- Haskell (.hs)
- Lua (.lua)
- R (.r)
- Julia (.jl)
- Dart (.dart)
- Elm (.elm)
- Elixir (.ex)

Possible Future Enhancements (left as an exercise for the reader):
1. Add a configuration file option to allow users to define or modify import patterns without changing the script.
2. Implement language-specific parsers for more accurate analysis, especially for languages with complex module systems.
3. Add support for analyzing entire projects rather than just individual files.
4. Handle comments and string literals that might contain import-like statements.
5. Improve handling of circular dependencies and other edge cases.
6. Add more sophisticated file resolution for languages with complex module systems.
"""

import os
import re
import sys
import argparse

# Define import patterns for different languages
IMPORT_PATTERNS = {
    '.py': [
        r'^import\s+([\w.]+)',
        r'^from\s+([\w.]+)\s+import'
    ],
    '.js': [
        r'^import\s+.*?from\s+[\'"](.+?)[\'"]',
        r'^const\s+.*?=\s+require\([\'"](.+?)[\'"]\)'
    ],
    '.ts': [
        r'^import\s+.*?from\s+[\'"](.+?)[\'"]',
        r'^import\s+\{.*?\}\s+from\s+[\'"](.+?)[\'"]'
    ],
    '.java': [
        r'^import\s+([\w.]+);'
    ],
    '.go': [
        r'^import\s+[(\s]+"(.+?)"'
    ],
    '.rb': [
        r'^require\s+[\'"](.+?)[\'"]',
        r'^require_relative\s+[\'"](.+?)[\'"]'
    ],
    '.php': [
        r'^use\s+([\w\\]+)',
        r'^require(_once)?\s+[\'"](.+?)[\'"]',
        r'^include(_once)?\s+[\'"](.+?)[\'"]'
    ],
    '.cs': [
        r'^using\s+([\w.]+);'
    ],
    '.cpp': [
        r'^#include\s+[<"](.+?)[>"]'
    ],
    '.swift': [
        r'^import\s+([\w.]+)'
    ],
    '.kt': [
        r'^import\s+([\w.]+)'
    ],
    '.rs': [
        r'^use\s+([\w:]+)',
        r'^mod\s+([\w]+);'
    ],
    '.scala': [
        r'^import\s+([\w.]+)'
    ],
    '.hs': [
        r'^import\s+(qualified\s+)?([\w.]+)'
    ],
    '.lua': [
        r'^require\s+[\'"](.+?)[\'"]'
    ],
    '.r': [
        r'^library\((\w+)\)',
        r'^source\([\'"](.+?)[\'"]'
    ],
    '.jl': [
        r'^using\s+([\w.]+)',
        r'^import\s+([\w.]+)'
    ],
    '.dart': [
        r'^import\s+[\'"](.+?)[\'"]'
    ],
    '.elm': [
        r'^import\s+([\w.]+)'
    ],
    '.ex': [
        r'^import\s+([\w.]+)',
        r'^alias\s+([\w.]+)'
    ]
}

def get_imports(file_path, patterns):
    with open(file_path, 'r') as file:
        content = file.read()

    imports = []
    for pattern in patterns:
        imports.extend(re.findall(pattern, content, re.MULTILINE))

    return imports

def resolve_local_import(import_name, current_dir, file_extension):
    parts = import_name.split('.')
    for i in range(len(parts), 0, -1):
        potential_path = os.path.join(current_dir, *parts[:i]) + file_extension
        if os.path.exists(potential_path):
            return potential_path
    return None

def analyze_dependencies(start_file, file_extension, visited=None):
    if visited is None:
        visited = set()

    abs_path = os.path.abspath(start_file)
    if abs_path in visited:
        return visited

    visited.add(abs_path)
    print(f"Analyzing: {abs_path}")

    patterns = IMPORT_PATTERNS.get(file_extension, [])
    if not patterns:
        print(f"Warning: No import patterns defined for {file_extension} files.")
        return visited

    imports = get_imports(abs_path, patterns)
    current_dir = os.path.dirname(abs_path)

    for imp in imports:
        local_file = resolve_local_import(imp, current_dir, file_extension)
        if local_file:
            print(f"  Found local import: {local_file}")
            analyze_dependencies(local_file, file_extension, visited)
        else:
            print(f"  External or built-in import: {imp}")

    return visited

def get_unused_files(all_files, used_files, file_extension):
    return [f for f in all_files if f.endswith(file_extension) and os.path.abspath(f) not in used_files]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze file dependencies and find unused files.")
    parser.add_argument("start_file", help="Path to the starting file for analysis")
    parser.add_argument("--extension", help="Specify file extension if different from the start file")
    args = parser.parse_args()

    if not os.path.exists(args.start_file):
        print(f"Error: File {args.start_file} does not exist.")
        sys.exit(1)

    file_extension = args.extension if args.extension else os.path.splitext(args.start_file)[1]
    dependencies = analyze_dependencies(args.start_file, file_extension)

    print("\nAll local file dependencies:")
    for dep in dependencies:
        print(dep)

    # Get all files in the current directory
    current_dir = os.path.dirname(os.path.abspath(args.start_file))
    all_files = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]

    # Find unused files
    unused_files = get_unused_files(all_files, dependencies, file_extension)

    print(f"\nUnused {file_extension} files in the current directory:")
    for file in unused_files:
        print(file)
