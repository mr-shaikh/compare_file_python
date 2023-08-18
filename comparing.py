import tkinter as tk
from tkinter import filedialog
import filecmp
import os
import chardet


def compare_folders(folder1_path, folder2_path, file_list):
    # Check if both folders are selected
    if folder1_path == "" or folder2_path == "":
        print("Please select both folders.")
        return

    # Clear the file list
    file_list.delete(0, tk.END)

    # Compare the contents of the two folders
    cmp = filecmp.dircmp(folder1_path, folder2_path)

    # Process common files
    for common_file in cmp.common_files:
        file1_path = f"{folder1_path}/{common_file}"
        file2_path = f"{folder2_path}/{common_file}"

        # Compare file contents
        if not filecmp.cmp(file1_path, file2_path, shallow=False):
            file_list.insert(tk.END, common_file)
            index = file_list.size() - 1
            file_list.itemconfig(index, {'fg': 'red'})

            try:
                # Read file contents with detected encoding
                with open(file1_path, "rb") as file1, open(file2_path, "rb") as file2:
                    file1_encoding = chardet.detect(file1.read())['encoding']
                    file2_encoding = chardet.detect(file2.read())['encoding']

                    if file1_encoding and file2_encoding and file1_encoding == file2_encoding and file1_encoding.startswith("utf"):
                        file1_contents = file1.read().decode(file1_encoding)
                        file2_contents = file2.read().decode(file2_encoding)
                    else:
                        print(f"Error reading file {common_file}: unsupported encoding or encoding mismatch")
                        continue
            except UnicodeDecodeError:
                print(f"Error reading file {common_file}: UnicodeDecodeError")
                continue

            if file1_contents != file2_contents:
                if file1_contents.replace('\n', '') == file2_contents.replace('\n', ''):
                    file_list.itemconfig(index, {'fg': 'orange'})
                else:
                    file_list.itemconfig(index, {'fg': 'red'})

                file1_rows = file1_contents.split('\n')
                file2_rows = file2_contents.split('\n')
                row_swapped = True

                # Check if rows are swapped
                for i in range(len(file1_rows)):
                    if file1_rows[i].strip() not in file2_rows:
                        row_swapped = False
                        break

                if row_swapped:
                    file_list.insert(tk.END, f"{common_file} - Swapped rows")
                    file_list.itemconfig(index, {'fg': 'orange'})
            else:
                file1_contents = open(file1_path, encoding='cp932', errors='ignore').readlines()
                file2_contents = open(file2_path, encoding='cp932', errors='ignore').readlines()
                match_found = False

                # Check if there is a match between rows
                for row1 in file1_contents:
                    row1 = row1.strip()
                    for row2 in file2_contents:
                        row2 = row2.strip()
                        if row1 == row2:
                            match_found = True
                            break
                    if match_found:
                        break

                if not match_found:
                    file_list.insert(tk.END, common_file)
                    index = file_list.size() - 1
                    file_list.itemconfig(index, {'fg': 'orange'})

    # Process files only in folder1 (missing in folder2)
    for file_only_folder1 in cmp.left_only:
        file_list.insert(tk.END, f"{file_only_folder1} - Missing")
        index = file_list.size() - 1
        file_list.itemconfig(index, {'fg': 'black'})

    # Process files only in folder2 (extra in folder2)
    for file_only_folder2 in cmp.right_only:
        file_list.insert(tk.END, f"{file_only_folder2} - Extra")
        index = file_list.size() - 1
        file_list.itemconfig(index, {'fg': 'black'})

