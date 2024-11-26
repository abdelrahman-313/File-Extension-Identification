import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
import magic
from slugify import slugify

# Get a logger instance
logger = logging.getLogger('django')

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt']

def is_allowed_file(filename):
    """Ensure the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    """Sanitize file name to prevent path traversal"""
    return slugify(filename)

def is_safe_file(file):
    """Check file's MIME type for safety"""
    file_type = magic.from_buffer(file.read(1024), mime=True)
    logger.debug(f"Detected file type: {file_type}")
    return file_type in ['image/jpeg', 'image/png', 'application/pdf', 'text/plain']

class FileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Accept WebSocket connection"""
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        logger.info(f"Disconnected with code {close_code}")

    async def receive(self, text_data):
        """Handle received data and process file information"""
        logger.debug("Received data: %s", text_data)

        # Handle incoming data from the client
        try:
            data = json.loads(text_data)
            file_data = data.get("file", {})
            file_name = file_data.get("name", "Unknown File Name")

            # Sanitize filename and check for file extension
            file_name = sanitize_filename(file_name)

            logger.debug(f"Sanitized file name: {file_name}")
            
            if not is_allowed_file(file_name):
                logger.error(f"File extension not allowed: {file_name}")
                await self.send(text_data=json.dumps({'error': 'Invalid file extension not in allowed extensions: {allowed}'.format(allowed=' , '.join(ALLOWED_EXTENSIONS))}))
                return

            # Read and validate file content for security (e.g., using magic)
            file = file_data.get("file")
            if not is_safe_file(file):
                logger.error("Malicious file content detected.")
                await self.send(text_data=json.dumps({'error': 'Unsafe file content'}))
                return

            # If everything is safe, respond with the file's extension
            file_extension = file_name.split('.')[-1]
            logger.info(f"File extension: {file_extension}")

            response = {
                'file_name': file_name,
                'file_extension': file_extension
            }
            await self.send(text_data=json.dumps(response))

        except json.JSONDecodeError:
            logger.error("Failed to decode JSON data")
            await self.send(text_data=json.dumps({'error': 'Invalid JSON data'}))
