import tkinter as tk
from tkinter import filedialog
from .comparing import compare_folders
import tkinter .messagebox as messagebox
from .file_downloader import download_file
from PIL import ImageTk, Image
import pandas as pd
import chardet
import openpyxl

class FolderComparatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Folder Comparator")
        
        # Set the size of the window based on the screen size of the system
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{int(screen_width * .8)}x{int(screen_height * .8)}")
        
        # Create a new frame with a black thin border at the top
        self.top_frame = tk.Frame(self.root, bd=1, relief="solid")
        self.top_frame.pack(side="top", fill="both")
        
        self.folder1_path = ""
        self.folder2_path = ""


        # Create the frame for all the buttons
        self.button_box = tk.Frame(self.root, bd=4, relief="groove", bg="#000050")  # Use hex code for dark blue
        self.button_box.pack(side="top", padx=5, pady=3, expand=True, fill="both")
        # Load the PNG logo image
        logo_image = Image.open("images/folder_logo.png")
        logo_image = logo_image.resize((20, 20))

        # Create the select folder 1 button on the top left
        self.folder1_button = tk.Button(self.button_box, text="Select Folder 1", bg="gray70", fg="white",
                                        relief="raised", borderwidth=2, command=self.select_folder1)

        # Add the logo image to the button
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.folder1_button.config(image=logo_photo, compound=tk.LEFT)
        self.folder1_button.image = logo_photo  # Keep a reference to the image to prevent garbage collection

        self.folder1_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Create the select folder 2 button below the select folder 1 button
        self.folder2_button = tk.Button(self.button_box, text="Select Folder 2", bg="gray70", fg="white",
                                        relief="raised", borderwidth=2, command=self.select_folder2)

        # Add the logo image to the button
        self.folder2_button.config(image=logo_photo, compound=tk.LEFT)
        self.folder2_button.image = logo_photo  # Keep a reference to the image to prevent garbage collection

        self.folder2_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Create the compare button beside the select folder 2 button
        self.compare_button = tk.Button(self.button_box, text="Compare Folders", bg="#008CBA", fg="white",
                                        relief="raised", borderwidth=2, command=self.compare_folders)

        compare_icon = ImageTk.PhotoImage(Image.open("images/comp.png").resize((20, 20)))
        self.compare_button.config(image=compare_icon, compound=tk.LEFT)
        self.compare_button.image = compare_icon

        self.compare_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Create the download button at the bottom left
        self.download_button = tk.Button(self.button_box, text="Download", bg="#008CBA", fg="white",
                                         relief="raised", borderwidth=2, command=self.download_files)

        download_icon = ImageTk.PhotoImage(Image.open("images/download.png").resize((20, 20)))
        self.download_button.config(image=download_icon, compound=tk.LEFT)
        self.download_button.image = download_icon

        self.download_button.grid(row=2, column=1, padx=10, pady=10)

        # Create the close button at the bottom right
        self.close_button = tk.Button(self.button_box, text="Close", bg="#f44336", fg="white",
                                      relief="raised", borderwidth=2, command=self.root.destroy)

        close_icon = ImageTk.PhotoImage(Image.open("images/off.png").resize((20, 20)))
        self.close_button.config(image=close_icon, compound=tk.LEFT)
        self.close_button.image = close_icon

        self.close_button.grid(row=2, column=3, padx=10, pady=10)

        # Configure the grid layout to expand as the window is resized
        self.button_box.columnconfigure(1, weight=1)
        self.button_box.rowconfigure(3, weight=1)

        # Create the file list box
        self.file_list = tk.Listbox(self.root, height=50, width=180)
        self.file_list.pack(pady=10)

        # Double-click binding for the file list box
        self.file_list.bind("<Double-Button-1>", self.show_file_contents)

        self.root.mainloop()

    def select_folder1(self):
        self.folder1_path = filedialog.askdirectory()
        if self.folder1_path:
            folder1_name = self.get_folder_name(self.folder1_path)
            folder1_label = tk.Label(self.button_box, text="Folder 1: " + folder1_name, fg="black")
            folder1_label.grid(row=0, column=1, padx=5, pady=5)

    def select_folder2(self):
        self.folder2_path = filedialog.askdirectory()
        if self.folder2_path:
            folder2_name = self.get_folder_name(self.folder2_path)
            folder2_label = tk.Label(self.button_box, text="Folder 2: " + folder2_name, fg="black")
            folder2_label.grid(row=1, column=1, padx=5, pady=5)

    def compare_folders(self):
        if not self.folder1_path or not self.folder2_path:
            messagebox.showinfo("Error", "First Select both Folders.")
            return

        compare_folders(self.folder1_path, self.folder2_path, self.file_list)




    def show_file_contents(self, event):
        selection = self.file_list.curselection()
        if selection:
            filename = self.file_list.get(selection[0])
            file1_path = f"{self.folder1_path}/{filename}"
            file2_path = f"{self.folder2_path}/{filename}"
            try:
                file1_contents = self.read_file(file1_path)
                file2_contents = self.read_file(file2_path)
            except UnicodeDecodeError:
                file1_contents = self.read_encoded_file(file1_path)
                file2_contents = self.read_encoded_file(file2_path)
            self.show_file_window(filename, file1_contents, file2_contents)

    def read_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()

    def read_encoded_file(self, file_path):
        with open(file_path, "rb") as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)["encoding"]
        with open(file_path, "r", encoding=encoding, errors="replace") as file:
            return file.readlines()

    def read_excel_file(self, file_path):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        file_contents = []
        for row in sheet.iter_rows(values_only=True):
            line = "\t".join(str(cell) for cell in row)
            file_contents.append(line)
        return file_contents
    
    
    
    def show_file_window(self, filename, file1_contents, file2_contents):
        # Create a new window to show the file contents
        file_window = tk.Toplevel(self.root)
        file_window.title(filename)

        # Set window properties
        file_window.geometry("700x500")
        file_window.configure(bg="#F2F2F2")
        file_window.columnconfigure(0, weight=2)
        file_window.columnconfigure(1, weight=2)

        # Create the text boxes to show the file contents
        file1_frame = tk.Frame(file_window, bd=1, relief="solid")
        file1_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        file2_frame = tk.Frame(file_window, bd=1, relief="solid")
        file2_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        file1_text = tk.Text(file1_frame, width=40, height=30, font=("Courier", 10))
        file1_text.pack(fill="both", expand=True)

        file2_text = tk.Text(file2_frame, width=40, height=30, font=("Courier", 10))
        file2_text.pack(fill="both", expand=True)

        # Compare the contents of the files and highlight any differences
        max_lines = max(len(file1_contents), len(file2_contents))

        # Add header row
        file1_text.insert(tk.END, "BELC\t\n")
        file2_text.insert(tk.END, "VEBUIN\t\n")

        # Configure header row
        header_tag = "header"
        file1_text.tag_configure(header_tag, justify="center", font=("Courier", 10, "bold"))
        file2_text.tag_configure(header_tag, justify="center", font=("Courier", 10, "bold"))

        for i in range(max_lines):
            # Add row number
            file1_text.insert(tk.END, f"{i+1}\t")
            file2_text.insert(tk.END, f"{i+1}\t")

            if i >= len(file1_contents):
                file1_text.insert(tk.END, "\n")
            else:
                file1_text.insert(tk.END, f"{file1_contents[i]}")

            if i >= len(file2_contents):
                file2_text.insert(tk.END, "\n")
            else:
                line = file2_contents[i].strip()
                if line == "":
                    file2_text.insert(tk.END, "\n")
                    continue
                vebuin_value = line.split()[0]
                belc_value = file1_contents[i].strip()
                if len(belc_value) != len(vebuin_value):
                    # if the length of the strings don't match, mark the row as mismatched
                    file2_text.insert(tk.END, f"{file2_contents[i]}")
                    column_index = len(file2_contents[i].split()[0])  # Assuming the second column starts after the first space
                    file2_text.tag_add("index", f"{i+2}.{column_index}", f"{i+2}.end")
                    file2_text.tag_config("index", foreground="red")
                else:
                    # check each character in the strings
                    for j in range(len(belc_value)):
                        if belc_value[j] != vebuin_value[j]:
                            # if any character doesn't match, mark the column as mismatched
                            file2_text.insert(tk.END, vebuin_value[j], "mismatched_column")
                            file2_text.tag_config("mismatched_column", foreground="red",background="yellow")
                        else:
                            file2_text.insert(tk.END, vebuin_value[j])

                    file2_text.insert(tk.END, " ")  # Add a space to separate columns

                # Check for extra spaces
                if len(line.split()) > 1:
                    file2_text.tag_add(f"extra_space_{i}", f"{i+2}.0", f"{i+2}.end")
                    file2_text.tag_config(f"extra_space_{i}", foreground="red")

            file2_text.insert(tk.END, "\n")

        # Disable editing in the text boxes
        file1_text.configure(state="disabled")
        file2_text.configure(state="disabled")
        
        
        #show error
        
        def show_error_rows():
            file1_text.configure(state="normal")
            file2_text.configure(state="normal")

            # Clear previous markings
            file1_text.tag_remove("mismatched_column", "1.0", tk.END)
            file2_text.tag_remove("mismatched_column", "1.0", tk.END)

            file1_text.delete(1.0, tk.END)
            file2_text.delete(1.0, tk.END)

            error_rows = []  # To store the row numbers of error rows

            # Add header row to file1_text and file2_text with a border
            file1_text.insert(tk.END, "Row\tBelc\n")
            file1_text.tag_add("header_border", "1.0", "1.end")
            file1_text.tag_config("header_border", relief="solid", borderwidth=1)
            
            file2_text.insert(tk.END, "Row\tVebuin\n")
            file2_text.tag_add("header_border", "1.0", "1.end")
            file2_text.tag_config("header_border", relief="solid", borderwidth=1)

            for i in range(max_lines):
                line = file2_contents[i].strip()
                if line == "":
                    file1_text.insert(tk.END, "\n")
                    file2_text.insert(tk.END, "\n")
                    continue

                vebuin_value = line.split()[0]
                belc_value = file1_contents[i].strip()

                if belc_value != vebuin_value:
                    error_rows.append(i + 1)  # Store the row number
                    file1_text.insert(tk.END, f"{i + 1}\t{file1_contents[i]}\n")
                    file2_text.insert(tk.END, f"{i + 1}\t{file2_contents[i]}\n")

                    # Mark mismatched characters in the Belc column
                    belc_start = file1_contents[i].index(belc_value)
                    belc_end = belc_start + len(belc_value)
                    file1_text.tag_add("mismatched_column", f"{i+2}.{belc_start}", f"{i+2}.{belc_end}")
                    file1_text.tag_config("mismatched_column", foreground="red")

                    # Mark mismatched characters in the Vebuin column
                    vebuin_start = line.index(vebuin_value)
                    vebuin_end = vebuin_start + len(vebuin_value)
                    file2_text.tag_add("mismatched_column", f"{i+2}.{vebuin_start}", f"{i+2}.{vebuin_end}")
                    file2_text.tag_config("mismatched_column", foreground="red")

            file1_text.configure(state="disabled")
            file2_text.configure(state="disabled")

            # Show error row numbers in a message box
            if error_rows:
                error_message = "Error Rows: " + ", ".join(str(row) for row in error_rows)




        # Create a frame for the button
        button_frame = tk.Frame(file_window, bg="#F2F2F2", bd=1, relief="solid")
        button_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="nw")

        # Create the button at the top left
        error_rows_button = tk.Button(button_frame, text="Errors", command=show_error_rows, bd=1, relief="solid", fg="white", bg="darkblue", width=8)
        error_rows_button.pack(padx=5, pady=5, anchor="nw")
        
        
        
        
    def get_folder_name(self, folder_path):
        return folder_path.split("/")[-1]



    def download_files(self):
        if not self.folder1_path or not self.folder2_path:
            messagebox.showinfo("Error", "No Error Files to Download.")
            return

        download_file(self.folder1_path, self.folder2_path, self.file_list)


if __name__ == "__main__":
    FolderComparatorGUI()
