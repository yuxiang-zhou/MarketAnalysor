import numpy as np
import math
from scipy import stats

def get_slope(values):
    v_max = np.max(values)
    v_min = np.min(values)
    n_value = len(values)


    slope, intercept, r_value, p_value, std_err = stats.linregress(np.linspace(v_min, v_max, n_value), values)

    if math.isnan(slope):
        slope = 0
    return slope
