"""
Example code of how to read and write vehicle parameters using pymavlink
"""

import time
# Import mavutil
from pymavlink import mavutil

# Create the connection to cube
connection = mavutil.mavlink_connection("COM13", baud=57600)
# Wait a heartbeat before sending commands
connection.wait_heartbeat()

# Request parameter
connection.mav.param_request_read_send(
    connection.target_system, connection.target_component,
    b'NTF_BUZZ_VOLUME',
    -1
)

# Print old parameter value
message = connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
# if message is NTF_BUZZER_VOLUME print value
if message is not None:
    print(message['param_id'])
    print(message['param_value'])

time.sleep(1)

# Set parameter value
# Set a parameter value TEMPORARILY to RAM. It will be reset to default on system reboot.
# Send the ACTION MAV_ACTION_STORAGE_WRITE to PERMANENTLY write the RAM contents to EEPROM.
# The parameter variable type is described by MAV_PARAM_TYPE in http://mavlink.org/messages/common.
connection.mav.param_set_send(
    connection.target_system, connection.target_component,
    b'NTF_BUZZ_VOLUME',
    2,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

# Read ACK
# IMPORTANT: The receiving component should acknowledge the new parameter value by sending a
# param_value message to all communication partners.
# This will also ensure that multiple GCS all have an up-to-date list of all parameters.
# If the sending GCS did not receive a PARAM_VALUE message within its timeout time,
# it should re-send the PARAM_SET message.
message = connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
if message is not None:
    print(message['param_id'])
    print(message['param_value'])

time.sleep(1)

# Request parameter value to confirm
connection.mav.param_request_read_send(
    connection.target_system, connection.target_component,
    b'NTF_BUZZ_VOLUME',
    -1
)

# Print new value in RAM
message = connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
if message is not None:
    print(message['param_id'])
    print(message['param_value'])

connection.reboot_autopilot()
