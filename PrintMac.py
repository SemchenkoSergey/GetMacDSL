# coding: utf-8

from resources import DslamMacAddress
import datetime,  os,  pickle,  sys

try:
    with open('resources{}{}'.format(os.sep, 'mac.db'), 'br') as read_file:
        list_dslam_mac_addrress  = pickle.load(read_file)
except:
    print()
    input('\nНе удалось прочитать файл "mac.db"...')
    sys.exit()

while True:
    for idx, dslam in enumerate(list_dslam_mac_addrress,  start=0):
        print('{}. {}'.format(idx,  dslam.hostname))
    while True:
        try:
            input_number = int(input('\nВведите номер: '))
        except:
            print('Введите число!')
            continue
        if input_number not in range(0,  len(list_dslam_mac_addrress)):
            print('Число не входит в диапазон!')
            continue
        break
    print()
    with open('out{}{} {}.txt'.format(os.sep, list_dslam_mac_addrress[input_number].hostname,  datetime.datetime.now().strftime('%H-2%M %d-%m-%y')),  'w') as out_file:
        out_file.write(str(list_dslam_mac_addrress[input_number]))
    print(list_dslam_mac_addrress[input_number])
    input_str = input('Для продолжения нажмите "Enter", для выхода наберите "exit": ')
    if input_str == 'exit':
        break
