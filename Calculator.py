# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 

@author: jdevore
"""

# Calculator.py

import pandas as pd
import numpy as np

def add_two_to_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds 2 to every numeric cell in the DataFrame.
    Non-numeric values are left unchanged.
    """
    return df.applymap(lambda x: x + 2 if isinstance(x, (int, float, np.number)) else x)


