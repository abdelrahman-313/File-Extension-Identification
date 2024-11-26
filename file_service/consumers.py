import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

# Get a logger instance for Django logs
logger = logging.getLogger("django")

class FileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Log the WebSocket connection event (only if necessary)
        logger.info("New WebSocket connection established")

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Log WebSocket disconnection event (if important)
        logger.info(f"WebSocket disconnected with close code: {close_code}")

    async def receive(self, text_data):
        # Log a shortened version of the data or important metadata only
        if len(text_data) > 200:  # Only log if the data is small enough
            logger.debug("Received large message, logging truncated version")
            logger.debug("Received data (first 200 chars): %s", text_data[:200])
        else:
            logger.debug("Received small message: %s", text_data)

        try:
            # Handle the incoming data (parse the JSON)
            data = json.loads(text_data)
            
            # Log specific key data or important fields
            if "file" in data:
                file_data = data["file"]
                logger.debug("Received file data: %s", json.dumps(file_data, ensure_ascii=False, indent=2))

            # Log the presence of file name, but do not log the entire file content if large
            file_name = data.get("file", {}).get("name", "Unknown File Name")
            logger.debug("File name: %s", file_name)

            # File extension (log only this important info)
            file_extension = file_name.split('.')[-1] if '.' in file_name else "Unknown Extension"
            logger.debug("File extension: %s", file_extension)

            # Send the response back to the client
            response = {
                'file_name': file_name,
                'file_extension': file_extension
            }
            await self.send(text_data=json.dumps(response))

            # Log that the response was sent
            logger.info("Response sent to client: %s", json.dumps(response, ensure_ascii=False, indent=2))

        except json.JSONDecodeError as e:
            # Log only error-level logs if the JSON is malformed
            logger.error("Failed to decode JSON data: %s", str(e))
        except Exception as e:
            # Log only unexpected exceptions at error level with the traceback
            logger.exception("An unexpected error occurred while processing the message: %s", str(e))
