# coding: utf-8

import csv, re, datetime, os, sys, pickle, openpyxl

def exit():
    print()
    input('\nДля закрытия программы нажмите Enter...')
    sys.exit()

def check_phone_number(phone_number):
    return phone_number if (len(phone_number) == 5) or (phone_number[0:4] == '8651') else phone_number[5:]
    
def load_list_inet_tv(data, file_list):
    file_flag = False
    for file in file_list:
        if ('Список подключений ШПД + ТВ' in file) and (file.split('.')[-1] == 'csv'):
            file_flag = True
            try:
                with open(file, encoding='windows-1251') as f:
                    reader = csv.reader(f, delimiter=';')
                    for row in reader:        
                        if row[41] != 'deleted' \
                           and 'DSL' in row[37] \
                           and row[23] == 'SSG-подключение':
                            data[row[21]] = {'phone' : check_phone_number(row[7]), 'address' : row[6], 'mac' : '-',  'fio': row[5]} 
            except Exception as ex:
                print('Не удалось обработать файл {}:'.format(file))
                print(ex)
                exit()
    if file_flag is False:
        print('Не найден файл "Список подключений ШПД + ТВ"')
        exit()

def load_list_sessions(data, file_list):
    file_flag = False
    for file in file_list:
        if ('Абонентские сессии' in file) and (file.split('.')[-1] == 'csv'):
            file_flag = True
            try:
                with open(file, encoding='windows-1251') as f:
                    reader = csv.reader((line.replace('\0','') for line in f), delimiter=';')
                    
                    for row in reader:
                        if row[5] in data:
                            dt = datetime.datetime.strptime(row[0], "%d.%m.%Y %H:%M:%S")
                            if data[row[5]].get('date') is None:
                                data[row[5]]['date'] = dt
                            if data[row[5]]['date'] <= dt:
                                data[row[5]]['mac'] = re.search(r'MAC: (.+?)\s', row[6]).group(1).replace('.', '')
                                data[row[5]]['date'] = dt            
            except Exception as ex:
                print('Не удалось обработать файл {}:'.format(file))
                print(ex)
                exit()
    if file_flag is False:
        print('Не найдены файлы "Абонентские сессии"')
        exit()
        
def data_modify(data):
    result = {}
    for key in data:
        result[data[key]['mac']] = {'phone' : data[key]['phone'], \
                                    'address' : data[key]['address'], \
                                    'account' : key,  \
                                    'fio' : data[key]['fio']}
    return result

def read_list(name):
    try:
        with open('resources{}{}'.format(os.sep, name), 'br') as read_file:
                return pickle.load(read_file)
    except:
        return []

def print_table(data, dslam_mac):
    if dslam_mac.model == '5600':
        table_name = 'Huawei_5600.xlsx'
    elif dslam_mac.model ==  '5616':
        table_name = 'Huawei_5616.xlsx'
    else:
        print('{} - не знакомый тип DSLAM!'.format(dslam_mac.model))
        exit()
    
    try:
        wb = openpyxl.load_workbook('resources{}{}'.format(os.sep, table_name))
    except Exception as ex:
        print('Не удалось открыть шаблон {}'.format(table_name))
        print(ex)
        exit()
    sh_default = wb.get_sheet_by_name('Sheet1')
    for board in dslam_mac.boards:
        row = 6
        wb.copy_worksheet(sh_default)
        sh_current = wb.get_sheet_by_name('{} Copy'.format(sh_default.title))
        sh_current.title = 'Плата {}'.format(board)
        sh_current.cell(row = 1, column = 3).value = dslam_mac.ip
        sh_current.cell(row = 2, column = 3).value = dslam_mac.hostname
        sh_current.cell(row = 3, column = 3).value = board
        for port in dslam_mac.ports[board]:
            mac_flag = False
            for mac, vlan in port:
                if mac in data:
                    sh_current.cell(row = row, column = 2).value = data[mac]['phone']
                    sh_current.cell(row = row, column = 3).value = data[mac]['address']
                    sh_current.cell(row = row, column = 4).value = data[mac]['fio']
                    sh_current.cell(row = row, column = 5).value = data[mac]['account']
                    sh_current.cell(row = row, column = 6).value = '({}, {})'.format(mac, vlan)
                    mac_flag = True
                    break
            if mac_flag is False:
                sh_current.cell(row = row, column = 6).value = str(port).replace('[','').replace(']','').replace("'", '') if len(port) > 0 else ''
            row += 1
    wb.remove_sheet(sh_default)
    wb.save('out{}{} {}.xlsx'.format(os.sep,  dslam_mac.hostname, datetime.datetime.now().strftime('%d-%m-%y')))
