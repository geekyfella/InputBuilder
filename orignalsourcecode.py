from __future__ import absolute_import, unicode_literals, division, print_function
import sys
import textwrap
from configparser import ConfigParser

class GamessOptg():
    def __init__(self, config):
        self.config = ConfigParser()
        self.config.read(config)
        
        # Set default values if not present
        self.config_defaults = {
            'path': 'rungms',
            'symmetry': 'c1',
            'processor': '1'
        }

        # Ensure the section and required options exist
        if not self.config.has_section('optInfo'):
            raise ValueError("The configuration file is missing the 'optInfo' section.")
        
        required_keys = ['memory', 'memddi', 'basis', 'method', 'spin', 'charge']
        missing_keys = [key for key in required_keys if key not in self.config['optInfo']]
        if missing_keys:
            raise ValueError("Missing required configuration keys: " + ", ".join(missing_keys))
        
        # Load optional geometry file path
        self.geomFile = self.config.get('gInfo', 'file', fallback=None)
        if not self.geomFile:
            raise FileNotFoundError("Initial geometry file path not provided in 'gInfo' section.")

        self.create_template()

    def create_template(self):
        with open(self.geomFile, 'r') as file:
            geom_data = file.read()
        n_atoms = len([line for line in geom_data.split('\n') if line.strip()])

        # Use default 'symmetry' if not specified
        symmetry = self.config['optInfo'].get('symmetry', self.config_defaults['symmetry'])

        gamess_template = textwrap.dedent(f"""
            $CONTRL SCFTYP={{self.resolve_scftype()}} {self.config['optInfo'].get('lvl')} RUNTYP=OPTIMIZE ICHARG={self.config['optInfo']['charge']}
            COORD=UNIQUE MULT={self.config['optInfo']['spin']} MAXIT=200 ISPHER=1 $END
            $SYSTEM MWORDS={self.config['optInfo']['memory']} MEMDDI ={self.config['optInfo']['memddi']} $END
            $STATPT NSTEP=100 HSSEND=.T. $END
            $BASIS  GBASIS={self.config['optInfo']['basis']} $END
            $GUESS  GUESS=HUCKEL $END
            $DATA
            Geometry with {n_atoms} atoms
            {symmetry}
            {geom_data}
            $END
        """).strip()

        with open('optg.inp', 'w') as f:
            f.write(gamess_template)

    def resolve_scftype(self):
        method = self.config['optInfo']['method']
        spin = self.config['optInfo']['spin']
        if spin == '1':
            return 'RHF'
        elif method == 'b3lyp':
            return 'UHF'
        return 'ROHF'

if __name__ == "__main__":
    try:
        p = GamessOptg('gms.config')
        print("Input file has been generated successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

