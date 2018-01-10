#!/usr/bin/env python2

import sys
import copy

import pybel
import openbabel

from correct_sdf import *

if __name__ == "__main__":

    nbo_filename = sys.argv[1]
    xyz_filename = sys.argv[2]

    bonds, charges, total_charge = get_bonds_nbo(nbo_filename)
    mol = pybel.readfile("xyz", xyz_filename).next()
    
    mol = delete_bonds_from_mol(mol)

    mol_corrected = add_bonds_to_mol(mol, bonds)

    total_charge_check = 0

    for i, atom in enumerate(mol):
        
        nuc = atom.OBAtom.GetAtomicNum()
        formal_charge = nuc - charges[i] 


        total_charge_check += formal_charge

        atom.OBAtom.SetFormalCharge(formal_charge)
        atom.OBAtom.SetSpinMultiplicity(0)
        # print i+1, nuc, charges[i], atom.formalcharge

    # print total_charge, total_charge_check
    assert (total_charge == total_charge_check)
    mol.OBMol.SetTotalCharge(total_charge)

    outfilename = xyz_filename.rstrip(".xyz") + "_corrected.sdf"
    
    mol.write("sdf", outfilename, overwrite=True)


    
        
