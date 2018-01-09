# check-sdf
Script to correct connectivity in SDF files via NBO calculations

How to run:

    ./correct_sdf.py nbo_result.log example.sdf

where `nbo_result.log` is the output from an NBO calculation (e.g. from Gaussian or Orca etc), and `example.sdf` is the input SDF file to be corrected.

This will produce the file `example_corrected.sdf`.

Requires Openbabel/Pybel.

This is under the MIT license, GL HF.
