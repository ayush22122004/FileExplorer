import os
import sys
def list_files_in_folder(folder_path):
    try:
        files = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                files.append({'name': file_name, 'size': file_size, 'path': file_path})
        return files
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return []
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0  
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps
def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    i = 0  
    j = 0  
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return True  
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False
def binary_search(files, target_name):
    low, high = 0, len(files) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_name = files[mid]['name']
        if mid_name == target_name:
            return mid 
        elif mid_name < target_name:
            low = mid + 1
        else:
            high = mid - 1
    return -1  
def heapify(files, n, i, key):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if key == 'name':
        if left < n and files[left]['name'] > files[largest]['name']:
            largest = left
        if right < n and files[right]['name'] > files[largest]['name']:
            largest = right
    elif key == 'size':
        if left < n and files[left]['size'] > files[largest]['size']:
            largest = left
        if right < n and files[right]['size'] > files[largest]['size']:
            largest = right 
    if largest != i:
        files[i], files[largest] = files[largest], files[i]
        heapify(files, n, largest, key)

def heap_sort(files, key):
    n = len(files)
    for i in range(n // 2 - 1, -1, -1):
        heapify(files, n, i, key)

   
    for i in range(n - 1, 0, -1):
        files[i], files[0] = files[0], files[i]
        heapify(files, i, 0, key)

def print_sorted_files(files):
    print("Sorted files by name:")
    for file in files:
        print(f"Name: {file['name']}, Size: {file['size']} bytes")
    print()

def main(folder_path):
    
    files = list_files_in_folder(folder_path)

    if not files:
        return

    while True:
        print("Choose an option:")
        print("1. Sort files by name")
        print("2. Sort files by size")
        print("3. Search for a file by name")
        print("4. Search for text within files")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':

            heap_sort(files, 'name')
            print_sorted_files(files)

        elif choice == '2':
            
            heap_sort(files, 'size')
            print_sorted_files(files)

        elif choice == '3':
           
            target_name = input("Enter file name to search: ")
            index = binary_search(files, target_name)
            if index != -1:
                print(f"File '{target_name}' found at index {index}.")
                print(f"File path: {files[index]['path']}")
            else:
                print(f"File '{target_name}' not found.")
        
        elif choice == '4':
            search_pattern = input("Enter search pattern: ")
            print(f"\nSearching for '{search_pattern}' in files...\n")
            pattern_found = False  # Flag to track if pattern is found in any file
            for file in files:
                with open(file['path'], 'r', encoding='utf-8') as f:
                    file_text = f.read()
                    if kmp_search(file_text, search_pattern):
                        print(f"Pattern found in file: {file['name']}")
                        pattern_found = True
            if not pattern_found:
                print(f"No occurrences of '{search_pattern}' found in any file.")

        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python file_searcher.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        main(folder_path)
