from flask import Flask, request, jsonify, abort
from cryptography.fernet import Fernet
import uuid
import datetime

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
    TODO: Implement Auth
    1. Check if the 'x-api-key' header exists in the request.
    2. Check if the provided key exists in the API_KEYS dictionary.
    3. If missing or invalid, use abort(401) to reject the request.
    4. If valid, return the role associated with the API key.
    """
    pass # Remove this pass and write your logic here

# --- API ENDPOINTS ---

@app.route('/keys', methods=['POST'])
def generate_key():
    role = check_auth()
    
    new_key_material = Fernet.generate_key().decode('utf-8')
    key_id = str(uuid.uuid4())
    
    """
    TODO: Encrypt Key & Add Metadata
    1. Encrypt 'new_key_material' using the cipher_suite.
    2. Store it in key_database[key_id] as a dictionary containing:
       - 'encrypted_key': the encrypted data
       - 'created_at': current UTC timestamp (use datetime)
       - 'created_by': the role that generated the key
       - 'revoked': False
    """
    
    # Placeholder: replace with actual encryption and storage logic
    key_database[key_id] = {'encrypted_key': new_key_material, 'revoked': False} 

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
    TODO: Decrypt Key
    1. Retrieve the encrypted key from key_record.
    2. Decrypt it using the cipher_suite.
    3. Assign the decrypted value to 'decrypted_key_material'.
    """
    
    # Placeholder: replace with actual decryption logic
    decrypted_key_material = key_record['encrypted_key']

    return jsonify({
        "key_id": key_id, 
        "key_material": decrypted_key_material,
        "metadata": {
            # Note: Ensure you added 'created_at' and 'created_by' in the POST route
            "created_at": key_record.get('created_at'),
            "created_by": key_record.get('created_by')
        }
    }), 200


@app.route('/keys/<key_id>', methods=['DELETE'])
def revoke_key(key_id):
    role = check_auth()
    
    """
    TODO: Implement RBAC & Revoke
    1. Check if the 'role' is 'admin'. If not, abort(403, description="Forbidden").
    2. Check if the key_id exists in the key_database. If not, abort(404).
    3. Update the key_record so that 'revoked' is True. 
       (Do NOT delete the key from the dictionary).
    """
    
    return jsonify({"message": f"Key {key_id} successfully revoked."}), 200

if __name__ == '__main__':
    # Running securely on localhost (TLS configuration omitted for time constraints)
    app.run(debug=True, port=5000)