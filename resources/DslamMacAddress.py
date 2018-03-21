# coding: utf-8

class DslamMacAddress():
    def __init__(self,  model,  ip,  hostname, boards,  ports):
        self.model = model
        self.hostname = hostname
        self.ip = ip
        self.boards = tuple(boards)
        self.ports = {}
        for board in self.boards:
            self.ports[board] = tuple([[] for x in range(0,  ports)])
    
    def __str__(self):
        result = 'model: {}\nip: {}\nhostname: {}\nboards: {}\n'.format(self.model,  self.ip,  self.hostname,  self.boards)
        for board in self.boards:
            for idx,  port in enumerate(self.ports[board]):
                result += 'board: {}, port: {}, mac: {}\n'.format(board,  idx,  port)
        return result
    
    def add_mac(self,  board,  port,  mac,  vlan):
        self.ports[board][port].append((mac,  vlan))
        
    def check_add_mac(self,  board,  port,  mac_list):
        for mac in mac_list:
            check_vlan = mac[1]
            check_mac_adr = mac[0].replace('-',  '')
            check_result = False
            for current_mac_adr,  current_vlan in self.ports[board][port]:
                if current_mac_adr == check_mac_adr and current_vlan == check_vlan:
                    check_result = True
                    break
            if check_result is False:
                self.add_mac(board,  port,  check_mac_adr,  check_vlan)
