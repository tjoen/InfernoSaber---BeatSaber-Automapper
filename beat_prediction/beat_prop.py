import numpy as np
import aubio
import madmom
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter

from tools.config import config


def get_beat_prop(x_song):
    # get volume through absolute frequency values
    set_a = volume_check(x_song)
    set_a = tcn_reshape(set_a)

    set_b = onset_detection(x_song)
    set_b = tcn_reshape(set_b)

    return [set_a, set_b]


def tcn_reshape(ar):
    tcn_len = config.tcn_len
    ar_out = np.zeros((len(ar) - tcn_len, tcn_len))
    for idx in range(len(ar) - tcn_len):
        ar_out[idx] = ar[idx:idx+tcn_len]

    ar_out.reshape(ar_out.shape[0], ar_out.shape[1], 1)
    return ar_out


def volume_check(x_song):
    volume = np.zeros(x_song.shape[1])
    for idx in range(len(volume)):
        volume[idx] = x_song[:, idx].sum()
    # normalize
    volume -= volume.min()
    volume /= volume.max()
    return volume


def onset_detection(x_song):
    x_song = x_song.T
    # sf = madmom.features.onsets.spectral_flux(x_song)
    # calculate the difference
    diff = np.diff(x_song, axis=0)
    # keep only the positive differences
    pos_diff = np.maximum(0, diff)
    # sum everything to get the spectral flux
    sf = np.sum(pos_diff, axis=1)
    sf -= sf.min()
    sf /= sf.max()
    sf = np.hstack((np.zeros(1), sf))

    # # maximum filter size spreads over 3 frequency bins
    # size = (1, 3)
    # max_spec = maximum_filter(x_song, size=size)
    # diff = np.zeros_like(x_song)
    # diff[1:] = (x_song[1:] - max_spec[: -1])
    # pos_diff = np.maximum(0, diff)
    # superflux = np.sum(pos_diff, axis=1)
    # superflux -= superflux.min()
    # superflux /= superflux.max()
    #
    # fig = plt.figure()
    # plt.plot(sf, label='sf')
    # plt.plot(superflux, linestyle='dashed', label='superflux')
    # plt.legend()
    # plt.show()

    return sf
