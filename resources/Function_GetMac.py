# coding: utf8

import pickle, os, sys, time, configparser
from resources import DslamHuawei, Settings

#DslamHuawei.LOGGING = True

def exit():
    print()
    input('\nДля закрытия программы нажмите Enter...')
    sys.exit()

def connect_dslam(host):
    #Создание объекта dslam
    ip = host[0]
    model = host[1]
    for i in range(1, 4):
        print('Попытка подключения к {} №{}'.format(ip, i))
        if model == '5600':
            try:
                dslam = DslamHuawei.DslamHuawei5600(ip, Settings.login_5600, Settings.password_5600, 20)
            except:
                print('Не удалось подключиться к {}'.format(ip))
                if i == 3:
                    return None
                else:
                    time.sleep(60)
                    continue
        elif model == '5616':
            try:
                dslam = DslamHuawei.DslamHuawei5616(ip, Settings.login_5616, Settings.password_5616, 20)
            except:
                print('Не удалось подключиться к {}'.format(ip))
                if i == 3:
                    return None
                else:
                    time.sleep(60)
                    continue
        else:
            print('Не знакомый тип DSLAM {}'.format(ip))
            return None
        break
    return dslam

def update_mac(dslam_mac, dslam):
    for board in dslam.boards:
        for port in range(0, dslam.ports):
            dslam_mac.check_add_mac(board,  port,  dslam.get_mac_address_port(board,  port))
            

def run(dslam_mac):
    host = (dslam_mac.ip, dslam_mac.model)
    dslam = connect_dslam(host)
    print('Обработка {}'.format(dslam_mac.hostname))
    update_mac(dslam_mac, dslam)
    del dslam
    print('{} обработан'.format(dslam_mac.hostname))

def read_list(name):
    try:
        with open('resources{}{}'.format(os.sep, name), 'br') as read_file:
                return pickle.load(read_file)
    except:
        return []
            
def write_list(name, list_dslam_mac_addrress):
    with open('resources{}{}'.format(os.sep, name), 'bw') as write_file:
        pickle.dump(list_dslam_mac_addrress, write_file)
