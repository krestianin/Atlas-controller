# from pyModbusTCP.client import ModbusClient

# IP_ADDRESS = '172.18.1.11'
# PORT = 502
# REGISTER = 5

# client = ModbusClient(host=IP_ADDRESS, port=PORT,unit_id=1, auto_open=True)
# print(client)
# response = client.read_holding_registers(REGISTER, 1) 

# print(response)
# if response:
#     print("Register Values:", response)
# else:
#     print("Failed to read registers")

# # if response.isError():
# #     print("Error reading register")
# # else:
# #     temperature = response.registers[0]
# #     if temperature == 0x7FFF:  # sensor error value 
# #         print("Sensor error")
# #     else:
# #         print(f"Current temperature: {temperature / 10.0}°C")  # Adjust scaling factor based on documentation

# client.close()


from pyModbusTCP.client import ModbusClient

IP_ADDRESS = '172.18.1.11'
PORT = 502
REGISTER = 5  # speed value
ORIGINAL_VALUE = 5  # Hypothetical safe value

client = ModbusClient(host=IP_ADDRESS, port=PORT,unit_id=1, auto_open=True) 
response = client.read_holding_registers(REGISTER, 1) 
print(response)

# Write the original value back to the register to ensure no changes are made
success = client.write_single_register(REGISTER, 5)

if success:
    print("Write operation successful.")
else:
    print("Failed to write to register. Please check the connection and settings.")

client.close()