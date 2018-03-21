# coding: utf-8

import os
from resources import Function_MakeTable

data = {}
file_list = ['in' + os.sep + x for x in os.listdir('in')]

Function_MakeTable.load_list_inet_tv(data, file_list)
Function_MakeTable.load_list_sessions(data, file_list)

data = Function_MakeTable.data_modify(data)

list_dslam_mac_addrress = Function_MakeTable.read_list('mac.db')
if len(list_dslam_mac_addrress) == 0:
    print('Запустите программу GetMac.py!')
    exit()

for dslam_mac in list_dslam_mac_addrress:
    Function_MakeTable.print_table(data, dslam_mac)

Function_MakeTable.exit()
