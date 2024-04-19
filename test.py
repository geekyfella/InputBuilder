###Code for Gamess Input generater####
#!!####Author: Dr. Satyam Ravi ##########


from __future__ import absolute_import, unicode_literals, division, print_function
import re
import sys
import textwrap
import subprocess
import numpy as np

if sys.version_info.major>2:
    from configparser import ConfigParser as ConfigParser
else :
    from ConfigParser import SafeConfigParser as ConfigParser

class GamessOptg():

    def __init__(self, config):
        scf = ConfigParser({'path':'rungms','symmetry':'c1','processor':'1'})
        scf.read(config)

        self.optInfo  = dict(scf.items('optInfo'))
        for key in ['memory', 'memddi', 'basis', 'method', 'spin', 'charge', 'symmetry']:
            if key not in self.optInfo:
                raise Exception('Option "%s" not found in config'%key)
        try:
            self.geomFile = scf.get('gInfo','file')
        except:
            raise KeyError('Initial geometry file not found in config')
        self.CreateTemplate()


    def CreateTemplate(self):
        indent = lambda txt:'\n'.join([' '+i.strip() for i in filter(None,txt.split('\n'))])
        with open(self.geomFile) as f: geomDat = f.read()
        self.nAtoms = len(list(filter(None,geomDat.split('\n'))))

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
                                            '''.format( scfmeth = 'RHF' if self.optInfo['spin'] =='1' else
                                                                  'UHF' if self.optInfo['method'] =='b3lyp' else 'ROHF',
                                                        lvl     = {'mp2':'MPLEVL=2','ump2':'MPLEVL=2',
                                                                  'ccsd':'CCTYP=ccsd','uccsd':'CCTYP=ccsd',
                                                                  'b3lyp':'DFTTYP=b3lyp'}.get(self.optInfo['method']),
                                                        charge  = self.optInfo['charge'],
                                                        spin    = self.optInfo['spin'],
                                                        memory  = self.optInfo['memory'],
                                                        memddi  = self.optInfo['memddi'],
                                                        pre     = '$SCF DIRSCF=.TRUE. $END\n$CPHF CPHF=AO $END'
                                                                  if self.optInfo['method'] == 'b3lyp' else '',
                                                        post    = '$CCINP MAXCC =100 $END\n$FORCE METHOD=FULLNUM $END'
                                                                  if self.optInfo['method'] in ['ccsd','uccsd'] else '',
                                                        basis   = self.optInfo['basis'],
                                                        geom    = geomDat.strip()))

        with open('optg.inp', 'w') as f: f.write(indent(gamessTemplate))


if __name__ == "__main__":
    p = GamessOptg('gms.config')        
