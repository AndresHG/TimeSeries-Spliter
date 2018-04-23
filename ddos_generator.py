

import sys
import os
import random
import shutil
from pprint import pprint

src = "/home/andres/Imágenes/Ataques-Fase3-Organizados-Carpeta-Tipo-Intensidad"
dest = os.path.join(os.getcwd(), "Results/DDoS")
src_legitimo = os.path.join(os.getcwd(), "Results/Divider")
granularity = "15000"
path_ddos = "/home/andres/Imágenes/Ataques"

def split_ddos(src, dest):

    # shutil.copytree(src, dest)
    for ddos_type in os.listdir(src):
        ddos_type_path = os.path.join(src, ddos_type)
        for ts in os.listdir(ddos_type_path):
            path_ts = os.path.join(ddos_type_path, ts)

            for ts_file in os.listdir(path_ts):
                if granularity == ts_file.split("-")[-1].split("_")[0]:
                    path_ts_file = os.path.join(path_ts, ts_file)
                    metric = ts_file.split("-")[3]
                    if metric == "LOIC":
                        metric = ts_file.split("-")[6]
                    if metric == 'TimeStamps':
                        continue
                    for user in os.listdir(src):
                        if ddos_type != user:
                            continue
                        now_dest = os.path.join(dest, user)
                        if not os.path.exists(now_dest):
                            os.mkdir(now_dest)
                        now_dest = os.path.join(now_dest, metric)
                        if not os.path.exists(now_dest):
                            os.mkdir(now_dest)
                        now_dest = os.path.join(now_dest, 'tmp')
                        if not os.path.exists(now_dest):
                            os.mkdir(now_dest)
                        now_dest = os.path.join(now_dest, ts_file)
                        shutil.copyfile(path_ts_file, now_dest)
            # shutil.rmtree(path_ts)

    accumulated = 0
    for dir in os.listdir(src_legitimo):
        this_src = os.path.join(src_legitimo, dir)
        # accumulated += (len(os.listdir(this_src))/13)/6
        # pprint('file: {} and len: {}'.format(this_src, accumulated))

        for ts_file in os.listdir(this_src):
            path_ts_file = os.path.join(this_src, ts_file)
            granu = ts_file.split("-")[-1].split("_")[0]
            if granu != granularity:
                continue

            metric = ts_file.split("-")[3]
            if metric == "LOIC":
                metric = ts_file.split("-")[6]
            if metric == "TimeStamps":
                continue
            for ddos_type in os.listdir(dest):
                path_ddos_type = os.path.join(dest, ddos_type)
                path_ddos_type_metric = os.path.join(path_ddos_type, metric)
                if not os.path.isdir(path_ddos_type_metric):
                    os.mkdir(path_ddos_type_metric)
                file_dest = os.path.join(path_ddos_type_metric, 'Legitimo')
                if not os.path.isdir(file_dest):
                    os.mkdir(file_dest)
                file_dest = os.path.join(file_dest, ts_file)
                shutil.copyfile(path_ts_file, file_dest)

    for user in os.listdir(dest):
        path_user = os.path.join(dest, user)

        # if granularity == "15000":
        #     mutations = 6
        # else:
        mutations = 6

        for metric in os.listdir(path_user):
            path_metric = os.path.join(path_user, metric)
            path_tmp = os.path.join(path_metric, 'tmp')
            path_legitimo = os.path.join(path_metric, 'Legitimo')
            path_ddos = os.path.join(path_metric, 'DDoS')
            if not os.path.isdir(path_ddos):
                os.mkdir(path_ddos)

            if mutations > len(os.listdir(path_tmp)):
                mutations = len(os.listdir(path_tmp))

            legitimas_to_merge = 100
            legitimas_used = []

            for cont_legitimo in range(0, legitimas_to_merge):

                filename_legitimo = random.choice(os.listdir(path_legitimo))
                while filename_legitimo in legitimas_used:
                    filename_legitimo = random.choice(os.listdir(path_legitimo))
                legitimas_used.append(filename_legitimo)

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

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    split_ddos(src, dest)