import pandas as pd
import numpy as np


# Select features for transformation
def generate_profit_for_one_shop(shop):
    features = ['bld_t', 'pop_tot', 'pop_den', 'pop_ax_t', 'poc_tot', 'iahu_x']
    if shop[features[0]] and shop[features[1]]:
        return np.pow(np.log1p(np.float64(shop[features[0]])) * np.sqrt(np.float64(shop[features[1]])), 3)
