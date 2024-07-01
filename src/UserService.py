from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import re

app = FastAPI()

# Set up Argon2 context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Sanitize input
def sanitize(input_string):
    # Basic email sanitization. For production, consider more comprehensive validation
    return re.sub(r'[^a-zA-Z0-9.@_-]', '', input_string)

# Connect to ScyllaDB (adjust credentials and connection details)
auth_provider = PlainTextAuthProvider(username='your_username', password='your_password')
cluster = Cluster(['scylla_db_address'], auth_provider=auth_provider)
session = cluster.connect()

# Ensure the keyspace and table exist
session.execute("CREATE KEYSPACE IF NOT EXISTS user_management WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};")
session.execute("CREATE TABLE IF NOT EXISTS user_management.watchers (user_email text PRIMARY KEY, pw_hash text);")

@app.post("/create_user/")
async def create_user(email: str, password: str):
    sanitized_email = sanitize(email)
    sanitized_password = sanitize(password)
    hashed_password = pwd_context.hash(sanitized_password)
    
    # Check if email already exists
    check_user = session.execute("SELECT * FROM user_management.watchers WHERE user_email = %s", [sanitized_email])
    
    if check_user.one():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Insert new user
    session.execute("INSERT INTO user_management.watchers (user_email, pw_hash) VALUES (%s, %s)", (sanitized_email, hashed_password))
    
    return {"message": "User created successfully"}


@app.post("/request_password_reset/")
async def request_password_reset(email: str):
    emailSanitized = sanitize(email)
    
    # Check if the email exists in the user_management table
    if not session.execute("SELECT * FROM user_management WHERE user_email = %s", [emailSanitized]).one():
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Generate a unique Argon2 hash for the password reset link
    unique_key = argon2.hash(uuid4().hex)
    expiry_time = datetime.utcnow() + timedelta(hours=25)
    change_key = unique_key[-6:]
    
    # Assume request_ip is fetched correctly from the request context
    request_ip = "user_ip_address"  # Placeholder, replace with actual IP address extraction logic
    
    # Insert the password reset hash into the password_reset_hashes table
    session.execute(
        """
        INSERT INTO password_reset_hashes (email, hash, expiry, change_key, request_ip, original_email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (emailSanitized, unique_key, expiry_time, change_key, request_ip, emailSanitized)
    )
    
    return {"message": "Password reset requested"}

@app.post("/change_password/{unique_hash}/")
async def change_password(unique_hash: str, request: Request, change: str, new_password: str):
    # Retrieve record from password_reset_hashes
    record = session.execute(
        "SELECT * FROM password_reset_hashes WHERE hash = %s", [unique_hash]
    ).one()
    
    if not record:
        raise HTTPException(status_code=404, detail="Invalid reset link")
    
    # Check if the current time is past the expiry time
    if datetime.utcnow() > record['expiry']:
        return "This key is expired. Please use the password reset function again."
    
    # Check IP address and change_key
    client_ip = "client_ip_address"  # Placeholder, replace with actual IP extraction logic from request
    if client_ip != record['request_ip'] or change != record['change_key']:
        raise HTTPException(status_code=403, detail="Unauthorized attempt to change password")
    
    # Update password in user_management table
    hashed_password = pwd_context.hash(new_password)
    session.execute(
        "UPDATE user_management SET pw_hash = %s WHERE user_email = %s",
        (hashed_password, record['original_email'])
    )
    
    return {"message": "Password successfully updated"}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
