__author__ = 'Konrad Kopciuch'

import Bio.PDB


def pdb_rmsd(c1, c2):
    '''
    Funkcja zwraca RMSD pomiedzy atomami P i C4 szkieletu dwoch lancuchow
    :param c1: lancuch1
    :param c2: lancuch2
    :return: RMSD
    '''

    backbone_atoms = ['P', 'C4*']

    chain1_residues, chain2_residues = c1.get_list(), c2.get_list()
    if len(chain1_residues) != len(chain2_residues):
        raise Exception("Chains of different length.")

    atoms1, atoms2 = [], []
    for res1, res2 in zip(chain1_residues, chain2_residues):
        for atom in backbone_atoms:
            try:
                at1 = res1[atom]
                at2 = res2[atom]

                atoms1 += [at1]
                atoms2 += [at2]
            except:
                continue

    sup = Bio.PDB.Superimposer()
    sup.set_atoms(atoms1, atoms2)

    return sup.rms

def get_rmsd(pdb_path_x, pdb_path_y):
    '''
    Funckja zwraca RMSD dla lancuchow znajdujacych sie w plikach pdb, brane sa ostatnie lancuchy z pliku
    :param pdb_path_x: sciezka do pliku pdb
    :param pdb_path_y: sciezka do pliku pdb
    :return: rmsd
    '''
    parser = Bio.PDB.PDBParser()
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
    rmsd = pdb_rmsd(chain1, chain2)
    return rmsd
