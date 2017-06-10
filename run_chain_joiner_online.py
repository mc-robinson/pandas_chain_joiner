#!/usr/bin/env python
# File name: run_chain_joiner.py
# Author: Matt Robinson
# Date created: 06/09/2017
# Date last modified: 06/09/2017
# Python Version: 3.6
"""
This program uses wget to obtain the files needed for chain_joiner from the PDB website.
It then runs chain_joiner in automodel mode. 

usage: python run_chain_joiner.py pdb_code
"""

import os
import sys
import subprocess

pdb_id = sys.argv[1]

#make url's for wget
pdb_url = 'https://files.rcsb.org/download/' + pdb_id + '.pdb'
fasta_url = 'http://www.rcsb.org/pdb/files/fasta.txt?structureIdList=' + pdb_id

#make file names
pdb_fn = pdb_id + '.pdb'
fasta_fn = pdb_id + '.fasta'

#get the files from the pdb_database
os.system('wget -O ' + pdb_fn + ' ' + pdb_url)
os.system('wget -O ' + fasta_fn + ' ' + fasta_url)

#call the functions
subprocess.call(['python', 'pandas_chain_joiner.py', pdb_id + '.pdb', pdb_id + '.fasta','-a'])

#make a folder for the output
os.makedirs('./' + pdb_id +'_output/')

#get a list of all output files in the working directory
output_files = [filename for filename in os.listdir('.') if filename.startswith(pdb_id)]

#mv these files to the output folder
for file in output_files:
	os.system('mv ' + file + ' ./' + pdb_id + '_output/')	


