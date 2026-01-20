"""
Core QR code business logic - completely decoupled from UI.
This module can be tested independently and reused in different contexts.
"""
from typing import Optional, Tuple
from pathlib import Path
import logging
import qrcode
from qrcode.image.pil import PilImage
import cv2
import numpy as np
from PIL import Image

from config import (
    QR_VERSION, QR_ERROR_CORRECTION, QR_BOX_SIZE, QR_BORDER,
    QR_FILL_COLOR, QR_BACK_COLOR, TEMP_DIR, TEMP_QR_FILENAME,
    ERROR_EMPTY_TEXT, ERROR_INVALID_IMAGE, ERROR_QR_DECODE_FAILED,
    ERROR_QR_GENERATION_FAILED
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QRCodeError(Exception):
    """Base exception for QR code operations."""
    pass


class QRCodeGenerationError(QRCodeError):
    """Raised when QR code generation fails."""
    pass


class QRCodeDecodingError(QRCodeError):
    """Raised when QR code decoding fails."""
    pass


class QRCodeProcessor:
    """Handles QR code generation and decoding operations."""

    def __init__(self):
        """Initialize QR code processor with configuration."""
        self.error_correction_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }
        self.temp_file_path = TEMP_DIR / TEMP_QR_FILENAME

    def generate_qr_code(
        self,
        text: str,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate a QR code from text.

        Args:
            text: Text content to encode in QR code
            output_path: Optional custom output path. If None, uses temp directory

        Returns:
            Path to the generated QR code image

        Raises:
            QRCodeGenerationError: If generation fails
        """
        if not text or not text.strip():
            logger.error("Attempted to generate QR code with empty text")
            raise QRCodeGenerationError(ERROR_EMPTY_TEXT)

        try:
            logger.info(f"Generating QR code for text of length {len(text)}")

            qr = qrcode.QRCode(
                version=QR_VERSION,
                error_correction=self.error_correction_map[QR_ERROR_CORRECTION],
                box_size=QR_BOX_SIZE,
                border=QR_BORDER,
            )

            qr.add_data(text)
            qr.make(fit=True)

            image: PilImage = qr.make_image(
                fill_color=QR_FILL_COLOR,
                back_color=QR_BACK_COLOR
            )

            save_path = output_path or self.temp_file_path
            image.save(str(save_path))

            logger.info(f"QR code generated successfully at {save_path}")
            return save_path

        except Exception as e:
            logger.error(f"QR code generation failed: {str(e)}")
            raise QRCodeGenerationError(f"{ERROR_QR_GENERATION_FAILED}: {str(e)}")

    def decode_qr_code(self, image_path: Path) -> str:
        """
        Decode a QR code from an image file.

        Args:
            image_path: Path to the image file containing QR code

        Returns:
            Decoded text from the QR code

        Raises:
            QRCodeDecodingError: If decoding fails
        """
        if not image_path.exists():
            logger.error(f"Image file not found: {image_path}")
            raise QRCodeDecodingError(f"File not found: {image_path}")

        try:
            logger.info(f"Decoding QR code from {image_path}")

            # Read image with OpenCV
            image = cv2.imread(str(image_path))

            if image is None:
                raise QRCodeDecodingError(ERROR_INVALID_IMAGE)

            # Create detector and decode
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(image)

            if not data:
                logger.warning("No QR code detected in image")
                raise QRCodeDecodingError(ERROR_QR_DECODE_FAILED)

            logger.info(f"Successfully decoded QR code: {len(data)} characters")
            return data

        except cv2.error as e:
            logger.error(f"OpenCV error during QR decoding: {str(e)}")
            raise QRCodeDecodingError(f"{ERROR_INVALID_IMAGE}: {str(e)}")
        except QRCodeDecodingError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during QR decoding: {str(e)}")
            raise QRCodeDecodingError(f"{ERROR_QR_DECODE_FAILED}: {str(e)}")

    def validate_image_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Validate if a file is a valid image.

        Args:
            file_path: Path to the file to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_path.exists():
            return False, "File does not exist"

        if not file_path.is_file():
            return False, "Path is not a file"

        try:
            with Image.open(file_path) as img:
                img.verify()
            return True, ""
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"

    def cleanup_temp_files(self):
        """Remove temporary QR code files."""
        try:
            if self.temp_file_path.exists():
                self.temp_file_path.unlink()
                logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to clean up temp files: {str(e)}")
