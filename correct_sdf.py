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

    charges = [0 for i in range(10000)]

    start_lines = []
    end_lines = []

    for i, line in enumerate(lines):

        if "------ Lewis --------------------------------------" in line:
            start_lines.append(i)

        if "------ non-Lewis ----------------------------------" in line:
            end_lines.append(i)
# """            
# 1234567890123456789012345
#   137. BD ( 1) C  1- C  2
# """
    for i in range(len(start_lines)):

        start_line = start_lines[i]
        end_line = end_lines[i]

        for line in lines[start_line+1:end_line]:
            print line
            tokens = line.split()

            if (len(tokens) < 2):
                continue
            elif tokens[1] == "CR":
                a = int(tokens[5]) - 1
                charges[a] += 2
            elif tokens[1] == "LP":
                a = int(tokens[5]) - 1
                charges[a] += 2
            elif tokens[1] == "BD":
                
                # print "-" + line[16:19] + "-"
                # a = int(tokens[5][:-1]) - 1
                a = int(line[16:19]) - 1
                charges[a] += 1

                # b = int(tokens[7]) - 1
                b = int(line[22:25]) - 1
                charges[b] += 1


    total_charge = None


    for i, line in enumerate(lines):
        if "* Total *" in line:
            tokens = line.split()
            total_charge = int(float(tokens[3]))

    return bonds, charges, total_charge


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

    bonds, charges, total_charge = get_bonds_nbo(nbo_filename)
    mol = pybel.readfile("sdf", sdf_filename).next()
    
    mol = delete_bonds_from_mol(mol)

    mol_corrected = add_bonds_to_mol(mol, bonds)

    total_charge_check = 0

    for i, atom in enumerate(mol):
        
        nuc = atom.OBAtom.GetAtomicNum()
        formal_charge = nuc - charges[i] 


        total_charge_check += formal_charge

        atom.OBAtom.SetFormalCharge(formal_charge)
        atom.OBAtom.SetSpinMultiplicity(0)
        print nuc, charges[i], atom.formalcharge

    # print total_charge, total_charge_check
    assert (total_charge == total_charge_check)
    mol.OBMol.SetTotalCharge(total_charge)

    outfilename = sdf_filename.rstrip(".sdf") + "_corrected.sdf"
    
    mol.write("sdf", outfilename, overwrite=True)


    
        
