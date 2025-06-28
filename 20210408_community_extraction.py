# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 14:41:51 2021

@author: 81805
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import collections

def make_g(net_list):
    g = nx.Graph()    
    g.add_edges_from(net_list)
    return g

def draw_net(g):
    nx.draw_networkx(g)
    plt.show()

def community_extraction_and_indicate_degree(g):    
    degree_each_strains_dict = dict(g.degree)
    cliques   = nx.find_cliques(g)
    community = [c for c in cliques]
    return degree_each_strains_dict, community

def wrapper(net_list):
    g = make_g(net_list)
    draw_net(g)
    degree_each_strains_dict, community = community_extraction_and_indicate_degree(g)
    return g, degree_each_strains_dict, community

if __name__ == "__main__":
    
    generalist_path = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/strain_network/20210407_summarize/sharing_ortholog_number_more_than;5_generalist.tsv"
    #specialist_path = "C:/Users/81805/Desktop//research_MGEs/project_LAB178/strain_network/20210407_summarize/sharing_ortholog_number_more_than;5_specialist.tsv"
    out_dir         = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/strain_network/20210407_summarize/"
    
    l_generalist = pd.read_table(generalist_path)[["node1","node2"]].values.tolist()
    g, degree_each_strains_dict, community = wrapper(l_generalist)
    
    
    with open(out_dir + "community_extraction_of_generalist.txt","w") as f:
        com_num = 0
        for com in community:
            com_num += 1
            genus = list(set([x.split("_")[0] for x in com]))
            f.write("community " + str(com_num) + "\n")
            f.write("\t"+"number of strains ; " + str(len(com))+ "\n")
            f.write("\t"+"genus ; \n")
            for i in genus:
                f.write("\t\t"+i+"\n")
            f.write("\t"+"menber ; \n")
            for e in com:
                f.write("\t\t"+e+"\n")

    with open(out_dir + "community_extraction_of_generalist_only_genus.txt","w") as f:
        com_num = 0
        l_genus = []
        for com in community:
            com_num += 1
            genus = list(set([x.split("_")[0] for x in com]))
            l_genus.append(genus)
        l_genus_tup = [tuple(x) for x in l_genus]
        com_num_dict = dict(collections.Counter(l_genus_tup))
        l_genus_set = list(set(l_genus_tup))
        l_pattern   = [chr(ord('A') + i) for i in range(26)]
        counter = 0
        for recom in l_genus_set:
            f.write("pattern " + l_pattern[counter] + " ")
            counter += 1
            f.write("(" + str(com_num_dict[recom]) + " groups) ; ")
            for i in list(recom):
                f.write(i+", ")
            f.write("\n")
