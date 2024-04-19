import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from configparser import ConfigParser
import os
import textwrap

class GamessOptg():
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
            $SYSTEM MWORDS={memory} MEMDDI ={memddi} $END
            {pre}
            $STATPT NSTEP=100 HSSEND=.T. $END
            {post}
            $BASIS  GBASIS={basis} $END
            $GUESS  GUESS=HUCKEL $END
            $DATA
            optg and freq
            C1
            {geom}
            $END
            '''.format(scfmeth='RHF' if self.optInfo['spin'] == '1' else
                        'UHF' if self.optInfo['method'] == 'b3lyp' else 'ROHF',
                        lvl={'mp2': 'MPLEVL=2', 'ump2': 'MPLEVL=2',
                             'ccsd': 'CCTYP=ccsd', 'uccsd': 'CCTYP=ccsd',
                             'b3lyp': 'DFTTYP=b3lyp'}.get(self.optInfo['method']),
                        charge=self.optInfo['charge'],
                        spin=self.optInfo['spin'],
                        memory=self.optInfo['memory'],
                        memddi=self.optInfo['memddi'],
                        pre='$SCF DIRSCF=.TRUE. $END\n$CPHF CPHF=AO $END'
                            if self.optInfo['method'] == 'b3lyp' else '',
                        post='$CCINP MAXCC =100 $END\n$FORCE METHOD=FULLNUM $END'
                             if self.optInfo['method'] in ['ccsd', 'uccsd'] else '',
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
