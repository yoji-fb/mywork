"""
v000 - Function created: mypdplot, mypyplot

"""
import numpy as np
import pandas as pd
from matplotlib import style
import matplotlib.dates as mdates
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import time
import os
import fnmatch
import xlsxwriter

plt.style.use('tableau-colorblind10')
plt.rcParams['axes.grid'] = True
plt.rcParams['xtick.bottom'] = 'False'
plt.rcParams['ytick.left'] = 'False'



# df.plot
def mypdplot(df, xlab='xlabel', ylab='ylabel', xlim=(None, None), ylim=(None, None), color=0, legend=True, save=(False, None)):
    # plt.figure(figsize=(12,8))
    if color == 0:
        df.plot(grid=True)
    # elif color == 1:
    #     df.plot(grid=True, )

    # xlab #
    plt.xlabel(xlab)
    # ylab #
    plt.ylabel(ylab)
    # xlim #
    if xlim == (None, None):
        plt.xlim(df.index[0], df.index[-1])
    else:
        plt.xlim(xlim[0], xlim[1])
    # ylim #
    if ylim == (None, None):
        pass
    else:
        plt.ylim(ylim[0], ylim[1])
    # legend #
    if legend:
        plt.legend(loc='upper left', ncol=2, fontsize=8)
    # save #
    if save[0]:
        plt.savefig(save[1])


# pyplot
def mypyplot(df, x=False, xlab='xlabel', ylab='ylabel', xlim=(None, None), ylim=(None, None), color=0, legend=True, save=(False, None)):

    n = len(df.columns)  # #variable n below should be number of curves to plot
    if color == 0:  # Default
        plt.figure(figsize=(12,8))
        for i in range(n):
            if x == False:
                plt.plot(df.index, df.iloc[:, i], label=df.columns[i])
            else:
                plt.plot(x, df.iloc[:, i], label=df.columns[i])
    elif color == 1:  # 'jet_r'  # https://stackoverflow.com/questions/28465028/pyplot-matplotlib-line-plot-same-color
        cmap = plt.get_cmap('jet_r')
        plt.figure()
        for i in range(n):
            color=cmap(float(i)/n)
            if x == False:
                plt.plot(df.index, df.iloc[:, i], label=df.columns[i], c=color)
            else:
                plt.plot(x, df.iloc[:, i], label=df.columns[i], c=color)

    # xlab #
    plt.xlabel(xlab)
    # ylab #
    plt.ylabel(ylab)
    # xlim #
    if xlim == (None, None):
        if x == False:
            plt.xlim(df.index[0], df.index[-1])
        else:
            plt.xlim(x[0], x[-1])
    else:
        plt.xlim(xlim[0], xlim[1])
    # ylim #
    if ylim == (None, None):
        pass
    else:
        plt.ylim(ylim[0], ylim[1])
    # legend #
    if legend:
        plt.legend(loc='upper left', ncol=2, fontsize=8)
    # save #
    if save[0]:
        plt.savefig(save[1])




