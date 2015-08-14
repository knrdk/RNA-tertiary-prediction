__author__ = 'Konrad Kopciuch'

import Bio.PDB

start_id = 1
end_id   = 70
atoms_to_be_aligned = range(start_id, end_id + 1)

ref_filename = "C:\\RNA-templates\\4WJ3_Q.pdb"
sample_filename = "C:\\RNA-templates\\4WJ3_T.pdb"

pdb_parser = Bio.PDB.PDBParser(QUIET = True)
ref_structure = pdb_parser.get_structure("reference", ref_filename)
sample_structure = pdb_parser.get_structure("samle", sample_filename)

ref_model    = ref_structure[0]
sample_model = sample_structure[0]
'''
# Make a list of the atoms (in the structures) you wish to align.
# In this case we use CA atoms whose index is in the specified range
ref_atoms = []
sample_atoms = []

# Iterate of all chains in the model in order to find all residues
for ref_chain in ref_model:
  # Iterate of all residues in each model in order to find proper atoms
  for ref_res in ref_chain:
    # Check if residue number ( .get_id() ) is in the list
    if ref_res.get_id()[1] in atoms_to_be_aligned:
      # Append CA atom to list
      ref_atoms.append(ref_res['CA'])

# Do the same for the sample structure
for sample_chain in sample_model:
  for sample_res in sample_chain:
    if sample_res.get_id()[1] in atoms_to_be_aligned:
      sample_atoms.append(sample_res['CA'])
'''
ref_atoms = list(ref_model.get_atoms())
sample_atoms = list(sample_model.get_atoms())

print len(ref_atoms)

# Now we initiate the superimposer:
super_imposer = Bio.PDB.Superimposer()
super_imposer.set_atoms(ref_atoms, sample_atoms)
super_imposer.apply(sample_model.get_atoms())

# Print RMSD:
print super_imposer.rms