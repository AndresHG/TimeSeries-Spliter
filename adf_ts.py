


import sys
import os
import shutil
from pandas import Series
from statsmodels.tsa.stattools import adfuller
from pprint import pprint

def split_timeseries(src, dest):

    if not os.path.isdir(dest):
        os.mkdir(dest)
    else:
        shutil.rmtree(dest)
        os.mkdir(dest)

    for dir in os.listdir(src):

        now_src = os.path.join(src, dir)
        if not os.path.isdir(now_src):
            continue

        for file in os.listdir(now_src):

            static_src = os.path.join(now_src, file)

            with open(static_src, "r") as fileno:
                data = fileno.readlines()

            X = [float(x.strip()) for x in data]
            result = adfuller(X)
            print('ADF Statistic: {}'.format(result[0]))
            print('p-value: {}'.format(result[1]))
            # print('Critical Values:')
            # for key, value in result[4].items():
            #     print('\t%s: %.3f' % (key, value))


if __name__ == '__main__':

    src = sys.argv[1]
    dest = os.path.join(os.getcwd(), "Results/ADF")
    split_timeseries(src, dest)