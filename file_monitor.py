import os
import hashlib
import json

HASH_FILE = 'file_hashes.json'

def compute_file_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def monitor_directory(directory):
    current_hashes = {}
    previous_hashes = load_hashes()

    # Compute current hashes
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, directory)
            current_hashes[rel_path] = compute_file_hash(path)

    # Compare with previous
    added = set(current_hashes) - set(previous_hashes)
    removed = set(previous_hashes) - set(current_hashes)
    modified = {f for f in current_hashes if f in previous_hashes and current_hashes[f] != previous_hashes[f]}

    # Report
    if added: print("Added files:", *added, sep='\n  - ')
    if removed: print("Removed files:", *removed, sep='\n  - ')
    if modified: print("Modified files:", *modified, sep='\n  - ')
    if not (added or removed or modified):
        print("No changes detected.")

    # Save current state
    save_hashes(current_hashes)

if __name__ == "__main__":
    directory_to_monitor = '.'  # Change to your target directory
    monitor_directory(directory_to_monitor)
