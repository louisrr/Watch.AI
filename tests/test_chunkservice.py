import os
import socket
import pytest
from unittest.mock import patch, mock_open, MagicMock

# Import the functions from your script
from my_script import read_in_chunks, divide, assemble_chunks

# Sample data to be used in tests
sample_file_path = 'test_file.mp4'
sample_file_content = b'A' * (50 * 1024 * 1024 + 1)  # 50 MB + 1 byte
sample_chunk_size = 50 * 1024 * 1024

@pytest.fixture
def mock_file():
    m_open = mock_open(read_data=sample_file_content)
    with patch('builtins.open', m_open):
        yield m_open

@pytest.fixture
def mock_socket():
    with patch('socket.socket') as mock_sock:
        mock_socket_instance = MagicMock()
        mock_sock.return_value = mock_socket_instance
        yield mock_socket_instance

def test_read_in_chunks(mock_file):
    chunks = list(read_in_chunks(sample_file_path))
    assert len(chunks) == 2
    assert chunks[0] == sample_file_content[:sample_chunk_size]
    assert chunks[1] == sample_file_content[sample_chunk_size:]

def test_divide(mock_file, mock_socket, monkeypatch):
    mock_file_size = len(sample_file_content)
    monkeypatch.setattr(os.path, 'getsize', lambda x: mock_file_size)

    mock_socket.recv.return_value = b'OK'

    divide(sample_file_path)

    assert mock_socket.connect.called
    assert mock_socket.sendall.called
    assert mock_socket.recv.called

    # Ensure the correct number of chunks were sent
    sendall_calls = mock_socket.sendall.call_args_list
    assert len(sendall_calls) == 2

    # Check the content of the first sendall call (first chunk)
    first_call_args = sendall_calls[0][0][0]
    expected_command = f"INSERT INTO group_id VALUES (0, {sample_file_content[:sample_chunk_size]})\n".encode('utf-8')
    assert first_call_args.startswith(b"INSERT INTO group_id VALUES (0, ")
    assert first_call_args.endswith(b")\n")

def test_assemble_chunks(mock_socket):
    group_id = 'test_group_id'
    mock_socket.recv.side_effect = [b'chunk1', b'chunk2', b'']

    assembled_data = assemble_chunks(group_id)

    assert mock_socket.connect.called
    assert mock_socket.sendall.called
    assert assembled_data == b'chunk1chunk2'
