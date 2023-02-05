# Filetobitstream and BitstreamtoFile
# chenkj@ustc.edu.cn

import os
import libnum
import base64
import numpy as np



def file2mess(mess_path):
    _, filename = os.path.split(mess_path)                          # Filename
    ext = filename.split('.')[-1]                                   # Ext
    ext_bin = libnum.s2b(ext).zfill(32)                             # Ext_bin
    with open(mess_path, 'rb') as f:
        file_data = f.read()
        file_data_b64 = base64.b64encode(file_data)
    file_data_bin = libnum.s2b(file_data_b64)                       # mess bin
    mess_len_bin = libnum.s2b(str(len(file_data_bin))).zfill(160)    # mess len

    ext_list = ext_bin.replace('', ' ')[1:-1].split(' ')            # extbin len (32位)
    mess_len_list = mess_len_bin.replace('', ' ')[1:-1].split(' ')  # messbin len(160位)
    file_data_list = file_data_bin.replace('', ' ')[1:-1].split(' ')

    mess = np.array(ext_list + mess_len_list + file_data_list).astype(int)
    return mess


def mess2file(mess, save_path='.', save_name='rec'):
    mess_str = ''
    for i in range(len(mess)):
        mess_str = mess_str + str(int(mess[i]))
    ext_bin = mess_str[:32]
    mess_len_bin = mess_str[32:192]
    ext = str(libnum.b2s(ext_bin).decode('utf-8'))
    mess_len = str(libnum.b2s(mess_len_bin).decode('utf-8'))
    mess_bin = mess_str[192:192 + int(mess_len)]
    mess_b64 = libnum.b2s(mess_bin)
    with open(os.path.join(save_path, save_name + '.' + ext), 'wb') as f:
        mess = base64.b64decode(mess_b64)
        f.write(mess)
    return os.path.join(save_path, save_name + '.' + ext)

mess_path = 'filetransfer/1.tex'
mess = file2mess(mess_path)
mess2file(mess)
