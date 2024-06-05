from flask import Blueprint, request, jsonify
from flask_socketio import emit
from datetime import datetime, timedelta
from sqlalchemy import func
from Global import sessionMaker
from models.TimeSeriesPacket import TimeSeriesPacket
from flask_socketio import emit
import json


def main_connect():
    print('Client connected')


def main_disconnect():
    print('Client disconnected')
    


def handle_request_data_24_hour_sum():
    session = sessionMaker()
    
    from_time_dt = datetime.now() - timedelta(hours=24)

    print(f"Received request_data event with range: {from_time_dt}")

    size_sum = session.query(
        func.sum(func.length(TimeSeriesPacket.size)).label('total_size')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt
    ).scalar() or 0  # Set default to 0 if no data found
    
 
    session.close()
    
    data_json = {
        "value": round(size_sum / 1024)
    }

    emit('data_update_24_hour_sum', json.dumps(data_json), namespace='/main')


def handle_request_data_24_hours_total_packet_count():
    session = sessionMaker()
    
    from_time_dt = datetime.now() - timedelta(hours=24)
  
    print(f"Received request_data event with range: {from_time_dt}")

    total_packet_count = session.query(
        func.count()
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt
    ).scalar() or 0  # Set default to 0 if no data found
    
    session.close()
    
    data_json = {
        "value": total_packet_count
    }

    emit('data_update_last_24_hours_total_packet_count', json.dumps(data_json), namespace='/main')
    
def handle_request_data_30():

    session = sessionMaker()

   # Calculate the timestamp 30 minutes ago
    from_time_dt = datetime.now() - timedelta(minutes=30)

    # Log received time range for debugging
    print(f"Received request_data event with range: {from_time_dt}")

    # Query the database to count packets for each minute within the last 30 minutes
    quantity_per_minute = session.query(
        func.date_trunc('minute', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()
    
    
    # Close the session
    session.close()

    # Convert the result to a JSON-like format
    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    # Emit the data update event
    emit('data_update_30', json.dumps(data_json), namespace='/main')
   
def handle_request_data_60():

    session = sessionMaker()

   # Calculate the timestamp 30 minutes ago
    from_time_dt = datetime.now() - timedelta(minutes=60)

    # Log received time range for debugging
    print(f"Received request_data event with range: {from_time_dt}")

    # Query the database to count packets for each minute within the last 30 minutes
    quantity_per_minute = session.query(
        func.date_trunc('minute', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()

    # Close the session
    session.close()

    # Convert the result to a JSON-like format
    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    # Emit the data update event
    emit('data_update_60', json.dumps(data_json), namespace='/main')
  
def handle_request_data_12h():

    session = sessionMaker()

   # Calculate the timestamp 30 minutes ago
    from_time_dt = datetime.now() - timedelta(hours=12)

    # Query the database to count packets for each minute within the last 30 minutes
    quantity_per_minute = session.query(
        func.date_trunc('hour', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()

    # Close the session
    session.close()

    # Convert the result to a JSON-like format
    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    # Emit the data update event
    emit('data_update_12h', json.dumps(data_json), namespace='/main')
  
def handle_request_data_24h():

    session = sessionMaker()

   # Calculate the timestamp 60 minutes ago
    from_time_dt = datetime.now() - timedelta(hours=24)

 
    # Query the database to count packets for each minute within the last 30 minutes
    quantity_per_minute = session.query(
        func.date_trunc('hour', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()

    # Close the session
    session.close()

    # Convert the result to a JSON-like format
    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    # Emit the data update event
    emit('data_update_24h', json.dumps(data_json), namespace='/main')

def handle_request_data_protocols():

    session = sessionMaker()

    protocol_counts = session.query(
    TimeSeriesPacket.protocol,
        func.count(TimeSeriesPacket.id).label('packet_count')
    ).group_by(TimeSeriesPacket.protocol).all()

    # Close the session
    session.close()

    protocol_counts = [ {"protocol":p[0], "count":p[1]} for p in protocol_counts ]
    

    emit('data_update_protocols', json.dumps(protocol_counts), namespace='/main')
  
def handle_request_data_source_ports():

    session = sessionMaker()

    top_src_ports = session.query(
    TimeSeriesPacket.src_port,
    func.count(TimeSeriesPacket.id).label('packet_count')
    ).group_by(
        TimeSeriesPacket.src_port
    ).order_by(
        func.count(TimeSeriesPacket.id).desc()
    ).limit(10).all()

    # Close the session
    session.close()

    top_src_ports = [{"port": i[0], "count":i[1]} for i in top_src_ports]

    emit('data_update_sourceports', json.dumps(top_src_ports), namespace='/main')
  
def handle_request_data_dest_ports():

    session = sessionMaker()

    top_dst_ports = session.query(
    TimeSeriesPacket.dst_port,
    func.count(TimeSeriesPacket.id).label('packet_count')
    ).group_by(
        TimeSeriesPacket.dst_port
    ).order_by(
        func.count(TimeSeriesPacket.id).desc()
    ).limit(10).all()

    # Close the session
    session.close()

    top_dst_ports = [{"port": i[0], "count":i[1]} for i in top_dst_ports]

    emit('data_update_destports', json.dumps(top_dst_ports), namespace='/main')
  
def handle_packet_count_by_ip():
   
    session = sessionMaker()

    # Execute the query
    result = session.query(
        TimeSeriesPacket.ip_address,
        func.count().label('packet_count')
    ).group_by(
        TimeSeriesPacket.ip_address
    ).order_by(
        func.count().desc()
    ).all()

    # Close the session
    session.close()
    
    data = [{"ip_address": row.ip_address, "count": row.packet_count} for row in result]
 
    emit('host_by_number_packets', json.dumps(data), namespace='/main')
  
def handle_packet_size_by_ip():
    session = sessionMaker()

    # Execute the query
    result = session.query(
        TimeSeriesPacket.ip_address,
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).group_by(
        TimeSeriesPacket.ip_address
    ).order_by(
        func.count().desc()
    ).all()

    # Close the session
    session.close()
    
    data = [{"ip_address": row.ip_address, "count": round(row.packet_count/1024)} for row in result]
 
    emit('host_by_size_packets', json.dumps(data), namespace='/main')

def handle_packet_host_by_source_packets():
    session = sessionMaker()


    result = session.query(
        TimeSeriesPacket.ip_address,
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).group_by(
        TimeSeriesPacket.ip_address
    ).order_by(
        func.count().desc()
    ).all()

    # Close the session
    session.close()
    
    data = [{"ip_address": row.ip_address, "count": round(row.packet_count/1024)} for row in result]
 
    emit('host_by_size_packets', json.dumps(data), namespace='/test')
   