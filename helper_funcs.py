import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage import gaussian_filter


def produce_scoring(model, data_pairs, data_pair_labels=None, threshold=0.5):
    make_binary = np.vectorize(lambda x: 1 if x >= threshold else 0)
    fig, ax = plt.subplots(1,len(data_pairs))

    for i, (X, y) in enumerate(data_pairs):
        preds = model.predict(X, verbose=0)
        ConfusionMatrixDisplay.from_predictions(y, make_binary(preds),
                                                ax=ax[i],
                                                colorbar=False,
                                                cmap="binary")
        ax[i].set_title(data_pair_labels[i])


def plot_heatmap(d, attr1, attr2):
    int_rt = d[attr1]
    fico = d[attr2]

    heatmap, xedges, yedges = np.histogram2d(int_rt, fico, bins=1000)
    heatmap = gaussian_filter(heatmap, sigma=16)

    x_vals = np.linspace(np.min(int_rt), np.max(int_rt), 1000)
    y_vals = np.linspace(np.min(fico), np.max(fico), 1000)
    X, Y = np.meshgrid(x_vals, y_vals)


    int_rt_default = int_rt[d["loan_status"]==0]
    fico_default = fico[d["loan_status"]==0]
    heatmap2, xedges2, yedges2 = np.histogram2d(int_rt_default, fico_default, bins=20)

    x_valsd = np.linspace(np.min(int_rt_default), np.max(int_rt_default), 20)
    y_valsd = np.linspace(np.min(fico_default), np.max(fico_default), 20)
    Xd, Yd = np.meshgrid(x_valsd, y_valsd)

    levels = np.arange(4, 32, 4)

    fig, ax = plt.subplots()

    scale_func = lambda a : 1/( 1+np.exp(-(7*a-4) ) )

    cs = ax.contourf(X, Y, heatmap.T, levels=10, cmap="Blues")

    for i in range(2, len(levels), 2):
        ax.contourf(Xd, Yd, heatmap2.T, levels=levels[i-2:i+1], colors="orange", alpha=scale_func((i)/7))

    ax.set_xlim((2,6))
    ax.set_ylim((600,820))
    ax.set_xlabel("Interest Rate")
    ax.set_ylabel("Fico Score")
    plt.show()