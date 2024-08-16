import socket
import json
import re 
from pyModbusTCP.client import ModbusClient
from scapy.all import IP, ICMP, sr1
import ipaddress 

# Функция для считывания температуры с машинок 
def fetch_temperature(host):
    # host = '10.11.1.42'  # IP address машинки
    port = 4028  # Port number
    command = {"id": 0, "jsonrpc": "2.0", "command": "stats"}

    # Получение данных с асика по порту port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(command).encode())
        response = b""
        while True:
            part = s.recv(4096)
            if not part:
                break
            response += part
        response = response.decode('utf-8')

    # Извлечь значения температур temp1, temp2, temp3 из ответа асика
    temperatures = re.findall(r'"temp\d+": (\d+)', response)
    # перевести string в int
    temperatures = [int(temp) for temp in temperatures]
    # Найти макс. температуру
    max_temp = max(temperatures) if temperatures else None
    return max_temp

# Пинг IP адреса. Функция не используется 
def ping_host(ip):
    try:
        socket.setdefaulttimeout(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((str(ip), 80))  # Подключвение к порту 80
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return False
    

# Скан сети для поиска рабочих адрессов от start_ip до end_ip, проверяя адреса вплоть до 10.11.х.last_host_digit
def scan_network(start_ip, end_ip, last_host_digit):
    """ Scan a custom IP range up to the last_host_digit in each subnet. """
    active_hosts = []
    start = ipaddress.IPv4Address(start_ip)
    last_host_digit = int(end_ip.split('.')[3]) 
    # sec_octet = int(end_subnet.split('.')[1]) # 2 октет подсети
    end_subnet = int(end_ip.split('.')[2])  # 3 октет подсети
    print(last_host_digit)
    # Проход по адресам 
    for sec_octet in range(int(start_ip.split('.')[1]), int(end_ip.split('.')[1]) + 1):
        for third_octet in range(int(start_ip.split('.')[2]), end_subnet + 1):
            end_ip = f"10.{sec_octet}.{third_octet}.{last_host_digit}"
            end = ipaddress.IPv4Address(end_ip)
            
            current_ip = ipaddress.IPv4Address(f"10.{sec_octet}.{third_octet}.0")
            while current_ip <= end:
                try:
                    # Пинг IP адреса по TCP протоколу, порт 80
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)  # Timeout for the socket operation

                        if s.connect_ex((str(current_ip), 80)) == 0:
                            active_hosts.append(str(current_ip))
                            print(f"Host {current_ip} is active.")
                except Exception as e:
                    print(f"Failed to connect to {current_ip}: {e}")
                current_ip = ipaddress.IPv4Address(int(current_ip) + 1)
    print(active_hosts)
    return active_hosts



# Функция, чтобы настроить скорость вентилятора
def set_fan_speed(fan_speed):
    IP_ADDRESS = '172.18.1.11' # IP контроллера 
    PORT = 502
    REGISTER = 5  # Регистр 5 контролирует скорость вентилятора
    client = ModbusClient(host=IP_ADDRESS, port=PORT, unit_id=1, auto_open=True)
    print(fan_speed)
    # if client.write_single_register(REGISTER, fan_speed):
    #     print(f"Fan speed set to {fan_speed}.")
    # else:
    #     print("Failed to write to register. Please check the connection and settings.")
    client.close()


# # Main 
# def main():
#     # Указать пул адресов и до какого адреса в каждой подсети проверять: К примеру, '10.11.1.42', '10.11.2', 70
#     hosts = scan_network('10.31.1.1', '10.32.3.5', 5)
#     temperatures = [fetch_temperature(host) for host in hosts if fetch_temperature(host) is not None]
#     if temperatures:
#         average_temp = sum(temperatures) / len(temperatures) 
#         print(average_temp)
#         # Изменить скорость в зависимости от средней максимальной температуры во всех машиках
#         if 63 <= average_temp:
#             fan_speed = 5
#             print('>=63')
#         elif 55 <= average_temp < 63:
#             fan_speed = 4
#             print('55-63')
#         else:
#             fan_speed = 3
#             print('<55')
#         set_fan_speed(fan_speed)
#     else:
#         print(f"Error: the temperature funciton didn't work properely")


# if __name__ == "__main__":
#     main()