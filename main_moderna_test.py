__author__ = 'Konrad Kopciuch'

from moderna import *

a = load_alignment('C:\\RNA-templates\\algn.fasta')
t = load_template('C:\\RNA-templates\\1EXD_B.pdb','A')

m = create_model(t,a)

m.write_pdb_file('C:\\RNA-templates\\01core_model.pdb')
