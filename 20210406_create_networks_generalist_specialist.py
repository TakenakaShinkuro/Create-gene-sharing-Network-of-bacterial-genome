# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:33:35 2021

@author: 81805
"""

import pandas as pd
import numpy as np
from time import time
import itertools



def get_HGT_orthoid(df):
        try:
            tmp = list(df[df["HGT_or_NAT"] == "HGT"].index)
            return tmp
        except KeyError:
            non_list = []
            return non_list


def drop_annotation_col(df):
    try:
        df_u = df.drop("cog_annotation",axis = 1)
    except KeyError:
        df_u = df    
    try:
        df_p = df_u.drop("HGT_or_NAT",axis = 1)
    except KeyError:
        df_p = df_u
    try:
        df_t = df_p.drop("total",axis = 1)
    except KeyError:
        df_t = df_p
    
    return df_t

def change_ortholog_num(df):
    HGT_orthoid = get_HGT_orthoid(df)
    df_t        = drop_annotation_col(df)
    df_f        = df_t.loc[HGT_orthoid]    
    df_nom      = df_f.where(df_f < 1,1)
    
    return df_nom


def change_ortholog_num_notonly_HGT(df):
    df_t   = drop_annotation_col(df)
    df_nom = df_t.where(df_t < 1,1)
    
    return df_nom

def make_cog_list(df):
    cog_list = []
    for index,value in df.iterrows():
        cog_list.append([index, value["cog_annotation"]])
    
    return cog_list

def clus_ortho_for_cytoscape_test(df, threshold):    
    start = time()
    
    df_drop_bin = change_ortholog_num_notonly_HGT(df)
    
    df_share_ortho_number = pd.DataFrame(index=df_drop_bin.columns.tolist(),columns=df_drop_bin.columns.tolist())
    combi_list  = list(itertools.combinations(tuple(df_drop_bin.columns.tolist()),2))
    for each_combi_tuple in combi_list:
        each_combi_list = list(each_combi_tuple)
        df_tmp = df_drop_bin[each_combi_list]
        share_ortho_number = len(df_tmp[(df_tmp.iloc[:,0]!=0) & (df_tmp.iloc[:,1]!=0)].index.tolist())
        df_share_ortho_number.at[each_combi_list[0],each_combi_list[1]] = share_ortho_number
        df_share_ortho_number.at[each_combi_list[1],each_combi_list[0]] = share_ortho_number  

    print(1,str(time()-start))    
    node_edge_list     = [tuple(sorted([index,ids])) for index,value in df_share_ortho_number.iterrows() for i,ids in zip(value,value.index) if (i > threshold and index != ids)]
    print(2,str(time()-start))  
    node_edge_list_uni = list(set(node_edge_list))    
    print(3,str(time()-start))  
    node_edge_list_uni_res = [list(x) for x in node_edge_list_uni]    
    print(4,str(time()-start))  
    df_res = pd.DataFrame(node_edge_list_uni_res,columns=["node1","node2"])    
    print(5,str(time()-start))    
    
    return df_res,node_edge_list_uni

def wrapper_generalist_specialist_network(path_plus, path_minus, path2, path3, out_dir, cog=False, threshold=0.9):    
    df2 = pd.read_table(path2)
    df3 = pd.read_table(path3,index_col="id")
    
    s_tmpx = df3["curated_name"].str.replace(" ","_")+"_"+df3["strain"].str.replace(" ","_")
    dict_tmp       = s_tmpx.to_dict()
    dict_id_spname = {k+".protein.faa":v for k,v in dict_tmp.items()}
    df2_re         = df2.rename(columns=dict_id_spname).rename({"Group_ID":"group_id"},axis='columns')
    df_set         = df2_re.set_index("group_id")
    
    
    s_tmp1  = df3["genus"].str[:1] +"._"+ df3["species"]
    s_tmp2  = " _ssp._"+ df3["subspecies"]
    s_tmp3  = s_tmp2.fillna("")
    s_tmp4  = s_tmp1 + s_tmp3
    df_LAB178_genus = pd.concat([s_tmpx.rename("strain_name"), df3["genus"], s_tmp4.rename("short_name")],axis=1)
    l_LAB178        = s_tmpx.tolist()
    #l_LAB178_genus  = [[x,x.split("_")[0]] for x in l_LAB178 for e in x]
    #df_LAB178_genus = pd.DataFrame(l_LAB178_genus,columns=["strain_name","genus"])
    #l_LAB178_combi  = list(itertools.combinations(tuple(l_LAB178),2))
    #l_LAB178_double = [list(x) for x in l_LAB178_combi]
    #df_LAB178_combi = pd.DataFrame(l_LAB178_double,columns=["node1","node2"])    
    
    df_plus    = pd.read_table(path_plus,index_col="group_id")
    df_minus   = pd.read_table(path_minus,index_col="group_id")
    if cog == False:
        df_generalist                 = df_set.loc[df_plus.index.tolist()]
        df_specialist                 = df_set.loc[df_minus.index.tolist()]    
    else:
        df_generalist                 = df_set.loc[df_plus[df_plus["cog_annotation"].str.contains(cog).replace(np.nan,False)].index.tolist()]
        df_specialist                 = df_set.loc[df_minus[df_minus["cog_annotation"].str.contains(cog).replace(np.nan,False)].index.tolist()]    

    df_res_generalist,node_edge_list_uni = clus_ortho_for_cytoscape_test(df_generalist,threshold)
    df_res_specialist,node_edge_list_uni = clus_ortho_for_cytoscape_test(df_specialist,threshold)
    
    l_tmp  = df_res_generalist.values.tolist()+df_res_specialist.values.tolist()
    l_g_s  = list(set([e for x in l_tmp for e in x]))
    l_del  = [x for x in l_LAB178 if not x in l_g_s]
    df_del = pd.DataFrame(l_del,columns=["node1"])
    
    df_res_generalist_specialist_other    = pd.concat([df_res_generalist.assign(relation="generalist"),df_res_specialist.assign(relation="specialist"),df_del],ignore_index=True)
    return df_res_generalist, df_res_specialist, df_res_generalist_specialist_other, df_LAB178_genus


    
def strain_table_plus_colorcode(colorpath,df_LAB178_genus):
    df_color  = pd.read_table(colorpath)    
    for genus_colorcode in df_color[["Unnamed: 0","genus","genus_color"]].values.tolist():
        genus_num = genus_colorcode[0]
        genus     = genus_colorcode[1]
        colorcode = genus_colorcode[2]
        df_LAB178_genus.loc[df_LAB178_genus["genus"] == genus, "genus_colorcode"] = colorcode
        df_LAB178_genus.loc[df_LAB178_genus["genus"] == genus, "genus_num"] = genus_num
    return df_LAB178_genus    
    

if __name__ == '__main__':
    #ortholog_counts_per_species_stat_path = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/20200401_LAB_178_sonicparanoid/remove_bacillus/only_accessory/ortholog_counts_per_species.stats_remove_bacillus.only_accessory.tsv"
    path_plus  = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/ortholog_network/accessory/0.9_0.3/each_orthlog/phenotype/std_1/number_of_utilization_sugar_over_threshold.10.65.tsv"
    path_minus = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/ortholog_network/accessory/0.9_0.3/each_orthlog/phenotype/minus_1_std/number_of_utilization_sugar_over_threshold.3.02.tsv"
    path2      = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/20200401_LAB_178_sonicparanoid/remove_bacillus/ortholog_counts_per_species.stats_remove_bacillus.tsv"    
    path3      = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/multiple_regression_analysis/"+\
                 "20210216_HGTnum_sigi_darkhorse_analysis/daga_LAB178_table_plus_phenotype_cog_fulfill.tsv"
    colorpath  = "C:/Users/81805/Desktop//research_MGEs/project_LAB178/strain_network/20210406_summarize/genus_colorcode.tsv"

    out_dir    = "C:/Users/81805/Desktop//research_MGEs/project_LAB178/strain_network/20210407_summarize/"
    cog        = False
    threshold  = 5
    
    df_res_generalist, df_res_specialist, df_res_generalist_specialist_other, df_LAB178_genus = wrapper_generalist_specialist_network(path_plus, path_minus, path2, path3, out_dir, cog, threshold)
    df_LAB178_genus_plus_color = strain_table_plus_colorcode(colorpath,df_LAB178_genus)
    df_res_generalist.to_csv(out_dir+"sharing_ortholog_number_more_than;"+str(threshold)+"_generalist.tsv",sep="\t")
    df_res_specialist.to_csv(out_dir+"sharing_ortholog_number_more_than;"+str(threshold)+"_specialist.tsv",sep="\t")
    df_res_generalist_specialist_other.to_csv(out_dir + "sharing_ortholog_number_more_than;"+str(threshold)+"_generalist_specialist_others.tsv",sep="\t")    
    df_LAB178_genus_plus_color.to_csv(out_dir + "sharing_ortholog_number_more_than;5_strain_table_plus_colorcode.tsv",sep="\t",index=False)
