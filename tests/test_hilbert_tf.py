import pytest
import numpy as np
from hilb.hilbert_transforms import get_slow_var
from hilb.hilbert_transforms import phase_from_hilbert
import os

def test_phase_from_hilbert():
    sr = 299
    bp = [6,30]
    x = np.arange(0, 10, 0.1)
    pos = np.sin(x)
    phs,_ = phase_from_hilbert(pos,sr,bp)
    tou = np.ndarray.flatten(np.load(os.path.join(os.path.dirname(__file__), 'hilbphasetest.npy')))
    np.testing.assert_allclose(tou[0:30], phs[0:30], atol=0.1)


def test_get_slow_var():
    amp_func = np.ptp #peak to peak
    sr = 299
    bp = [6,30]
    x = np.arange(0, 10, 0.1)
    pos = np.sin(x)
    phs,_ = phase_from_hilbert(pos,sr,bp)
    testamp = np.ndarray.flatten(np.load(os.path.join(os.path.dirname(__file__),'hilbamptest.npy')))

    amp,itop,ibot = get_slow_var(pos,phs,amp_func)

    np.testing.assert_allclose(testamp[0:30], amp[0:30], rtol=0.1)




if __name__ == "__main__":
    test_phase_from_hilbert()
    test_get_slow_var()
    print("Everything passed")