import os
import sys

def fix_file_with_null_bytes(file_path):
    print(f"Fixing file: {file_path}")
    try:
        # Read the content as binary
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Remove null bytes
        fixed_content = content.replace(b'\x00', b'')
        
        # Write back the fixed content
        with open(file_path, 'wb') as f:
            f.write(fixed_content)
        
        print(f"Successfully fixed: {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_null_bytes.py <file_path> [<file_path> ...]")
        sys.exit(1)
    
    files_to_fix = sys.argv[1:]
    success_count = 0
    
    for file_path in files_to_fix:
        if os.path.isfile(file_path):
            success = fix_file_with_null_bytes(file_path)
            if success:
                success_count += 1
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nFixed {success_count} out of {len(files_to_fix)} files.") 