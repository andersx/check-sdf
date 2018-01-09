#!/usr/bin/env python2

import sys
import copy

import pybel
import openbabel

CHAR2NUM = dict()
CHAR2NUM["S"] = 1
CHAR2NUM["D"] = 2
CHAR2NUM["T"] = 3

def get_bonds_nbo(filename):


    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    start_line = -1
    end_line = -1

    for i, line in enumerate(lines):

        if "$CHOOSE" in line:
            start_line = i

        if "$END" in line:
            end_line = i

    mode = "lone"


    bonds = []

    for line in lines[start_line+1:end_line]:
        
        if mode == "end":
            break
        
        if mode == "bond":

            tokens = line.split()
            if tokens[0] == "BOND":
                tokens = tokens[1:]
            
            if tokens[-1] == "END":
                tokens = tokens[:-1]
            # print len(tokens), tokens

            for n in range(len(tokens) // 3):

                bonds.append(tokens[n*3:n*3+3])


            if "END" in line:
                mode = "end"

        if mode == "lone":
            if "END" in line:
                mode = "bond"
        


    return bonds


def delete_bonds_from_mol(mol):

    #Delete All bonds
    for i in range(10000):
        try:
            bo = mol.OBMol.GetBondById(i).GetBO()
            bond = mol.OBMol.GetBondById(i) 
            mol.OBMol.DeleteBond(bond)
        except AttributeError:
            break

    return mol


def add_bonds_to_mol(mol, bonds):

    for i, bond in enumerate(bonds):

        mol.OBMol.AddBond(int(bond[1]), int(bond[2]), CHAR2NUM[bond[0]])

    return mol

if __name__ == "__main__":

    nbo_filename = sys.argv[1]
    sdf_filename = sys.argv[2]

    bonds = get_bonds_nbo(nbo_filename)
    mol = pybel.readfile("sdf", sdf_filename).next()
    
    mol = delete_bonds_from_mol(mol)

    mol_corrected = add_bonds_to_mol(mol, bonds)

    outfilename = sdf_filename.rstrip(".sdf") + "_corrected.sdf"
    
    mol.write("sdf", outfilename, overwrite=True)


    
        
