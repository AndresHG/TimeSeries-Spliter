
import sys
import os
import random
import shutil
from pprint import pprint

src = "/home/andres/Imágenes/Legitimo_Users"
dest = os.path.join(os.getcwd(), "Results/Users")
granularity = "30000"
path_ddos = "/home/andres/Imágenes/Ataques"

def split_users(src, dest, path_ddos, granularity):

    users_ts = {}
    for user in os.listdir(src):
        tmp_src = os.path.join(src, user)
        tmp_dest = os.path.join(dest, user)
        os.mkdir(tmp_dest)
        # users_ts[user] = []
        for ts in os.listdir(tmp_src):
            users_ts[ts] = user
    # pprint(users_ts)

    src = os.path.join(os.getcwd(), "Results/Divider")
    for ts in os.listdir(src):
        if ts in users_ts:
            src_ts = os.path.join(src, ts)
            dest_path_user = os.path.join(dest, users_ts[ts])
            for ts_file in os.listdir(src_ts):
                if granularity == ts_file.split("-")[-1].split("_")[0]:
                    path_ts_file = os.path.join(src_ts, ts_file)
                    now_dest = ts_file.split("-")[3]
                    if now_dest == "LOIC":
                        now_dest = ts_file.split("-")[6]
                    if now_dest == "TimeStamps":
                        continue
                    now_dest = os.path.join(dest_path_user, now_dest)
                    if not os.path.exists(now_dest):
                        os.mkdir(now_dest)
                    now_dest = os.path.join(now_dest, 'Legitimo')
                    if not os.path.exists(now_dest):
                        os.mkdir(now_dest)
                    now_dest = os.path.join(now_dest, ts_file)
                    shutil.copyfile(path_ts_file, now_dest)

    for ts in os.listdir(path_ddos):
        path_ts = os.path.join(path_ddos, ts)
        for ts_file in os.listdir(path_ts):
            if granularity == ts_file.split("-")[-1].split("_")[0]:
                path_ts_file = os.path.join(path_ts, ts_file)
                metric = ts_file.split("-")[3]
                if metric == "LOIC":
                    metric = ts_file.split("-")[6]
                if metric == 'TimeStamps':
                    continue
                for user in os.listdir(dest):
                    now_dest = os.path.join(dest, user)
                    now_dest = os.path.join(now_dest, metric)
                    now_dest = os.path.join(now_dest, 'tmp')
                    if not os.path.exists(now_dest):
                        os.mkdir(now_dest)
                    now_dest = os.path.join(now_dest, ts_file)
                    shutil.copyfile(path_ts_file, now_dest)

    typeh = 'DDoS'
    for user in os.listdir(dest):
        path_user = os.path.join(dest, user)

        if granularity == "15000":
            mutations = 6
        else:
            mutations = 12

        for metric in os.listdir(path_user):
            path_metric = os.path.join(path_user, metric)
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

                    if granularity == "15000":
                        data_ddos = data_legitimo + data_tmp
                    else:
                        data_ddos = data_legitimo + data_tmp + data_tmp

                    if len(data_ddos) > 20:
                        with open(file_ddos, "w+") as f:
                            f.writelines("\n".join(list(data_ddos)))

            shutil.rmtree(path_tmp)

if __name__ == '__main__':

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    split_users(src, dest, path_ddos, granularity)