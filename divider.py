
import sys
import os
import shutil
from pprint import pprint

def split_timeseries(src_here, dest, steps):

    if not os.path.isdir(dest):
        os.mkdir(dest)

    for dir in os.listdir(src_here):

        dest_now = os.path.join(dest, dir)
        if not os.path.isdir(dest_now):
            os.mkdir(dest_now)
        else:
            shutil.rmtree(dest_now)
            os.mkdir(dest_now)

        src = os.path.join(src_here, dir)

        for filename in os.listdir(src):
            file = os.path.join(src, filename)
            if not os.path.isdir(file):
                with open(file, 'r') as f:
                    data = f.readlines()
                    data = [x.strip() for x in data]
                cont = 0
                for i in range(0, len(data), steps):
                    if len(data[i: i + steps]) == steps:
                        destino = os.path.join(dest_now, filename + "_" + str(cont))
                        with open(destino, 'w+') as fileno:
                            fileno.writelines("\n".join(list(data[i: i + steps])))
                    cont += 1

        if len(os.listdir(dest_now)) == 0:
            shutil.rmtree(dest_now)

if __name__ == '__main__':

    src = sys.argv[1]
    dest = os.path.join(os.getcwd(),"Results/Divider")
    steps = int(sys.argv[2])
    split_timeseries(src, dest, steps)