import tkinter as tk
from tkinter import filedialog, messagebox
import textwrap

class ComputationalChemistryInputBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Computational Chemistry Input Builder")

        # Initialize default parameter values
        self.parameter_values = {
            'basis_set': 'cc-pVTZ',
            'functional': 'B3LYP',
            'charge': 0,
            'multiplicity': 1,
            'geometry_file': ''
        }

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Basis Set
        self.basis_label = tk.Label(self, text="Basis Set:")
        self.basis_label.pack()
        self.basis_entry = tk.Entry(self)
        self.basis_entry.insert(0, self.parameter_values['basis_set'])
        self.basis_entry.pack()

        # Functional
        self.functional_label = tk.Label(self, text="Functional:")
        self.functional_label.pack()
        self.functional_entry = tk.Entry(self)
        self.functional_entry.insert(0, self.parameter_values['functional'])
        self.functional_entry.pack()

        # Charge
        self.charge_label = tk.Label(self, text="Charge:")
        self.charge_label.pack()
        self.charge_entry = tk.Entry(self)
        self.charge_entry.insert(0, str(self.parameter_values['charge']))
        self.charge_entry.pack()

        # Multiplicity
        self.multiplicity_label = tk.Label(self, text="Multiplicity:")
        self.multiplicity_label.pack()
        self.multiplicity_entry = tk.Entry(self)
        self.multiplicity_entry.insert(0, str(self.parameter_values['multiplicity']))
        self.multiplicity_entry.pack()

        # Geometry File
        self.geometry_label = tk.Label(self, text="Geometry File:")
        self.geometry_label.pack()
        self.geometry_entry = tk.Entry(self, width=50)
        self.geometry_entry.pack()

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_geometry_file)
        self.browse_button.pack()

        # Generate Input Button
        self.generate_button = tk.Button(self, text="Generate Input", command=self.generate_input)
        self.generate_button.pack()

        # Output Text Area
        self.output_text = tk.Text(self, height=20, width=80)
        self.output_text.pack()

    def browse_geometry_file(self):
        geometry_file = filedialog.askopenfilename(filetypes=[("XYZ Files", "*.xyz")])
        if geometry_file:
            self.geometry_entry.delete(0, tk.END)
            self.geometry_entry.insert(0, geometry_file)

    def generate_input(self):
        # Update parameter values based on user input
        self.parameter_values['basis_set'] = self.basis_entry.get()
        self.parameter_values['functional'] = self.functional_entry.get()
        self.parameter_values['charge'] = int(self.charge_entry.get())
        self.parameter_values['multiplicity'] = int(self.multiplicity_entry.get())
        self.parameter_values['geometry_file'] = self.geometry_entry.get()

        # Generate the input file content
        input_content = self.generate_input_content()

        # Display the input file content in the output text area
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, input_content)

        messagebox.showinfo("Success", "Input file generated successfully!")

    def generate_input_content(self):
        # Sample input file content generation based on the parameters
        input_template = textwrap.dedent(f"""
            # Computational Chemistry Input File
            Basis Set: {self.parameter_values['basis_set']}
            Functional: {self.parameter_values['functional']}
            Charge: {self.parameter_values['charge']}
            Multiplicity: {self.parameter_values['multiplicity']}
            
            Geometry:
            # Insert geometry from file: {self.parameter_values['geometry_file']}
        """)

        return input_template

if __name__ == "__main__":
    app = ComputationalChemistryInputBuilder()
    app.mainloop()
