import numpy as np
import torch
from tools.utils.load_and_save import load_npy
from tools.config import paths, config
import matplotlib.pyplot as plt


def filter_by_bps(min_limit=None, max_limit=None):
    # return songs in difficulty range
    diff_ar = load_npy(paths.diff_ar_file)
    name_ar = load_npy(paths.name_ar_file)

    if min_limit is not None:
        selection = diff_ar > min_limit
        name_ar = name_ar[selection]
        diff_ar = diff_ar[selection]
    if max_limit is not None:
        selection = diff_ar < max_limit
        name_ar = name_ar[selection]
        diff_ar = diff_ar[selection]

    return list(name_ar), list(diff_ar)


def check_cuda_device():
    if not torch.cuda.is_available():
        print("No Cuda device detected. Continue?")
        input("Enter")
    return None


def plot_autoenc_results(img_in, img_repr, img_out, n_samples):
    bneck_reduction = len(img_repr.flatten()) / len(img_in.flatten()) * 100
    print(f"Bottleneck shape: {img_repr.shape}. Reduction to {bneck_reduction}%")
    print("Plot original images vs. reconstruction")
    fig, axes = plt.subplots(nrows=3, ncols=n_samples, figsize=(12, 4))

    # if scale_repr:
    #     img_repr -= img_repr.min()
    #     img_repr /= img_repr.max()

    # plot original image
    for idx in np.arange(n_samples):
        ax = fig.add_subplot(3, n_samples, idx + 1)
        plt.imshow(np.transpose(img_in[idx], (1, 2, 0)))

    # plot bottleneck distribution
    for idx in np.arange(n_samples):
        ax = fig.add_subplot(3, n_samples, idx + n_samples + 1)
        plt.imshow(np.transpose(img_repr[idx][:3], (1, 2, 0)))

    # plot output image
    for idx in np.arange(n_samples):
        ax = fig.add_subplot(3, n_samples, idx + 2*n_samples + 1)
        plt.imshow(np.transpose(img_out[idx], (1, 2, 0)))

    plt.show()
