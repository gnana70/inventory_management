import os
import sys

def find_files_with_null_bytes(directory):
    print(f"Scanning directory: {directory}")
    found_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        if b'\x00' in content:
                            found_files.append(file_path)
                            print(f"Found null byte in: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return found_files

if __name__ == "__main__":
    target_dir = "."
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    
    problematic_files = find_files_with_null_bytes(target_dir)
    
    if problematic_files:
        print("\nFiles with null bytes:")
        for file in problematic_files:
            print(f"  - {file}")
    else:
        print("\nNo files with null bytes found.") 