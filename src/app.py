"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(members), 200 # changed to members instead of response_body for the test

@app.route('/members/<int:member_id>', methods=['GET']) # declaration of int:member_id inside the URL declares the integer as member_id, it can then be used later in the same function
def get_member_path(member_id):
    # This is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    print("bongos", member, member_id)
    if not member:
        return jsonify({
            "message" : "hey we ain't found shit"
        }), 404
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def add_member_path():
    info = request.get_json() # get access to body
    result = jackson_family.add_member(info)
    return jsonify(result), 200

@app.route('/members', methods=['PUT']) # Edit this later
def edit_member_path():
    info = request.get_json()
    result = jackson_family.add_member(info)
    return jsonify(result), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member_path(member_id): # 
    result = jackson_family.delete_member(int(member_id)) # 
    if result == None: #if statement to determine success or error code
        return f"Error, no member with the ID {member_id} found", 404
    else:
        return jsonify({"done": True}) # had to look at the documentation (readme) for what was expected to be returned



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
