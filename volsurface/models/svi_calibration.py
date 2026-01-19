import numpy as np 
from scipy.optimize import minimize
from volsurface.models.svi import svi_total_variance

def calibrate_svi (F , strikes , T, vols ):
    k = np.log(np.array(strikes)/F)
    w_mkt = vols**2*T

    def obj(x): 
        return np.mean((svi_total_variance(k , *x) - w_mkt)**2)

        res = minimize(obj, [0.01, 0.01, 0.01, 0.01, 0.01], bounds=[(0, None), (0, None), (-1, 1), (0, None), (0, None)])
        return dict(a=res.x[0], b=res.x[1], rho=res.x[2], m=res.x[3], sigma=res.x[4])
