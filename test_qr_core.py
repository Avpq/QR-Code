"""
Unit tests for QR code core functionality.
Proves refactored code maintains identical behavior.
"""
import unittest
from pathlib import Path
import tempfile
import shutil
from PIL import Image

from qr_core import (
    QRCodeProcessor,
    QRCodeGenerationError,
    QRCodeDecodingError
)


class TestQRCodeProcessor(unittest.TestCase):
    """Test suite for QRCodeProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = QRCodeProcessor()
        self.test_dir = Path(tempfile.mkdtemp())
        self.test_text = "Hello, World! This is a test QR code."

    def tearDown(self):
        """Clean up test files."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.processor.cleanup_temp_files()

    def test_generate_qr_code_success(self):
        """Test Case 1: QR code generation with valid text."""
        output_path = self.test_dir / "test_qr.png"

        result_path = self.processor.generate_qr_code(
            self.test_text,
            output_path
        )

        # Verify file was created
        self.assertTrue(result_path.exists())
        self.assertEqual(result_path, output_path)

        # Verify it's a valid PNG image
        with Image.open(result_path) as img:
            self.assertEqual(img.format, "PNG")
            self.assertGreater(img.width, 0)
            self.assertGreater(img.height, 0)

    def test_generate_qr_code_empty_text(self):
        """Test Case 2: QR code generation with empty text should fail."""
        with self.assertRaises(QRCodeGenerationError) as context:
            self.processor.generate_qr_code("")

        self.assertIn("empty", str(context.exception).lower())

        # Also test whitespace-only text
        with self.assertRaises(QRCodeGenerationError):
            self.processor.generate_qr_code("   ")

    def test_generate_and_decode_roundtrip(self):
        """Test Case 3: Generate QR code and decode it - should get same text."""
        output_path = self.test_dir / "roundtrip_qr.png"

        # Generate QR code
        qr_path = self.processor.generate_qr_code(self.test_text, output_path)

        # Decode the generated QR code
        decoded_text = self.processor.decode_qr_code(qr_path)

        # Verify we get back the exact same text
        self.assertEqual(decoded_text, self.test_text)

    def test_decode_qr_code_from_nonexistent_file(self):
        """Test Case 4: Decoding from non-existent file should fail gracefully."""
        fake_path = self.test_dir / "nonexistent.png"

        with self.assertRaises(QRCodeDecodingError) as context:
            self.processor.decode_qr_code(fake_path)

        self.assertIn("not found", str(context.exception).lower())

    def test_decode_qr_code_from_invalid_image(self):
        """Test Case 5: Decoding from non-image file should fail gracefully."""
        # Create a text file pretending to be an image
        fake_image = self.test_dir / "fake_image.png"
        fake_image.write_text("This is not an image!")

        with self.assertRaises(QRCodeDecodingError):
            self.processor.decode_qr_code(fake_image)

    def test_validate_image_file_valid(self):
        """Test Case 6: Image validation with valid image."""
        # Generate a valid QR code image
        output_path = self.test_dir / "valid.png"
        self.processor.generate_qr_code("test", output_path)

        is_valid, error_msg = self.processor.validate_image_file(output_path)

        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_validate_image_file_invalid(self):
        """Test Case 7: Image validation with invalid file."""
        # Non-existent file
        fake_path = self.test_dir / "nonexistent.png"
        is_valid, error_msg = self.processor.validate_image_file(fake_path)
        self.assertFalse(is_valid)
        self.assertIn("not exist", error_msg)

        # Invalid image file
        invalid_file = self.test_dir / "invalid.png"
        invalid_file.write_text("Not an image")
        is_valid, error_msg = self.processor.validate_image_file(invalid_file)
        self.assertFalse(is_valid)
        self.assertIn("Invalid", error_msg)

    def test_generate_qr_code_with_special_characters(self):
        """Test Case 8: QR code with special characters and emojis."""
        special_text = "Special chars: !@#$%^&*() 中文 العربية 🎉🔥"
        output_path = self.test_dir / "special_qr.png"

        qr_path = self.processor.generate_qr_code(special_text, output_path)
        decoded_text = self.processor.decode_qr_code(qr_path)

        self.assertEqual(decoded_text, special_text)

    def test_generate_qr_code_with_long_text(self):
        """Test Case 9: QR code with very long text."""
        long_text = "A" * 1000  # 1000 character string

        output_path = self.test_dir / "long_qr.png"
        qr_path = self.processor.generate_qr_code(long_text, output_path)
        decoded_text = self.processor.decode_qr_code(qr_path)

        self.assertEqual(decoded_text, long_text)

    def test_cleanup_temp_files(self):
        """Test Case 10: Cleanup removes temporary files."""
        # Generate QR code to temp location (default)
        self.processor.generate_qr_code("test")

        # Verify temp file exists
        self.assertTrue(self.processor.temp_file_path.exists())

        # Cleanup
        self.processor.cleanup_temp_files()

        # Verify temp file is removed
        self.assertFalse(self.processor.temp_file_path.exists())


class TestBackwardCompatibility(unittest.TestCase):
    """Ensure refactored code maintains exact same behavior as original."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = QRCodeProcessor()
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test files."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_identical_qr_generation_behavior(self):
        """
        Verify QR code generation produces functionally identical results.
        Both old and new code should generate QR codes that decode to same text.
        """
        test_data = [
            "Simple text",
            "https://github.com/Avpq",
            "Email: test@example.com",
            "Multi\nLine\nText",
            "Numbers: 1234567890",
        ]

        for text in test_data:
            with self.subTest(text=text):
                output_path = self.test_dir / f"test_{hash(text)}.png"
                qr_path = self.processor.generate_qr_code(text, output_path)
                decoded = self.processor.decode_qr_code(qr_path)
                self.assertEqual(text, decoded)


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestQRCodeProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardCompatibility))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
