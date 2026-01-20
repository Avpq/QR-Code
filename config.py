"""
Configuration constants for QR Code Application.
Centralizes all magic numbers and configuration values.
"""
from pathlib import Path
import tempfile

# Application metadata
APP_NAME = "QR Code Generator"
APP_VERSION = "2.0.0"

# UI Configuration
UI_FILE = "QRCodeGUI.ui"
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# Image display settings
IMAGE_DISPLAY_WIDTH = 350
IMAGE_DISPLAY_HEIGHT = 350

# QR Code generation settings
QR_VERSION = 4  # Determines QR code size (1-40)
QR_ERROR_CORRECTION = "H"  # L, M, Q, H (L=7%, M=15%, Q=25%, H=30% error correction)
QR_BOX_SIZE = 20  # Size of each QR code box in pixels
QR_BORDER = 2  # Border size in boxes
QR_FILL_COLOR = "black"
QR_BACK_COLOR = "white"

# File dialog settings
SUPPORTED_IMAGE_FORMATS = "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
DEFAULT_SAVE_FORMAT = "PNG"
DEFAULT_SAVE_EXTENSION = ".png"

# Temporary file handling
TEMP_DIR = Path(tempfile.gettempdir()) / "qrcode_app"
TEMP_QR_FILENAME = "temp_qr.png"

# Error messages
ERROR_NO_FILE_SELECTED = "No file selected"
ERROR_INVALID_IMAGE = "Invalid image file or corrupted data"
ERROR_QR_DECODE_FAILED = "Failed to decode QR code from image"
ERROR_QR_GENERATION_FAILED = "Failed to generate QR code"
ERROR_EMPTY_TEXT = "Cannot generate QR code from empty text"
ERROR_FILE_SAVE_FAILED = "Failed to save file"
ERROR_UI_FILE_MISSING = f"UI file '{UI_FILE}' not found"

# Success messages
SUCCESS_QR_GENERATED = "QR code generated successfully"
SUCCESS_QR_DECODED = "QR code decoded successfully"
SUCCESS_FILE_SAVED = "File saved successfully"

# Ensure temp directory exists
TEMP_DIR.mkdir(parents=True, exist_ok=True)
