from flask import Blueprint, request, jsonify
from flask_socketio import emit
from datetime import datetime, timedelta
from sqlalchemy import func
from Global import sessionMaker
from models.TimeSeriesPacket import TimeSeriesPacket
import json

def main_connect():
    print('Client connected')

def main_disconnect():
    print('Client disconnected')

def handle_request_data_24_hour_sum_host(ip_address):
    session = sessionMaker()
    from_time_dt = datetime.now() - timedelta(hours=24)
    #print(f"Received request_data event with range: {from_time_dt}")
    
    size_sum = session.query(
        func.sum(func.length(TimeSeriesPacket.size)).label('total_size')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt,
        TimeSeriesPacket.ip_address == ip_address
    ).scalar() or 0  # Set default to 0 if no data found

    session.close()
    
    data_json = {
        "value": round(size_sum / 1024)
    }

    emit('data_update_24_hour_sum_host', json.dumps(data_json), namespace='/main')

def handle_request_data_24_hours_total_packet_count_host(ip_address):
    session = sessionMaker()
    from_time_dt = datetime.now() - timedelta(hours=24)
    #print(f"Received request_data event with range: {from_time_dt}")

    total_packet_count = session.query(
        func.count()
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt,
        TimeSeriesPacket.ip_address == ip_address
    ).scalar() or 0  # Set default to 0 if no data found

    session.close()
    
    data_json = {
        "value": total_packet_count
    }

    emit('data_update_last_24_hours_total_packet_count_host', json.dumps(data_json), namespace='/main')

def handle_request_data_30_host(ip_address):
    session = sessionMaker()
    from_time_dt = datetime.now() - timedelta(minutes=30)
    #print(f"Received request_data event with range: {from_time_dt}")

    quantity_per_minute = session.query(
        func.date_trunc('minute', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt,
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()

    session.close()

    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    emit('data_update_30_host', json.dumps(data_json), namespace='/main')

def handle_request_data_60_host(ip_address):
    session = sessionMaker()
    from_time_dt = datetime.now() - timedelta(minutes=60)
    #print(f"Received request_data event with range: {from_time_dt}")

    quantity_per_minute = session.query(
        func.date_trunc('minute', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt,
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()

    session.close()

    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    emit('data_update_60_host', json.dumps(data_json), namespace='/main')

def handle_request_data_12h_host(ip_address):
    session = sessionMaker()
    from_time_dt = datetime.now() - timedelta(hours=12)

    quantity_per_minute = session.query(
        func.date_trunc('hour', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt,
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()

    session.close()

    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    emit('data_update_12h_host', json.dumps(data_json), namespace='/main')

def handle_request_data_24h_host(ip_address):
    
    session = sessionMaker()
    from_time_dt = datetime.now() - timedelta(hours=24)

    quantity_per_minute = session.query(
        func.date_trunc('hour', TimeSeriesPacket.timestamp).label('time_interval'),
        func.sum(func.length(TimeSeriesPacket.size)).label('packet_count')
    ).filter(
        TimeSeriesPacket.timestamp >= from_time_dt,
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        'time_interval'
    ).order_by(
        'time_interval'
    ).all()

    session.close()

    data_json = [
        {"quantity": round(row.packet_count / 1024), "timestamp": row.time_interval.strftime("%Y-%m-%d %H:%M:%S")}
        for row in quantity_per_minute
    ]

    emit('data_update_24h_host', json.dumps(data_json), namespace='/main')

def handle_request_data_protocols_host(ip_address):
    session = sessionMaker()

    protocol_counts = session.query(
        TimeSeriesPacket.protocol,
        func.count(TimeSeriesPacket.id).label('packet_count')
    ).filter(
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(TimeSeriesPacket.protocol).all()

    session.close()

    protocol_counts = [ {"protocol": p[0], "count": p[1]} for p in protocol_counts ]
    emit('data_update_protocols_host', json.dumps(protocol_counts), namespace='/main')

def handle_request_data_source_ports_host(ip_address):
    session = sessionMaker()

    top_src_ports = session.query(
        TimeSeriesPacket.src_port,
        func.count(TimeSeriesPacket.id).label('packet_count')
    ).filter(
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        TimeSeriesPacket.src_port
    ).order_by(
        func.count(TimeSeriesPacket.id).desc()
    ).limit(10).all()

    session.close()

    top_src_ports = [{"port": i[0], "count": i[1]} for i in top_src_ports]
    emit('data_update_sourceports_host', json.dumps(top_src_ports), namespace='/main')

def handle_request_data_dest_ports_host(ip_address):
    session = sessionMaker()

    top_dst_ports = session.query(
        TimeSeriesPacket.dst_port,
        func.count(TimeSeriesPacket.id).label('packet_count')
    ).filter(
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        TimeSeriesPacket.dst_port
    ).order_by(
        func.count(TimeSeriesPacket.id).desc()
    ).limit(10).all()

    session.close()

    top_dst_ports = [{"port": i[0], "count": i[1]} for i in top_dst_ports]
    emit('data_update_destports_host', json.dumps(top_dst_ports), namespace='/main')
    
def handle_top_destinations_by_packet_count(ip_address):
    session = sessionMaker()

    result = session.query(
        TimeSeriesPacket.dst,
        func.count(TimeSeriesPacket.id).label('packet_count')
    ).filter(
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        TimeSeriesPacket.dst
    ).order_by(
        func.count(TimeSeriesPacket.id).desc()
    ).limit(10).all()

    session.close()
    
    data = [{"dst_ip_address": row.dst, "count": row.packet_count} for row in result]
    emit('data_update_top_destinations_by_packet_count', json.dumps(data), namespace='/main')


def handle_top_sources_by_packet_count(ip_address):
    session = sessionMaker()

    result = session.query(
        TimeSeriesPacket.src,
        func.count(TimeSeriesPacket.id).label('packet_count')
    ).filter(
        TimeSeriesPacket.ip_address == ip_address
    ).group_by(
        TimeSeriesPacket.src
    ).order_by(
        func.count(TimeSeriesPacket.id).desc()
    ).limit(10).all()

    session.close()
    
    data = [{"src_ip_address": row.src, "count": row.packet_count} for row in result]
    emit('data_update_top_sources_by_packet_count', json.dumps(data), namespace='/main')


