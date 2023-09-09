"""
Defintions for problem 0
"""

import numpy as np
import scipy.integrate
from scipy.integrate import DenseOutput
from scipy.interpolate import interp1d

class ForwardEulerOutput(DenseOutput):
    """
    Interpolate ForwardEuler output

    """
    def __init__(self, ts, ys):

        """
        store ts and ys computed in forward Euler method

        These will be used for evaluation
        """
        super(ForwardEulerOutput, self).__init__(np.min(ts), np.max(ts))
        self.interp = interp1d(ts, ys, kind='linear', copy=True)


    def _call_impl(self, t):
        """
        Evaluate on a range of values
        """
        return self.interp(t)
