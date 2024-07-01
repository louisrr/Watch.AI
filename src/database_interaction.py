from cassandra.cluster import Cluster

def connect_to_db():
    cluster = Cluster(['127.0.0.1'])  # Use your ScyllaDB IP
    session = cluster.connect('your_keyspace')
    return session

def get_visual_representation(entity, session):
    query = "SELECT visual_link FROM visual_elements WHERE name = %s"
    result = session.execute(query, (entity,))
    return result.one().visual_link if result else None
