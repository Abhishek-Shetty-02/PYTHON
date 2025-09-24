import numpy as np
import pandas as pd
import json 

def load_data(path_list):
    #base_path = r"\ticket_002_security_breach.json"
    dfs = []
    for path in path_list:
        #full_path = base_path+path
        with open(path, "r",encoding="utf-8") as f:
            data = json.load(f)
        df = pd.json_normalize(data)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)