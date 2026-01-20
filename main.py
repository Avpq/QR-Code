"""
QR Code Generator Application - Refactored for Production
Clean separation of UI and business logic with proper error handling.
"""
import sys
from pathlib import Path
from typing import Optional
import logging

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox
)
from PyQt5 import uic, QtGui

from qr_core import QRCodeProcessor, QRCodeError
from config import (
    UI_FILE, WINDOW_TITLE, IMAGE_DISPLAY_WIDTH, IMAGE_DISPLAY_HEIGHT,
    SUPPORTED_IMAGE_FORMATS, DEFAULT_SAVE_FORMAT, DEFAULT_SAVE_EXTENSION,
    ERROR_NO_FILE_SELECTED, ERROR_UI_FILE_MISSING,
    SUCCESS_QR_GENERATED, SUCCESS_QR_DECODED, SUCCESS_FILE_SAVED
)

logger = logging.getLogger(__name__)


class QRCodeGUI(QMainWindow):
    """Main application window with clean, focused UI logic."""

    def __init__(self):
        """Initialize the GUI and set up connections."""
        super().__init__()

        # Load UI file
        ui_path = Path(UI_FILE)
        if not ui_path.exists():
            self._show_critical_error(ERROR_UI_FILE_MISSING)
            sys.exit(1)

        uic.loadUi(str(ui_path), self)
        self.setWindowTitle(WINDOW_TITLE)

        # Initialize business logic
        self.qr_processor = QRCodeProcessor()
        self.current_image_path: Optional[Path] = None

        # Connect UI signals to handlers
        self._connect_signals()

        self.show()
        logger.info("Application started successfully")

    def _connect_signals(self):
        """Connect UI elements to their respective handlers."""
        self.actionLoad_2.triggered.connect(self.load_image)
        self.actionSave.triggered.connect(self.save_image)
        self.actionQUIT.triggered.connect(self.quit_program)
        self.pushButton_qr2text.clicked.connect(self.decode_qr_code)
        self.pushButton_text2qr.clicked.connect(self.generate_qr_code)

    def load_image(self):
        """Handle loading an image file for QR code decoding."""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Load Image File",
                "",
                SUPPORTED_IMAGE_FORMATS
            )

            if not filename:
                logger.debug("File selection cancelled by user")
                return

            image_path = Path(filename)

            # Validate image before loading
            is_valid, error_msg = self.qr_processor.validate_image_file(image_path)
            if not is_valid:
                self._show_error(f"Invalid image file: {error_msg}")
                return

            # Load and display image
            self.current_image_path = image_path
            self._display_image(image_path)
            logger.info(f"Loaded image: {image_path}")

        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            self._show_error(f"Failed to load image: {str(e)}")

    def decode_qr_code(self):
        """Handle QR code decoding from the loaded image."""
        if not self.current_image_path:
            self._show_warning(ERROR_NO_FILE_SELECTED)
            return

        try:
            decoded_text = self.qr_processor.decode_qr_code(self.current_image_path)
            self.textEdit.setText(decoded_text)
            self._show_info(SUCCESS_QR_DECODED)
            logger.info("QR code decoded successfully")

        except QRCodeError as e:
            logger.warning(f"QR decode error: {str(e)}")
            self._show_error(str(e))
        except Exception as e:
            logger.error(f"Unexpected error during QR decode: {str(e)}")
            self._show_error(f"Unexpected error: {str(e)}")

    def generate_qr_code(self):
        """Handle QR code generation from text input."""
        try:
            text = self.textEdit.toPlainText()

            if not text.strip():
                self._show_warning("Please enter some text to generate QR code")
                return

            # Generate QR code
            qr_path = self.qr_processor.generate_qr_code(text)

            # Display generated QR code
            self._display_image(qr_path)
            self.current_image_path = qr_path

            self._show_info(SUCCESS_QR_GENERATED)
            logger.info("QR code generated successfully")

        except QRCodeError as e:
            logger.warning(f"QR generation error: {str(e)}")
            self._show_error(str(e))
        except Exception as e:
            logger.error(f"Unexpected error during QR generation: {str(e)}")
            self._show_error(f"Unexpected error: {str(e)}")

    def save_image(self):
        """Handle saving the currently displayed QR code image."""
        if not self.current_image_path:
            self._show_warning(ERROR_NO_FILE_SELECTED)
            return

        try:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save QR Code",
                f"qrcode{DEFAULT_SAVE_EXTENSION}",
                SUPPORTED_IMAGE_FORMATS
            )

            if not filename:
                logger.debug("Save cancelled by user")
                return

            # Get current pixmap and save
            pixmap = self.label.pixmap()
            if pixmap is None:
                self._show_error("No image to save")
                return

            pixmap.save(filename, DEFAULT_SAVE_FORMAT)
            self._show_info(SUCCESS_FILE_SAVED)
            logger.info(f"Image saved to: {filename}")

        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            self._show_error(f"Failed to save image: {str(e)}")

    def _display_image(self, image_path: Path):
        """
        Display an image in the GUI label.

        Args:
            image_path: Path to the image file
        """
        pixmap = QtGui.QPixmap(str(image_path))
        scaled_pixmap = pixmap.scaled(
            IMAGE_DISPLAY_WIDTH,
            IMAGE_DISPLAY_HEIGHT,
            aspectRatioMode=QtGui.Qt.KeepAspectRatio
        )
        self.label.setPixmap(scaled_pixmap)

    def quit_program(self):
        """Clean up resources and exit the application."""
        logger.info("Application closing")
        self.qr_processor.cleanup_temp_files()
        QApplication.quit()

    def closeEvent(self, event):
        """Handle window close event with cleanup."""
        self.qr_processor.cleanup_temp_files()
        event.accept()

    # UI Helper Methods
    def _show_error(self, message: str):
        """Display error message box."""
        QMessageBox.critical(self, "Error", message)

    def _show_warning(self, message: str):
        """Display warning message box."""
        QMessageBox.warning(self, "Warning", message)

    def _show_info(self, message: str):
        """Display information message box."""
        QMessageBox.information(self, "Success", message)

    def _show_critical_error(self, message: str):
        """Display critical error and log."""
        logger.critical(message)
        QMessageBox.critical(self, "Critical Error", message)


def main():
    """Application entry point with exception handling."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName(WINDOW_TITLE)

        window = QRCodeGUI()

        exit_code = app.exec_()
        logger.info(f"Application exited with code {exit_code}")
        sys.exit(exit_code)

    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
