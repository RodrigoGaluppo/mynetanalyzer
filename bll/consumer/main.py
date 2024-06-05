import configparser
from flask import Flask
from flask_socketio import SocketIO, emit
from Global import sessionMaker
from models.TimeSeriesPacket import TimeSeriesPacket
from controllers.MainPacket import (
    handle_packet_count_by_ip, 
    handle_request_data_30, 
    handle_request_data_60,
    handle_request_data_12h, 
    handle_request_data_24h, 
    handle_request_data_dest_ports, 
    handle_request_data_source_ports, 
    handle_request_data_protocols,
    main_connect,main_disconnect, 
    handle_packet_host_by_source_packets, 
    handle_packet_size_by_ip,
    handle_request_data_24_hour_sum,
    handle_request_data_24_hours_total_packet_count
)

from controllers.HostPacket import (
    handle_request_data_30_host, 
    handle_request_data_60_host,
    handle_request_data_12h_host, 
    handle_request_data_24h_host, 
    handle_request_data_dest_ports_host, 
    handle_request_data_source_ports_host, 
    handle_request_data_protocols_host,
    handle_top_destinations_by_packet_count,
    handle_top_sources_by_packet_count,
    handle_request_data_24_hour_sum_host,
    handle_request_data_24_hours_total_packet_count_host
)

# Load configuration from default.conf file
config = configparser.ConfigParser()
config.read('default.conf')

# Read configuration parameters from the file
socketio_server_port = config.getint('DEFAULT', 'socketio_server_port')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

socketio.on("hello",namespace="/main")
def d():
    print("hello")

# MAIN
@socketio.on('connect', namespace='/main')
def func():
    main_connect()

@socketio.on('disconnect', namespace='/main')
def func():
    main_disconnect()

@socketio.on('request_data_24_hours_sum', namespace='/main')
def func():
    handle_request_data_24_hour_sum()

@socketio.on('request_data_24_hours_total_packet_count', namespace='/main')
def func():
    handle_request_data_24_hours_total_packet_count()

@socketio.on('request_data_30', namespace='/main')
def func():
    handle_request_data_30()
    
@socketio.on('request_data_60', namespace='/main')
def func():
    handle_request_data_60()

@socketio.on('request_data_12h', namespace='/main')
def func():
    handle_request_data_12h()

@socketio.on('request_data_24h', namespace='/main')
def func():
    handle_request_data_24h()

@socketio.on('request_data_protocols', namespace='/main')
def func():
    handle_request_data_protocols()

@socketio.on('request_data_sourceports', namespace='/main')
def func():
    handle_request_data_source_ports()

@socketio.on('request_data_destports', namespace='/main')
def func():
    handle_request_data_dest_ports()

@socketio.on('request_host_by_number_packets', namespace='/main')
def func():
    handle_packet_count_by_ip()

@socketio.on('request_host_by_size_packets', namespace='/main')
def func():
    handle_packet_size_by_ip()

@socketio.on('request_host_by_source_packets', namespace='/main')
def func():
    handle_packet_host_by_source_packets()
    
   

# Host
@socketio.on('request_data_24_hours_sum_host', namespace='/main')
def func(parameters):
    handle_request_data_24_hour_sum_host(parameters.get("ip"))

@socketio.on('request_data_24_hours_total_packet_count_host', namespace='/main')
def func(parameters):
    handle_request_data_24_hours_total_packet_count_host(parameters.get("ip"))

@socketio.on('request_data_30_host', namespace='/main')
def func(parameters):
    handle_request_data_30_host(parameters.get("ip"))

@socketio.on('request_data_60_host', namespace='/main')
def func(parameters):
    handle_request_data_60_host(parameters.get("ip"))

@socketio.on('request_data_12h_host', namespace='/main')
def func(parameters):
    handle_request_data_12h_host(parameters.get("ip"))

@socketio.on('request_data_24h_host', namespace='/main')
def func(parameters):
    handle_request_data_24h_host(parameters.get("ip"))

@socketio.on('request_data_protocols_host', namespace='/main')
def func(parameters):
    handle_request_data_protocols_host(parameters.get("ip"))

@socketio.on('request_data_sourceports_host', namespace='/main')
def func(parameters):
    handle_request_data_source_ports_host(parameters.get("ip"))

@socketio.on('request_data_destports_host', namespace='/main')
def func(parameters):
    handle_request_data_dest_ports_host(parameters.get("ip"))

@socketio.on('request_top_sources_by_packet_count', namespace='/main')
def func(parameters):
    handle_top_sources_by_packet_count(parameters.get("ip"))

@socketio.on('request_top_destinations_by_packet_count', namespace='/main')
def func(parameters):
    handle_top_destinations_by_packet_count(parameters.get("ip"))

if __name__ == '__main__':
    socketio.run(app, debug=True, port=socketio_server_port)

