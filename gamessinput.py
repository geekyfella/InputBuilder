import tkinter as tk
from tkinter import filedialog, messagebox
import textwrap
import os

class ComputationalChemistryInputBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Builder")
        self.geometry_file = ""
        
                                                
        self.options = {                                              #
            'GUESS': ["HUCKEL", "HCore"],                             # 
            'RUNTYP': ["Energy", "Hassian", "Optimization"],          # Define arrays for various parameters
            'SCFMETH': ["RHF", "UHF", "ROHF", "GVB", "MCSCF"],        #
            'LVL': ["LEVL2", "DFT"],                                  #
            'CHARGE': list(map(str, range(6))),     
            'SPIN': ["1", "2"],
            'MEMORY': ["10", "20", "30"],
            'MEMDDI': ["1", "2", "3"],
            'BASIS': ["cc-pVDZ", "cc-pVTZ", "cc-pVQZ"]
        }
        
        
        self.parameter_values = {key: self.options[key][0] for key in self.options}    # Initialize default parameter values  
        
        
        self.create_widgets()      # Create GUI elements

    def create_widgets(self):
        # Create the widgets dynamically
        row = 0
        for i, (key, values) in enumerate(self.options.items()):
            label = tk.Label(self, text=key + ":")
            label.grid(row=row // 2, column=(row % 2) * 2, sticky=tk.W, padx=5, pady=5)
            variable = tk.StringVar(self)
            variable.set(values[0])  # default value
            self.parameter_values[key] = values[0]  # set default
            option_menu = tk.OptionMenu(self, variable, *values, command=lambda value, k=key: self.set_value(k, value))
            option_menu.grid(row=row // 2, column=(row % 2) * 2 + 1, sticky=tk.EW, padx=5, pady=5)
            row += 1

        # Buttons for geometry, generation, and save
        geom_button = tk.Button(self, text="Import Geometry File", command=self.import_geometry)
        geom_button.grid(row=(row + 1) // 2, column=0, columnspan=2, pady=10, padx=5)

        generate_button = tk.Button(self, text="Generate Input", command=self.generate_input)
        generate_button.grid(row=(row + 3) // 2, column=0, columnspan=2, pady=10, padx=5)

        save_button = tk.Button(self, text="Save Input File", command=self.save_input_file)
        save_button.grid(row=(row + 5) // 2, column=0, columnspan=2, pady=10, padx=5)

        # Output Text Area
        self.output_text = tk.Text(self, height=10, width=80)
        self.output_text.grid(row=(row + 7) // 2, column=0, columnspan=2, pady=10, padx=5)

    def set_value(self, key, value):
        self.parameter_values[key] = value

    def import_geometry(self):
        # Open a file dialog to choose the geometry file
        filename = filedialog.askopenfilename(filetypes=[("XYZ files", "*.xyz"), ("All files", "*.*")])
        if filename:
            self.geometry_file = filename
            messagebox.showinfo("File Selected", f"Geometry file selected: {os.path.basename(filename)}")
        else:
            messagebox.showinfo("File Selection Cancelled", "No file was selected.")

    def generate_input(self):
        # Generate the input file content
        input_content = self.generate_input_content()
        # Display the input file content in the output text area
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, input_content)
        messagebox.showinfo("Success", "Input file generated successfully!")

    def generate_input_content(self):
        # Sample input file content generation based on the parameters
        parameters_text = "\n".join(f"{key}: {self.parameter_values[key]}" for key in self.options)
        geom_content = ""
        if self.geometry_file:
            with open(self.geometry_file, 'r') as file:
                geom_content = file.read()
        input_template = textwrap.dedent(f"""
            # Computational Chemistry Input File
            {parameters_text}
            # Geometry
            {geom_content}
        """)
        return input_template

    def save_input_file(self):
        # Save the generated input content to a file
        input_content = self.generate_input_content()
        file_path = filedialog.asksaveasfilename(defaultextension=".inp", filetypes=[("Input files", "*.inp"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(input_content)
            messagebox.showinfo("File Saved", f"Input file saved as: {os.path.basename(file_path)}")
        else:
            messagebox.showinfo("Save Cancelled", "File save operation was cancelled.")

if __name__ == "__main__":
    app = ComputationalChemistryInputBuilder()
    app.mainloop()
