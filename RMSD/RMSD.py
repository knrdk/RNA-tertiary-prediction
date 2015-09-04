__author__ = 'Konrad Kopciuch'

import Bio.PDB as bpdb

def pdb_rmsd(c1, c2):

    backbone_atoms = ['P', 'O5*', 'C5*', 'C4*', 'C3*', 'O3*']
    backbone_atoms += ['P', "O5'", "C5'", "C4'", "C3'", "O3'"]

    a_5_names = ['P', 'O5*', 'C5*', 'C4*', 'O4*', 'O2*']
    a_5_names += ['P', "O5'", "C5'", "C4'", "O4'", "O2'"]
    a_3_names = ["C1*", "C2*", "C3*", "O3*"]
    a_3_names += ["C1'", "C2'", "C3'", "O3'"]

    a_names = dict()
    a_names['U'] = a_5_names + ['N1', 'C2', 'O2', 'N3', 'C4', 'O4', 'C5', 'C6'] + a_3_names
    a_names['C'] = a_5_names + ['N1', 'C2', 'O2', 'N3', 'C4', 'N4', 'C5', 'C6'] + a_3_names

    a_names['A'] = a_5_names + ['N1', 'C2', 'N3', 'C4', 'C5', 'C6', 'N6', 'N7', 'C8', 'N9'] + a_3_names
    a_names['G'] = a_5_names + ['N1', 'C2', 'N2', 'N3', 'C4', 'C5', 'C6', 'O6', 'N7', 'C8', 'N9'] + a_3_names

    a_names['U'] = a_5_names + ['N1', 'C2', 'O2', 'N3', 'C4', 'O4', 'C5', 'C6'] + a_3_names
    a_names['C'] = a_5_names + ['N1', 'C2', 'O2', 'N3', 'C4', 'N4', 'C5', 'C6'] + a_3_names

    a_names['A'] = a_5_names + ['N1', 'C2', 'N3', 'C4', 'C5', 'C6', 'N6', 'N7', 'C8', 'N9'] + a_3_names
    a_names['G'] = a_5_names + ['N1', 'C2', 'N2', 'N3', 'C4', 'C5', 'C6', 'O6', 'N7', 'C8', 'N9'] + a_3_names

    #backbone_atoms = ['P', 'C4*'] # dodane

    all_atoms1 = []
    all_atoms2 = []

    acceptable_residues = ['A','C','G','U','rA','rC','rG','rU','DG']
    c1_list = [cr for cr in c1.get_list() ]#if cr.resname.strip() in acceptable_residues]
    c2_list = [cr for cr in c2.get_list() ]#if cr.resname.strip() in acceptable_residues]

    if len(c1_list) != len(c2_list):
        raise Exception("Chains of different length.")

    for r1,r2 in zip(c1_list, c2_list):
        anames = backbone_atoms

        for a in anames:
	    try:
		at1 = r1[a]
		at2 = r2[a]

		all_atoms1 += [at1]
		all_atoms2 += [at2]
	    except:
	        continue

    sup = bpdb.Superimposer()
    sup.set_atoms(all_atoms1, all_atoms2)

    return len(all_atoms1), sup.rms

def get_rmsd(pdb_path_x, pdb_path_y):
    parser = bpdb.PDBParser()
    str1 = parser.get_structure("1", pdb_path_x)
    str2 = parser.get_structure("2", pdb_path_y)
    chain1 = None
    for x in str1.get_chains():
        chain1 = x
        continue
    chain2 = None
    for x in str2.get_chains():
        chain2 = x
        continue
    length, rmsd = pdb_rmsd(chain1, chain2)
    return rmsd
