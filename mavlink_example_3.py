from pymavlink import mavutil
import numpy as np

# Set up the connection to the Ardupilot SITL on TCP port 5762
connection = mavutil.mavlink_connection('tcp:127.0.0.1:5762')

# Wait for the heartbeat message to start being received
connection.wait_heartbeat()

# a function to receive roll angle from the autopilot
def get_roll_angle():
    # receive mavlink messages
    msg = connection.recv_match()
    # if no message, continue loop
    if not msg:
        return None
    # get ATTITUDE message
    if msg.get_type() == 'ATTITUDE':
        # return roll angle in degrees
        return np.degrees(msg.roll)
    

def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[channel_id - 1] = pwm
    connection.mav.rc_channels_override_send(
        connection.target_system,                # target_system
        connection.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.
    

def roll_to_rc_map(roll_angle):
    """ Map roll angle to RC channel pwm value
    Args:
        roll_angle (float): Roll angle in degrees
    Returns:
        rc_pwm (int): Channel pwm value 1100-1900
    """
    # map roll angle to pwm value
    rc_pwm = np.interp(roll_angle, [-180, 180], [1100, 1900])
    # return pwm value
    return rc_pwm


while True:
    # get roll angle
    roll_angle = get_roll_angle()
    # if no roll angle, continue loop
    if not roll_angle:
        continue
    print(f"Roll angle {roll_angle}")
    # map roll angle to pwm value
    rc_pwm = roll_to_rc_map(roll_angle)
    print(f"RC pwm {rc_pwm}")
    # set rc channel pwm value
    set_rc_channel_pwm(10, int(rc_pwm))
    
