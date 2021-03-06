# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
from onset_detection import onset_detector
import numpy as np
import madmom
import os
import time
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from sklearn import preprocessing
from onset_selection import onset_selector
from matplotlib import animation


def main(path):
    myprocessor = onset_detector(2048, 441)

    # start = time.time()
    # sf, time_interval = myprocessor.spectralflux(path)
    # print("Running spectral flux use {} seconds.".format(time.time() - start))
    # print(sf.shape)
    # print(time_interval)

    # selector = onsetSel(sf[0, :], 10, 3, 3, 0.3, 0.8)
    # quantified = selector.find_peaks()

    # plt.figure()
    # fig,left_axis=plt.subplots()
    # right_axis = left_axis.twinx()
    # p1, = left_axis.plot(sf[0, : 2000])
    # p2, = right_axis.plot(quantified[0 :2000], 'r--')
    # right_axis.set_ylim(0, 5)
    # plt.savefig('sf.png')

    start = time.time()
    sf, time_interval = myprocessor.superflux(path, False)
    print("Running super flux use {} seconds.".format(time.time() - start))
    print(sf.shape)
    print(time_interval)

    selector = onset_selector(sf, 10, 3, 3, 0.3, 0.8)
    quantified = selector.find_peaks(intvl=20)

    plt.figure()
    fig,left_axis=plt.subplots()
    right_axis = left_axis.twinx()
    p1, = left_axis.plot(sf[0, : 2000])
    p2, = right_axis.plot(quantified[0, 0:2000], 'r--')
    right_axis.set_ylim(0, 5)
    plt.savefig('superflux.png')

    # start = time.time()
    # nwpd, time_interval = myprocessor.normalized_weighted_phase_deviation(path, True)
    # print("Running normalizaed weighted phase deviation use {} seconds.".format(time.time() - start))
    # print(nwpd.shape)
    # print(time_interval)
    # selector = onset_selector(nwpd[0, :], 10, 3, 3, 0.3, 0.8)
    # quantified = selector.find_peaks()
    #
    # plt.figure()
    # fig,left_axis=plt.subplots()
    # right_axis = left_axis.twinx()
    # p1, = left_axis.plot(nwpd[0, : 2000])
    # p2, = right_axis.plot(quantified[0 :2000], 'r--')
    # #right_axis.set_ylim(0, 5)
    # plt.savefig('nwpd.png')
    #
    # print(len(quantified))


    step = 100

    plt.figure()
    fig, left_axis = plt.subplots()
    right_axis = left_axis.twinx()
    # p1, = left_axis.plot(nwpd[0, : 2000])
    # p2, = right_axis.plot(quantified[0 :2000], 'r--')
    p1, = left_axis.plot([], [], lw=2)
    p2, = right_axis.plot([], [], 'r--')
    p3, = right_axis.plot([], [], 'g--')

    left_axis.set_xlim(0, step)
    right_axis.set_ylim(0, step)


    # left_axis.set_ylim(0, 0.00035)
    left_axis.set_ylim(0, 10)
    right_axis.set_ylim(0, 10)


    # fig = plt.figure()
    #different ax scale
    # ax = plt.axes(xlim=(0, step), ylim=(0, 10))
    # ax = plt.axes(xlim=(0, step), ylim=(0, 0.00035))

    # line, = ax.plot([], [], lw=2)

    # initialization function: plot the background of each frame
    def init():
        # line.set_data([], [])
        p1.set_data([], [])
        p2.set_data([], [])
        p3.set_data([], [])
        # return line,
        return p1, p2, p3

    # animation function.  This is called sequentially
    def animate(i):
        x = np.linspace(0, step, step)
        # line.set_data(x, sf[0, i:i + step])
        # line.set_data(x, quantified[0, i:i+step])

        p1.set_data(x, sf[0, i:i + step])
        p2.set_data(x, quantified[0, i:i + step])       #channel 1
        p3.set_data(x, quantified[1, i:i + step])       #channel 2
        return p1, p2, p3

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=2000, interval=0, blit=False)

    anim.save('animation_demon.mp4', fps=100, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == '__main__':
    main("../data/" + "beat_it.mp3")