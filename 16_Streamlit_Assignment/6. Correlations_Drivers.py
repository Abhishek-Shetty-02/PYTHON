from Utils.load_data import load_data
import numpy as np
import pandas as pd


df = load_data()

# Top 5 +Corr with TARGET (list)
# Top 5 −Corr with TARGET (list)
# Most correlated with Income
# Most correlated with Credit
# Corr(Income, Credit)
# Corr(Age, TARGET)
# Corr(Employment Years, TARGET)
# Corr(Family Size, TARGET)
# Variance Explained by Top 5 Features (proxy via |corr|)
# # Features with |corr| > 0.5