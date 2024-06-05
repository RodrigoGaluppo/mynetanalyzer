from flask import Blueprint, request, jsonify
from models.Host import HostModel
from datetime import datetime
from Global import sessionMaker


host_blueprint = Blueprint('host_blueprint', __name__)

@host_blueprint.route('', methods=['POST'])
def create_host():
    data = request.json
    new_host = HostModel(
        ip=data['ip'],
        name=data['name'],
        created_at=datetime.now()
    )
    session = sessionMaker()
    try:
        session.add(new_host)
        session.commit()
        return jsonify(new_host.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@host_blueprint.route('', methods=['GET'])
def get_hosts():
    session = sessionMaker()
    try:
        hosts = session.query(HostModel).all()
        return jsonify([host.to_dict() for host in hosts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@host_blueprint.route('/<int:host_id>', methods=['GET'])
def get_host(host_id):
    session = sessionMaker()
    try:
        host = session.query(HostModel).get(host_id)
        if host:
            return jsonify(host.to_dict()), 200
        else:
            return jsonify({"error": "Host not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@host_blueprint.route('/<int:host_id>', methods=['PUT'])
def update_host(host_id):
    data = request.json
    session = sessionMaker()
    try:
        host = session.query(HostModel).get(host_id)
        if host:
            host.ip = data.get('ip', host.ip)
            host.name = data.get('name', host.name)
            session.commit()
            return jsonify(host.to_dict()), 200
        else:
            return jsonify({"error": "Host not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@host_blueprint.route('/<int:host_id>', methods=['DELETE'])
def delete_host(host_id):
    session = sessionMaker()
    try:
        host = session.query(HostModel).get(host_id)
        if host:
            session.delete(host)
            session.commit()
            return jsonify({"message": "Host deleted"}), 200
        else:
            return jsonify({"error": "Host not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
