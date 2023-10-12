from pymavlink import mavutil

# Set up the connection to the Ardupilot SITL on TCP port 5762
connection = mavutil.mavlink_connection('tcp:127.0.0.1:5762')

# Wait for the heartbeat message to start being received
connection.wait_heartbeat()

# request data to be sent at the given rate

 
vdr_message_id = 74 # https://mavlink.io/en/messages/common.html#VFR_HUD 

def set_rate(message_id, frequency_hz):  
    """
    Request MAVLink message in a desired frequency,
    documentation for SET_MESSAGE_INTERVAL:
        https://mavlink.io/en/messages/common.html#MAV_CMD_SET_MESSAGE_INTERVAL

    Args:
        message_id (int): MAVLink message ID
        frequency_hz (float): Desired frequency in Hz

    """
    connection.mav.command_long_send(
    connection.target_system, connection.target_component, # don't worry about these too much
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, # mavutil message request 
    0,
    message_id, # The MAVLink message ID
    1e6 / frequency_hz, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
    0, 0, 0, 0, # Unused parameters
    0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )


set_rate(vdr_message_id, 10) # set to 10 hz


while True:
    # receive mavlink messages
    msg = connection.recv_match()
    # if no message, continue loop
    if not msg:
        continue
    # get VFR_HUD message
    if msg.get_type() == 'VFR_HUD':
        # print message
        print(msg.airspeed)