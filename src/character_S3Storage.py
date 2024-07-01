import boto3
from datetime import datetime

# Create an S3 client
s3_client = boto3.client('s3')

# Specify your bucket name
bucket_name = 'your-bucket-name'

# Generate a unique file name
file_name = f"{datetime.now().isoformat()}_character.png"

# Upload the file
s3_client.upload_file("temp_image.png", bucket_name, file_name)

# Generate the URL of the uploaded file
image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
