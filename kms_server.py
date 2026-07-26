from flask import Flask, request, jsonify, abort
from cryptography.fernet import Fernet
import uuid
from datetime import datetime, timezone

app = Flask(__name__)

# --- INSECURE CONFIGURATION (FOR EDUCATIONAL PURPOSES ONLY) ---
MASTER_KEY = Fernet.generate_key() 
cipher_suite = Fernet(MASTER_KEY)

# Dictionary mapping API keys to user roles
API_KEYS = {
    "admin-key-123": "admin",
    "client-key-456": "client"
}

# In-memory database to store our keys
key_database = {}

# --- HELPER FUNCTIONS ---
def check_auth():
    """
    Auth Implementation
    1. Check if the 'x-api-key' header exists in the request.
    2. Check if the provided key exists in the API_KEYS dictionary.
    3. If missing or invalid, use abort(401) to reject the request.
    4. If valid, return the role associated with the API key.
    """
    if 'x-api-key' not in request.headers:
        abort(401, description="API key is missing")

    api_key = request.headers['x-api-key']
    if api_key not in API_KEYS or API_KEYS[api_key]['revoked'] is True:
        abort(401, description="API key is invalid")

    return API_KEYS[api_key]

# --- API ENDPOINTS ---

@app.route('/keys', methods=['POST'])
def generate_key():
    role = check_auth()
    
    new_key_material = Fernet.generate_key().decode('utf-8')
    key_id = str(uuid.uuid4())
    
    """
    Key Encryption & Add Metadata
    1. Encrypt 'new_key_material' using the cipher_suite.
    2. Store it in key_database[key_id] as a dictionary containing:
       - 'encrypted_key': the encrypted data
       - 'created_at': current UTC timestamp (use datetime)
       - 'created_by': the role that generated the key
       - 'revoked': False
    """
    # encryption and storage logic
    encrypted_key = cipher_suite.encrypt(new_key_material.encode('utf-8')).decode('utf-8')
    key_database[key_id] = {
        'encrypted_key': encrypted_key,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'created_by': role,
        'revoked': False
    }

    return jsonify({"message": "Key generated successfully", "key_id": key_id}), 201


@app.route('/keys/<key_id>', methods=['GET'])
def get_key(key_id):
    role = check_auth()
    
    if key_id not in key_database:
        abort(404, description="Key not found")
        
    key_record = key_database[key_id]
    
    if key_record.get('revoked'):
        abort(400, description="This key has been revoked")

    """
    Key Decryption
    1. Retrieve the encrypted key from key_record.
    2. Decrypt it using the cipher_suite.
    3. Assign the decrypted value to 'decrypted_key_material'.
    """
    # decryption logic
    decrypted_key_material = cipher_suite.decrypt(key_record['encrypted_key'].encode('utf-8')).decode('utf-8')

    return jsonify({
        "key_id": key_id, 
        "key_material": decrypted_key_material,
        "metadata": {
            "created_at": key_record.get('created_at'),
            "created_by": key_record.get('created_by')
        }
    }), 200


@app.route('/keys/<key_id>', methods=['DELETE'])
def revoke_key(key_id):
    role = check_auth()
    """
    RBAC & Revoke Implementation
    1. Check if the 'role' is 'admin'. If not, abort(403, description="Forbidden").
    2. Check if the key_id exists in the key_database. If not, abort(404).
    3. Update the key_record so that 'revoked' is True. 
       (Do NOT delete the key from the dictionary).
    """
    if role != 'admin':
        abort(403, description="Forbidden")

    if key_id not in key_database:
        abort(404, description="Key ID does not exist in the key database")

    key_database[key_id]['revoked'] = True

    return jsonify({"message": f"Key {key_id} successfully revoked."}), 200

if __name__ == '__main__':
    # Running securely on localhost (TLS configuration omitted for time constraints)
    app.run(debug=True, port=5000)