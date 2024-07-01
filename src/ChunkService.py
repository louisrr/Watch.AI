import os
import socket

def read_in_chunks(file_path, chunk_size=50*1024*1024):  # Default chunk size is 50 MB
    """Generator to read a file in chunks."""
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

def divide(file_path):
    """Divide the file into chunks and send to the DHT server."""
    file_size = os.path.getsize(file_path)
    print(f"Total file size: {file_size} bytes")

    # Calculate total chunks
    total_chunks = file_size // (50 * 1024 * 1024)
    if file_size % (50 * 1024 * 1024) != 0:
        total_chunks += 1

    print(f"Total chunks to send: {total_chunks}")

    # TCP connection details
    host = 'localhost'  # Assuming the server is running locally
    port = 5732  # The port on which the C++ server is listening
    
    # Establish a TCP connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        # Send each chunk to the server
        for i, chunk in enumerate(read_in_chunks(file_path)):
            # Simulate the insertion command as if we're using the server's DSL
            command = f"INSERT INTO group_id VALUES ({i}, {chunk})\n"
            sock.sendall(command.encode('utf-8'))  # Send the command encoded as bytes
            
            # Await server response for confirmation
            response = sock.recv(1024)  # Read server response
            print(f"Server response for chunk {i}: {response.decode('utf-8')}")

def assemble_chunks(group_id):
    """Retrieve chunks by group ID and assemble them into a single data object."""
    # TCP connection details
    host = 'localhost'  # Assuming the server is running locally
    port = 5732  # The port on which the C++ server is listening

    # Establish a TCP connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        # Send a command to retrieve all chunks for a specific group_id
        command = f"SELECT * FROM {group_id}\n"
        sock.sendall(command.encode('utf-8'))

        # Receive and assemble chunks
        assembled_data = b''
        while True:
            chunk = sock.recv(1024)  # Assuming chunks are sent sequentially and fit in this buffer size
            if not chunk:
                break
            assembled_data += chunk

    return assembled_data


# Example usage
if __name__ == "__main__":
    # First, divide a large video file into chunks and send them
    video_file_path = "/path/to/large/video/file.mp4"
    divide(video_file_path)

    # After dividing, simulate retrieving and assembling chunks from the group
    group_id = "some_group_id"
    data = assemble_chunks(group_id)
    print("Assembled data length:", len(data))

    # Optionally, write the data to a file or process further
    with open("output_file", "wb") as file:
        file.write(data)