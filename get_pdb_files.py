#!/usr/bin/env python
# File name: get_pdb_files.py
# Author: Matt Robinson
# Date created: 06/09/2017
# Date last modified: 06/09/2017
# Python Version: 3.6

# usage: python get_pdb_files.py ids_list.txt

import sys
import os

with open(sys.argv[1]) as ids_list:
    pdb_ids = ids_list.readlines() 

os.makedirs('./test_files/')
os.chdir('./test_files/')

for pdb_id in pdb_ids:

	pdb_id = str(pdb_id)
	pdb_id = pdb_id.rstrip()

	os.makedirs('./' + pdb_id)
	os.chdir('./' + pdb_id)

	pdb_url = 'https://files.rcsb.org/download/' + pdb_id + '.pdb'
	fasta_url = 'http://www.rcsb.org/pdb/files/fasta.txt?structureIdList=' + pdb_id

	#make file names
	pdb_fn = pdb_id + '.pdb'
	fasta_fn = pdb_id + '.fasta'

	os.system('wget -O ' + pdb_fn + ' ' + pdb_url)
	os.system('wget -O ' + fasta_fn + ' ' + fasta_url)

	os.chdir('../')




