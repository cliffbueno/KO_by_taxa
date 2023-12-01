#!/usr/bin/env python3

import sqlite3
import sys
import os

## Usage: phython3 get_meta_ko_by_taxa.py taxonoid taxa_list
## this script is designed to run on local machines that can access IMG/M database 

def run():

  taxa_infile=sys.argv[2]
  taxonoid=sys.argv[1]

  in_taxa=set()

  with open (taxa_infile) as input:
    for line in input:
      line=line.strip()
      if len(line)>=1: in_taxa.add(line)

  cLsdb='/dbpath/'+ taxonoid  +'/contig_taxonomy.sdb'
  gene_dir='/dbpath/' + taxonoid  + '/genes/'
  kosdb='/dbpath/' + taxonoid + '/ko.sdb'
  sc_tx_dict={}
  gene_sc_dict={}

  if not os.path.exists(cLsdb):
    sys.exit(cLsdb+" NOT_FOUND\n")

  conn=sqlite3.connect(cLsdb)
  sql=conn.execute("select scaffold_oid,lineage from contig_lin")
  for row in sql:
    (sc,tx)=(row[0],row[1])
    tab=tx.split(";")
    for item in tab:
      if item in in_taxa: sc_tx_dict[sc]=tx.replace(" ","_")
  conn.close()

  gene_sdb_list=os.listdir(gene_dir)

  for sdb in gene_sdb_list:
    sdb=gene_dir+sdb
    conn=sqlite3.connect(sdb)
    sql=conn.execute("select gene_oid, scaffold_oid from scaffold_genes")
    for row in sql:
      (geneID, sc)=(row[0],row[1])
      if sc_tx_dict.get(sc):
        gene_sc_dict[geneID]=sc
    conn.close()


  conn=sqlite3.connect(kosdb)
  sql=conn.execute("select ko, genes from ko_genes")
  for row in sql:
    ko=row[0]
    genes=row[1].split()
    for gene in genes:
      if gene_sc_dict.get(gene):
        sc=gene_sc_dict[gene]
        sys.stdout.write(ko+"\t"+gene+"\t"+taxonoid+"|"+sc+"|"+sc_tx_dict[sc]+"\n")


#####
run()

###end###
