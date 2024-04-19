import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from configparser import ConfigParser
import os

class GamessOptgGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GAMESS Input Generator")

        self.config_label = tk.Label(self, text="Select Config File:")
        self.config_label.pack()

        self.config_entry = tk.Entry(self, width=50)
        self.config_entry.pack()

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_config)
        self.browse_button.pack()

        self.generate_button = tk.Button(self, text="Generate Input", command=self.generate_input)
        self.generate_button.pack()

        self.output_text = tk.Text(self, height=20, width=80)
        self.output_text.pack()

    def browse_config(self):
        config_file = filedialog.askopenfilename(filetypes=[("Config files", "*.config")])
        if config_file:
            self.config_entry.delete(0, tk.END)
            self.config_entry.insert(0, config_file)

    def generate_input(self):
        config_file = self.config_entry.get()
        if not os.path.exists(config_file):
            messagebox.showerror("Error", "Config file not found!")
            return

        try:
            p = GamessOptg(config_file)
            output_text = p.PrintOutput()
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, output_text)
            messagebox.showinfo("Success", "Input file generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = GamessOptgGUI()
    app.mainloop()
