# Key Management Service (KMS) API

Implements the missing security and access control logic for a partially built KMS API.

## Run the KMS Server

Create a python virtual environment and activate the venv.

```bash
python3 -m venv venv
source venv/bin/activate
```

Run the service

```bash
python3 kms_server.py
```

## Make API Calls to the KMS Server

```bash
# Successful POST /keys request showing the generated key_id.
curl -X POST http://127.0.0.1:5000/keys -H "x-api-key: admin-key-123"

# Successful GET /keys/<key_id> request showing the decrypted key and metadata.
curl -X GET http://127.0.0.1:5000/keys/0c3167be-946a-41e6-b5d6-48bffc8dcd56 -H "x-api-key: admin-key-123"

# Failed DELETE /keys/<key_id> request showing a 403 Forbidden when using the "client" API key.
curl -X DELETE http://127.0.0.1:5000/keys/0c3167be-946a-41e6-b5d6-48bffc8dcd56 -H "x-api-key: client-key-456"

# Successful DELETE /keys/<key_id> request showing the key being revoked when using the "admin" API key.
curl -X DELETE http://127.0.0.1:5000/keys/0c3167be-946a-41e6-b5d6-48bffc8dcd56 -H "x-api-key: admin-key-123" 
```
