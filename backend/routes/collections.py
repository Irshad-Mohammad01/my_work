from flask import Blueprint, jsonify, request
from backend.models.collection import CollectionModel
from backend.extensions import db

collections_bp = Blueprint('collections', __name__)

@collections_bp.route('', methods=['GET'])
@collections_bp.route('/', methods=['GET'])
def get_collections():
    try:
        collections = CollectionModel.query.filter_by(is_active=True).order_by(CollectionModel.display_order.asc(), CollectionModel.id.asc()).all()
        return jsonify([c.to_dict() for c in collections]), 200
    except Exception as e:
        print("Error fetching collections:", e)
        return jsonify([]), 200

@collections_bp.route('/<int:collection_id>', methods=['GET'])
def get_collection(collection_id):
    try:
        collection = CollectionModel.query.get(collection_id)
        if not collection:
            return jsonify({"message": "Collection not found"}), 404
        return jsonify(collection.to_dict()), 200
    except Exception as e:
        print("Error fetching collection:", e)
        return jsonify({"message": "Server error"}), 500
