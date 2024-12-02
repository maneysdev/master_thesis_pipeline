#!/usr/bin/env python

import pandas as pd
import json
import os

class DataWriter:
    
    dataFrame = pd.DataFrame()
    
    def __init__(self):
        pass
    
    def gen_pandas_df(self, data):
        #generate and shuffle the dataframe rows
        self.dataFrame = (pd.DataFrame(data)).sample(frac = 1)
        
    def set_pandas_df(self, df):
        self.dataFrame = df
        
    def write_csv(self, path):
        directory = os.path.dirname(path)
        # Check if the directory exists, and create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        self.dataFrame.to_csv(path, sep='\t', encoding='utf-8', index=False)
        
    def write_excel(self, path):
        directory = os.path.dirname(path)
        # Check if the directory exists, and create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.dataFrame.to_excel(path, index=False)

    def write_json(self, path, data):
        directory = os.path.dirname(path)
        # Check if the directory exists, and create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'w') as f:
            json.dump(data, f)
