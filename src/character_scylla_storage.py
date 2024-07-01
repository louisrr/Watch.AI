from cassandra.cluster import Cluster
import uuid
from datetime import datetime

# Connect to your ScyllaDB cluster
cluster = Cluster(['your_scylla_db_ip'])
session = cluster.connect()

# Specify the keyspace and table
keyspace = 'your_keyspace_name'
table = 'character_profiles'

# Example metadata
user_id = 'user123'
character_name = 'AvatarName'
timestamp = datetime.now()
character_id = uuid.uuid4()  # Generate a unique UUID for the character

# Prepare the insert query with the new UUID field
insert_query = f"""
INSERT INTO {keyspace}.{table} (character_id, user_id, name, image_url, created_at)
VALUES (%s, %s, %s, %s, %s);
"""

# Execute the query with the UUID
session.execute(insert_query, (character_id, user_id, character_name, image_url, timestamp))
