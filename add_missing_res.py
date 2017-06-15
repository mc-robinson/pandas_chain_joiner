#!/usr/bin/env python
# File name: add_missing_res.py
# Author: Matt Robinson
# Date created: 06/15/2017
# Date last modified: 06/15/2017
# Python Version: 3.6
"""
Description:

Usage: python add_missing_residues.py [pdb_filename].pdb

Note: the PDB file must be in the same directory as this script.
"""
import sys
import re
import os 
from biopandas.pdb import PandasPdb
import pandas as pd

#get the pdb file name
pdb_id = os.path.splitext(os.path.basename(sys.argv[1]))[0]

#create biopandas object of the PDB file
ppdb = PandasPdb()
ppdb.read_pdb(sys.argv[1])

#create the pandas dataframes
atom_df = ppdb.df['ATOM']
hetatm_df = ppdb.df['HETATM']
others_df = ppdb.df['OTHERS']

#make atom_df so it contains both atoms and hetatms
atom_df = pd.concat([hetatm_df, atom_df])
#sort based on atom_number so it's in order
atom_df = atom_df.sort_values(by=['atom_number'])
#reset the indicies of the df
atom_df = atom_df.reset_index(drop=True)

def main():

	#chop the protein
	os.system('$MCPROdir/miscexec/chop -c -i ' + sys.argv[1] + ' > ./' + pdb_id + '_chop.log')

	#read the data
	with open(pdb_id + '_chop.log') as chop_log:
		chop_data = chop_log.readlines()

	#get list of residues immediately following chain breaks
	end_res_l = get_chop_res_l(chop_data)

	#get list of the missing res numbers
	missing_res_l = get_missing_res_l(end_res_l)

	#now write the PDB file
	write_pdb(missing_res_l)

def get_chop_res_l(chop_data):
    res_l = []
    for line in chop_data:
        if (line[0:16] == '   disconnection'):
            res = []
            res_str = line.split('(')[1].split(')')[0]
            res_l.append(res_str)
    return res_l

def get_missing_res_l(end_res_l):
	missing_res_l = []
	for res in end_res_l:
		#get num and chain
	    res_num = int(res[:-1])
	    res_chain = res[-1]
	    
	    #make boolean selecters for dataframe
	    correct_num = atom_df['residue_number'] ==  res_num
	    correct_chain = atom_df['chain_id'] == res_chain
	    
	    #find the flanking residue before the missing res
	    end_res_idx = atom_df.loc[correct_num & correct_chain].index[0]
	    begin_res_num = int(atom_df.iloc[end_res_idx -1]['residue_number'])
	    
	    #find the residues in the missing chain
	    missing_chain = list(range(begin_res_num+1,res_num))
	    #add the chain_id
	    missing_chain.append(res_chain)

	    #append to list of lists
	    missing_res_l.append(missing_chain)

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1
	    
def write_pdb(missing_res_l):

	with open(sys.argv[1]) as pdb_file:
		pdb_data = pdb_file.readlines()

	#create the header
	str_lst = [' 465',
 ' 465 MISSING RESIDUES',
 ' 465 THE FOLLOWING RESIDUES WERE NOT LOCATED IN THE',
 ' 465 EXPERIMENT. (M=MODEL NUMBER; RES=RESIDUE NAME; C=CHAIN',
 ' 465 IDENTIFIER; SSSEQ=SEQUENCE NUMBER; I=INSERTION CODE.)',
 ' 465',
 ' 465   M RES C SSSEQI']
 	#add the specific residues
 	for l in missing_res_ls:
	    for res_num in l[:-1]:
	        str_lst.append(' 465     UNK ' + str(l[-1]) + '   ' + str(res_num))

	#find where to index the string
	insert_idx = index_containing_substring(pdb_data,'REMARK 500')

	#add REMARK to beginning of every entry
	for i in range(len(str_lst)):
		str_lst[i] = 'REMARK' + str_lst[i]

	pdb_contents = pdb_data[:insert_idx] + str_lst + pdb_data[insert_idx:]

	new_pdb = open("mr_"+pdb_id+'.pdb') 
	new_pdb.writelines(pdb_contents) 
	new_pdb.close() 

	#get a list of remarks
	# remark_lst = []
	# for i in range(len(overall_list)):
	#     remark_lst.append('REMARK')
	# #get a list of indices
	# idx_lst = []
	# for i in range(len(overall_list)):
 #    	idx_lst.append(i)








if __name__ == "__main__":
	main()






