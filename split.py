

import sys
import os
import shutil
import random
from pprint import pprint

def split_timeseries(src, dest, typeh):

    if not os.path.isdir(dest):
        os.mkdir(dest)
    else:
        if typeh != 'tmp':
            shutil.rmtree(dest)
            os.mkdir(dest)

    for dir in os.listdir(src):

        now_src = os.path.join(src, dir)
        if not os.path.isdir(now_src):
            continue

        for file in os.listdir(now_src):
            granularity = file.split("-")[-1].split("_")[0]
            static_dest = os.path.join(dest, granularity)
            if not os.path.exists(static_dest):
                os.mkdir(static_dest)
            static_src = os.path.join(now_src, file)

            if not os.path.exists(static_dest):
                os.mkdir(static_dest)
            shutil.copyfile(static_src, os.path.join(static_dest, file))

    for dir in os.listdir(dest):
        this_src = os.path.join(dest, dir)
        for file in os.listdir(this_src):
            if os.path.isdir(os.path.join(this_src, file)):
                continue
            now_dest = file.split("-")[3]
            if now_dest == "LOIC":
                now_dest = file.split("-")[6]
            if now_dest == "TimeStamps":
                continue
            now_dest = os.path.join(this_src, now_dest)
            if not os.path.isdir(now_dest):
                os.mkdir(now_dest)
            now_dest = os.path.join(now_dest, typeh)
            if not os.path.isdir(now_dest):
                os.mkdir(now_dest)
            this_file = os.path.join(this_src, file)
            shutil.copyfile(this_file, os.path.join(now_dest, file))
            # Use this only if you want to delete dest folder
            os.remove(this_file)

    if typeh.lower() == 'tmp': # Las series legitimas deben estar parseadas
        typeh = 'DDoS'
        for granularity in os.listdir(dest):
            path_granularity = os.path.join(dest, granularity)

            if granularity == "15000":
                mutations = 6
            else:
                mutations = 12

            for metric in os.listdir(path_granularity):
                path_metric = os.path.join(path_granularity, metric)
                path_tmp = os.path.join(path_metric, 'tmp')
                path_legitimo = os.path.join(path_metric, 'Legitimo')
                path_ddos = os.path.join(path_metric, 'DDoS')
                if not os.path.isdir(path_ddos):
                    os.mkdir(path_ddos)

                for filename_legitimo in os.listdir(path_legitimo):
                    file_legitimo = os.path.join(path_legitimo, filename_legitimo)
                    ddos_ts_used = []

                    for contador in range(0, mutations):

                        filename_tmp = random.choice(os.listdir(path_tmp))
                        while filename_tmp in ddos_ts_used:
                            filename_tmp = random.choice(os.listdir(path_tmp))
                        ddos_ts_used.append(filename_tmp)

                        data_ddos = []
                        data_tmp = []
                        data_legitimo = []
                        file_tmp = os.path.join(path_tmp, filename_tmp)

                        with open(file_legitimo, "r") as f:
                            data_legitimo = f.read().splitlines()
                        with open(file_tmp, "r") as f:
                            data_tmp = f.read().splitlines()

                        file_ddos = os.path.join(path_ddos, filename_legitimo + "--" + filename_tmp)

                        # if granularity == "15000":
                        #     data_ddos = data_legitimo + data_tmp
                        # else:
                        data_ddos = data_legitimo + data_tmp + data_tmp


                        if len(data_ddos) > 20:
                            with open(file_ddos, "w+") as f:
                                f.writelines("\n".join(list(data_ddos)))

                shutil.rmtree(path_tmp)


if __name__ == '__main__':

    src = sys.argv[1]
    if sys.argv[2].lower() == 'ddos':
        typeh = 'tmp'
    else:
        typeh = 'Legitimo'
    dest = os.path.join(os.getcwd(), "Results/Split")
    split_timeseries(src, dest, typeh)