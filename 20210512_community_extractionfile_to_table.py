# -*- coding: utf-8 -*-
"""
Created on Wed May 12 19:50:07 2021

@author: 81805
"""

import pandas as pd

path = "C:/Users/81805/Desktop/research_MGEs/project_LAB178/strain_network/20210407_summarize/community_extraction_of_generalist.txt"
out_dir = "C:/Users/81805/Desktop/paper/supplement/"

flag = "zero"
c_genus = ""
c_member = ""
with open(path,"r") as f:
    l_df  = []
    l_tmp = []
    for i in f:
        if "community" in i:
            if len(l_tmp)!=0:
                l_tmp.append(c_member.rstrip(","))
                l_df.append(l_tmp)
                l_tmp = []
                flag = "zero"
            l_tmp.append(i.split(" ")[1].rstrip("\n"))
        else:
            if "number of strains" in i:
                num_of_strain = i.split(" ; ")[1]
                l_tmp.append(num_of_strain.rstrip("\n"))
                continue
            if "genus" in i:
                flag = "one"
                c_genus = ""
                continue
            if flag == "one" and "menber" not in i:
                c_genus += i.lstrip("\t").rstrip("\n") + ","
            if "menber" in i:
                l_tmp.append(c_genus.rstrip(","))
                flag = "two"
                c_member = ""
                continue
            if flag == "two":
                c_member += i.lstrip("\t").rstrip("\n") + ","
    l_tmp.append(c_member.rstrip(","))
    l_df.append(l_tmp)

df = pd.DataFrame(l_df,columns=["community", "number of strains", "genus", "member"])
df.to_csv(out_dir + "table_s2.tsv",sep="\t", index=False)
                