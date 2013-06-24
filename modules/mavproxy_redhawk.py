#!/usr/bin/env python
'''
RedHawk mavproxy bridge
Seth Lakowske
June 2013
'''

def name():
    '''return module name'''
    return 'RedHawk bridge'

def description():
    '''return module description'''
    return 'Connects mavproxy to RedHawk'

def init(_mpstate):
    '''initialise module'''
    global mpstate
    mpstate = _mpstate
    mpstate.antenna_state = module_state()
    mpstate.command_map['antenna'] = (cmd_antenna, "antenna link control")

def unload():
    '''unload module'''
    pass

def mavlink_packet(m):
    '''handle an incoming mavlink packet'''
    state = mpstate.antenna_state
    
    if m.get_type() == 'GPS_RAW' and state.gcs_location is not None:
        #send m.lat m.lon m.alt
        (gcs_lat, gcs_lon) = state.gcs_location
        bearing = cuav_util.gps_bearing(gcs_lat, gcs_lon, m.lat, m.lon)
    elif m.get_type() == 'GPS_RAW_INT' and state.gcs_location is not None:
        (gcs_lat, gcs_lon) = state.gcs_location
        bearing = cuav_util.gps_bearing(gcs_lat, gcs_lon, m.lat/1.0e7, m.lon/1.0e7)

