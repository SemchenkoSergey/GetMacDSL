# coding: utf-8
from resources import DslamMacAddress, Function_GetMac, Settings
from concurrent.futures import ThreadPoolExecutor
import time, datetime

# Инициализация списка DSLAM с мак-адресами
list_dslam_mac_addrress = Function_GetMac.read_list('mac.db')
if len(list_dslam_mac_addrress) == 0:
    print('\n--- Создание объектов для хранения MAC-адресов ---')
    for host in Settings.hosts:
        dslam = Function_GetMac.connect_dslam(host)
        dslam_info = dslam.get_info()
        dslam_mac = DslamMacAddress.DslamMacAddress(dslam_info['model'], dslam_info['ip'], dslam_info['hostname'], dslam.boards, dslam.ports)
        #print('Обработка {}'.format(dslam_mac.hostname))
        #Function_GetMac.update_mac(dslam_mac, dslam)
        list_dslam_mac_addrress.append(dslam_mac)
        del dslam
        #print('{} обработан'.format(dslam_mac.hostname))
    Function_GetMac.write_list('mac.db', list_dslam_mac_addrress)

# Запуск основной программы
run_interval = int((24*60*60)/Settings.number_of_launches)
print('\n--- Запуск программы ---')
while True:
    current_time = datetime.datetime.now()    
    if 'run_time' in locals():
        if (current_time - run_time).seconds < run_interval:
            time.sleep(300)
            continue
    list_dslam_mac_addrress = Function_GetMac.read_list('mac.db')
    with ThreadPoolExecutor(max_workers=Settings.threads) as executor:
        executor.map(Function_GetMac.run, list_dslam_mac_addrress)
    
    print('***** Обработка завершена (время запуска {}) *****'.format(current_time.strftime('%H:%M')))
    Function_GetMac.write_list('mac.db', list_dslam_mac_addrress)
    run_time = current_time
