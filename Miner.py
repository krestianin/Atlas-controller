import requests

# Assuming you have an endpoint to get miner info
# response = requests.get('http://10.13.5.19/temp')
# response = requests.get('https://api.emcd.io/v1/btc/workers/10.46.10.18')
# miner_info = response.json()  # This will contain the JSON data from the miner


# url = f"http://10.11.1.22/api/getinfostats"
# try:
#     response = requests.get(url, verify=False)  # Disable SSL certificate verification

#     response.raise_for_status()
#     print(response.json() )  # Assuming the API returns JSON data
# except requests.RequestException as e:
#     print(f"Error fetching data from : {e}")

import socket
import json
import re 
from pyModbusTCP.client import ModbusClient
from scapy.all import IP, ICMP, sr1
import ipaddress 

host = '10.11.1.42'  # IP address машинки
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
    print(response)

# Извлечь все значения температур temp1, temp2, temp3 из ответа асика
temperatures = re.findall(r'"temp\d+": (\d+)', response)
# перевести string в int
temperatures = [int(temp) for temp in temperatures]
# Найти макс. температуру
max_temp = max(temperatures) if temperatures else None
print(max_temp)

# import socket
# import json

# data = json.dumps({"id": 0, "jsonrpc": "2.0", "command": "stats"})
# host = '10.46.10.18'  # IP address of the miner
# port = 4028  # Port number for JSON-RPC
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((host, port))
#     s.sendall(data.encode())
#     response = s.recv(4096)
#     decoded_response = response.decode()
#     json_response = json.loads(decoded_response)
#     # Assuming temperature is reported as 'temp_chip1' in the "STATS" part of the JSON
#     temp_chip1 = int(json_response['STATS'][0]['temp_chip1'].split('-')[1])  # Extract max temperature from the range
#     print(temp_chip1)



# import socket
# import json

# data = json.dumps({"id": 0, "jsonrpc": "2.0", "command": "stats"})
# host = '10.11.1.42'  # IP address of the device
# port = 4028  # Port number

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((host, port))
#     s.sendall(data.encode())
#     response = s.recv(4096)
#     decoded_response = response.decode()
#     # json_response = json.loads(decoded_response)
#     # Assuming temperature is reported as 'temp_chip1' in the "STATS" part of the JSON
#     temp_chip1 = int(decoded_response[0][0]['temp_chip1'].split('-')[1])  # Extract max temperature from the range
#     print(temp_chip1)



# def fetch_temperature():
#     data = json.dumps({"id": 0, "jsonrpc": "2.0", "command": "stats"})
#     host = '10.11.2.62'  # IP address of the miner
#     port = 4028  # Port number for JSON-RPC
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((host, port))
#         s.sendall(data.encode())
#         response = s.recv(4096)
#         decoded_response = response.decode()
#         json_response = json.loads(decoded_response)
#         # Assuming temperature is reported as 'temp_chip1' in the "STATS" part of the JSON
#         temp_chip1 = int(json_response['STATS'][0]['temp_chip1'].split('-')[1])  # Extract max temperature from the range
#         return temp_chip1
