import tkinter as tk
from tkinter import filedialog, messagebox
import textwrap
import os

class ComputationalChemistryInputBuilder(tk.Tk):
    def __init__(self):           #here we made a constructor
        super().__init__()
        self.title("INPUT BUILDER")
        self.geometry_file = ""

        self.options = {                                              #
            'GUESS': ["HUCKEL", "HCore"],                             # 
            'RUNTYP': ["Energy", "Hessian", "Optimization"],          # Define arrays for various parameters
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
            label = tk.Label(self, text=key + ":", padx=30, pady=10, font=("verdana 11 "))
            label.grid(row=row // 2, column=(row % 2) * 2, sticky=tk.W, padx=130, pady=5)
            variable = tk.StringVar(self)
            variable.set(values[0])  # default value
            self.parameter_values[key] = values[0]  # set default
            option_menu = tk.OptionMenu(self, variable, *values, command=lambda value, k=key: self.set_value(k, value))
            option_menu.grid(row=row // 2, column=(row % 2) * 2 + 1, sticky=tk.EW, padx=50, pady=5, ipadx=70)
            row += 1

        # Buttons for geometry, generation, submit and save
        geom_button = tk.Button(self, text="Import Geometry File", command=self.import_geometry, background="#DCDCDC", relief="raised")
        geom_button.grid(row=(row + 1) // 2, column=0, columnspan=4, pady=20, padx=5, ipadx=30)

        generate_button = tk.Button(self, text="Generate Output", command=self.generate_input, background="#DCDCDC", relief="raised")
        generate_button.grid(row=(row + 3) // 2, column=0, columnspan=4, pady=0, padx=5, ipadx=0)

        save_button = tk.Button(self, text="Save Input File", command=self.save_input_file, background="#DCDCDC", relief="raised")
        save_button.grid(row=(row + 100) // 2, column=1, columnspan=1, pady=0, padx=5, ipadx=1)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.submit_input, background="#DCDCDC", relief="raised")
        submit_button.grid(row=(row + 100) // 2, column=2, columnspan=1, pady=10, padx=0, ipadx=10)

        # Output Text Area
        self.output_text = tk.Text(self, height=10, width=80)
        self.output_text.grid(row=(row + 50) // 2, column=0, columnspan=4, pady=20, ipady=96, ipadx=50, padx=5)

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
        # Get the values of the parameters
        parameters = {
            'scfmeth': self.parameter_values['SCFMETH'],
            'lvl': self.parameter_values['LVL'],
            'charge': self.parameter_values['CHARGE'],
            'spin': self.parameter_values['SPIN'],
            'memory': self.parameter_values['MEMORY'],
            'memddi': self.parameter_values['MEMDDI'],
            'basis': self.parameter_values['BASIS']
        }

        # Fill in the template with the parameter values
        parameters_text = '''
            $CONTRL SCFTYP={scfmeth} {lvl} RUNTYP=OPTIMIZE ICHARG={charge}
            COORD=UNIQUE MULT={spin} MAXIT=200 ISPHER=1 $END
            $SYSTEM MWORDS={memory} MEMDDI ={memddi} $END
            $STATPT NSTEP=100 HSSEND=.T. $END
            $BASIS  GBASIS={basis} $END
            $GUESS  GUESS=HUCKEL $END
            $DATA
            optg and freq
            C1
            $END
        '''
        input_content = textwrap.dedent(parameters_text).format(**parameters)

        # Append geometry content if available
        geom_content = ""
        if self.geometry_file:
            with open(self.geometry_file, 'r') as file:
                geom_content = file.read()

        input_template = f"""
            # Project by Hemali,Aditya,Ojasvi,Dev,Om
            {input_content}
            # Geometry
            {geom_content}
        """

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
    
    def submit_input(self):
        # Functionality to be executed when the submit button is clicked
        pass

if __name__ == "__main__":
    app = ComputationalChemistryInputBuilder()
    app.mainloop()
