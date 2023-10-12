from pymavlink import mavutil

# Set up the connection to the Ardupilot SITL on TCP port 5762
connection = mavutil.mavlink_connection('tcp:127.0.0.1:5762')

# Wait for the heartbeat message to start being received
connection.wait_heartbeat()

while True:
    # receive mavlink messages
    msg = connection.recv_match()
    # if no message, continue loop
    if not msg:
        continue
    # get VFR_HUD message
    if msg.get_type() == 'HEARTBEAT':
        # print message
        print(msg)

