import tkinter as tk
from tkinter import filedialog, messagebox
from configparser import ConfigParser
import os
import textwrap

class GamessOptg:
    def __init__(self, config):
        scf = ConfigParser({'path': 'rungms', 'symmetry': 'c1', 'processor': '1'})
        scf.read(config)

        self.optInfo = dict(scf.items('optInfo'))
        for key in ['memory', 'memddi', 'basis', 'method', 'spin', 'charge', 'symmetry']:
            if key not in self.optInfo:
                raise Exception('Option "%s" not found in config' % key)
        try:
            self.geomFile = scf.get('gInfo', 'file')
        except:
            raise KeyError('Initial geometry file not found in config')
        self.CreateTemplate()

    def CreateTemplate(self):
        indent = lambda txt: '\n'.join([' ' + i.strip() for i in filter(None, txt.split('\n'))])
        with open(self.geomFile) as f:
            geomDat = f.read()
        self.nAtoms = len(list(filter(None, geomDat.split('\n'))))

        gamessTemplate = textwrap.dedent('''
            $CONTRL SCFTYP={scfmeth} {lvl} RUNTYP=OPTIMIZE ICHARG={charge}
            COORD=UNIQUE MULT={spin} MAXIT=200 ISPHER=1 $END
            $SYSTEM MWORDS={memory} MEMDDI={memddi} $END
            {pre}
            $STATPT NSTEP=100 HSSEND=.T. $END
            {post}
            $BASIS GBASIS={basis} $END
            $GUESS GUESS=HUCKEL $END
            $DATA
            optg and freq
            C1
            {geom}
            $END
            '''.format(
            scfmeth='RHF' if self.optInfo['spin'] == '1' else
            'UHF' if self.optInfo['method'] == 'b3lyp' else 'ROHF',
            lvl={'mp2': 'MPLEVL=2', 'ump2': 'MPLEVL=2',
                 'ccsd': 'CCTYP=ccsd', 'uccsd': 'CCTYP=ccsd',
                 'b3lyp': 'DFTTYP=b3lyp'}.get(self.optInfo['method']),
            charge=self.optInfo['charge'],
            spin=self.optInfo['spin'],
            memory=self.optInfo['memory'],
            memddi=self.optInfo['memddi'],
            pre='$SCF DIRSCF=.TRUE. $END\n$CPHF CPHF=AO $END' if self.optInfo['method'] == 'b3lyp' else '',
            post='$CCINP MAXCC=100 $END\n$FORCE METHOD=FULLNUM $END' if self.optInfo['method'] in ['ccsd', 'uccsd'] else '',
            basis=self.optInfo['basis'],
            geom=geomDat.strip()))

        with open('optg.inp', 'w') as f:
            f.write(indent(gamessTemplate))

    def PrintOutput(self):
        with open('optg.inp', 'r') as f:
            return f.read()

class GamessOptgGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GAMESS Input Generator")

        self.config_values = {
            'memddi': 30,
            'memory': 50,
            'processor': 1,
            'method': 'mp2',
            'basis': 'ccd',
            'spin': 3,
            'charge': 4
        }

        self.create_widgets()

    def create_widgets(self):
        self.config_label = tk.Label(self, text="Select Config File:")
        self.config_label.pack()

        self.config_entry = tk.Entry(self, width=50)
        self.config_entry.pack()

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_config)
        self.browse_button.pack()

        self.memddi_label = tk.Label(self, text="memddi:")
        self.memddi_label.pack()
        self.memddi_entry = tk.Entry(self)
        self.memddi_entry.insert(0, str(self.config_values['memddi']))
        self.memddi_entry.pack()

        self.memory_label = tk.Label(self, text="memory:")
        self.memory_label.pack()
        self.memory_entry = tk.Entry(self)
        self.memory_entry.insert(0, str(self.config_values['memory']))
        self.memory_entry.pack()

        self.processor_label = tk.Label(self, text="processor:")
        self.processor_label.pack()
        self.processor_entry = tk.Entry(self)
        self.processor_entry.insert(0, str(self.config_values['processor']))
        self.processor_entry.pack()

        self.method_label = tk.Label(self, text="method:")
        self.method_label.pack()
        self.method_entry = tk.Entry(self)
        self.method_entry.insert(0, self.config_values['method'])
        self.method_entry.pack()

        self.basis_label = tk.Label(self, text="basis:")
        self.basis_label.pack()
        self.basis_entry = tk.Entry(self)
        self.basis_entry.insert(0, self.config_values['basis'])
        self.basis_entry.pack()

        self.spin_label = tk.Label(self, text="spin:")
        self.spin_label.pack()
        self.spin_entry = tk.Entry(self)
        self.spin_entry.insert(0, str(self.config_values['spin']))
        self.spin_entry.pack()

        self.charge_label = tk.Label(self, text="charge:")
        self.charge_label.pack()
        self.charge_entry = tk.Entry(self)
        self.charge_entry.insert(0, str(self.config_values['charge']))
        self.charge_entry.pack()

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

        self.config_values['memddi'] = int(self.memddi_entry.get())
        self.config_values['memory'] = int(self.memory_entry.get())
        self.config_values['processor'] = int(self.processor_entry.get())
        self.config_values['method'] = self.method_entry.get()
        self.config_values['basis'] = self.basis_entry.get()
        self.config_values['spin'] = int(self.spin_entry.get())
        self.config_values['charge'] = int(self.charge_entry.get())

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
