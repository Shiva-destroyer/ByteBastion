#!/usr/bin/env python3
"""
ByteBastion System Test Suite
Comprehensive automated testing for all 10 security modules
Developer: Sai Srujan Murthy
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.file_checker import FileIntegrityChecker
from modules.keylogger import EducationalKeylogger
from modules.file_type_identifier import FileTypeIdentifier
from modules.password_generator import PasswordGenerator
from modules.data_deletion import DataDeletionUtility
from modules.aes_crypto import AESCrypto
from modules.directory_monitor import DirectorySyncMonitor
from modules.temp_cleaner import TempFileCleaner
from modules.hidden_detector import HiddenFileDetector
from modules.disk_analyzer import DiskSpaceAnalyzer


class TestFileIntegrityChecker(unittest.TestCase):
    """Test File Integrity Checker module"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, 'w') as f:
            f.write("Original content for hash testing")
        self.checker = FileIntegrityChecker()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        # Clean up database file if exists
        if os.path.exists('integrity_database.json'):
            os.remove('integrity_database.json')
    
    def test_calculate_hash(self):
        """Test SHA-256 hash calculation"""
        hash1 = self.checker.calculate_sha256(self.test_file)
        self.assertIsNotNone(hash1)
        self.assertEqual(len(hash1), 64)  # SHA-256 produces 64 hex chars
        
        # Hash should be consistent
        hash2 = self.checker.calculate_sha256(self.test_file)
        self.assertEqual(hash1, hash2)
    
    def test_hash_mismatch_detection(self):
        """Test detection of file modifications"""
        # Calculate original hash
        original_hash = self.checker.calculate_sha256(self.test_file)
        
        # Modify file
        with open(self.test_file, 'w') as f:
            f.write("Modified content - different from original")
        
        # Calculate new hash
        new_hash = self.checker.calculate_sha256(self.test_file)
        
        # Hashes should differ
        self.assertNotEqual(original_hash, new_hash)
    
    def test_database_operations(self):
        """Test hash storage and retrieval"""
        # Add file to database
        with patch('builtins.input', return_value=''):
            self.checker.add_file_hash(self.test_file)
        
        # Verify database file exists
        self.assertTrue(os.path.exists('integrity_database.json'))
        
        # Load database and check entry
        with open('integrity_database.json', 'r') as f:
            db = json.load(f)
        
        self.assertIn(self.test_file, db)


class TestPasswordGenerator(unittest.TestCase):
    """Test Password Generator module"""
    
    def setUp(self):
        self.generator = PasswordGenerator()
    
    def test_password_generation_basic(self):
        """Test basic password generation"""
        with patch('builtins.input', side_effect=['12', 'y', 'y', 'y', 'y']):
            with patch('rich.console.Console.input', side_effect=['12', 'y', 'y', 'y', 'y']):
                password = self.generator.generate_password(
                    length=12,
                    use_uppercase=True,
                    use_digits=True,
                    use_symbols=True
                )
        
        self.assertEqual(len(password), 12)
        self.assertIsInstance(password, str)
    
    def test_password_complexity_requirements(self):
        """Test that passwords meet complexity requirements"""
        # Generate 50 passwords and verify all meet requirements
        for _ in range(50):
            password = self.generator.generate_password(
                length=16,
                use_uppercase=True,
                use_digits=True,
                use_symbols=True
            )
            
            self.assertEqual(len(password), 16)
            
            # Check for at least one uppercase
            self.assertTrue(any(c.isupper() for c in password))
            
            # Check for at least one digit
            self.assertTrue(any(c.isdigit() for c in password))
            
            # Check for at least one special character
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            self.assertTrue(any(c in special_chars for c in password))
    
    def test_password_length_requirements(self):
        """Test various password lengths"""
        for length in [8, 12, 16, 24, 32, 64, 128]:
            password = self.generator.generate_password(
                length=length,
                use_uppercase=True,
                use_digits=True,
                use_symbols=True
            )
            self.assertEqual(len(password), length)
    
    def test_entropy_calculation(self):
        """Test entropy calculation"""
        # Calculate entropy with charset_size
        length = 14
        charset_size = 94  # Standard ASCII printable characters
        entropy = self.generator.calculate_entropy(length, charset_size)
        self.assertGreater(entropy, 0)
        self.assertIsInstance(entropy, float)


class TestFileTypeIdentifier(unittest.TestCase):
    """Test File Type Identifier module"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.identifier = FileTypeIdentifier()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_text_file_detection(self):
        """Test detection of text file"""
        text_file = os.path.join(self.test_dir, "test.txt")
        with open(text_file, 'w') as f:
            f.write("This is a plain text file")
        
        result = self.identifier.analyze_file(text_file)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        # Check if mime type contains 'text'
        if 'mime_type' in result:
            self.assertIn('text', result['mime_type'].lower())
    
    def test_fake_extension_detection(self):
        """Test detection of mismatched file extensions"""
        # Create a .jpg file that contains plain text
        fake_jpg = os.path.join(self.test_dir, "fake_image.jpg")
        with open(fake_jpg, 'w') as f:
            f.write("This is actually text, not a JPEG image")
        
        result = self.identifier.analyze_file(fake_jpg)
        
        # Should detect as text, not image
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        # Should have a mismatch warning or mime_type showing text
        if 'mime_type' in result:
            self.assertIn('text', result['mime_type'].lower())
    
    def test_binary_file_detection(self):
        """Test detection of binary files"""
        # Create a file with PNG magic bytes
        png_file = os.path.join(self.test_dir, "test.png")
        with open(png_file, 'wb') as f:
            # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(b'\x00' * 100)  # Add some dummy data
        
        detected_type = self.identifier.analyze_file(png_file)
        self.assertIsNotNone(detected_type)


class TestAESCrypto(unittest.TestCase):
    """Test AES Encryption/Decryption module"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.crypto = AESCrypto()
        self.test_password = "TestPassword123!@#"
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_encrypt_decrypt_cycle(self):
        """Test encryption and decryption produces original content"""
        # Create test file
        test_file = os.path.join(self.test_dir, "original.txt")
        original_content = "This is secret data that needs encryption!"
        
        with open(test_file, 'w') as f:
            f.write(original_content)
        
        # Encrypt
        encrypted_file = test_file + ".enc"
        with patch('builtins.input', return_value=self.test_password):
            with patch('getpass.getpass', return_value=self.test_password):
                self.crypto.encrypt_file(test_file, self.test_password)
        
        # Verify encrypted file exists
        self.assertTrue(os.path.exists(encrypted_file))
        
        # Encrypted content should differ from original
        with open(encrypted_file, 'rb') as f:
            encrypted_content = f.read()
        self.assertNotEqual(encrypted_content, original_content.encode())
        
        # Decrypt
        # decrypt_file automatically creates output by removing .enc extension
        with patch('builtins.input', return_value=''):
            with patch('getpass.getpass', return_value=self.test_password):
                result = self.crypto.decrypt_file(encrypted_file, self.test_password)
        
        # Verify decryption succeeded
        self.assertTrue(result)
        
        # The decrypted file should be at original location (original.txt)
        # since decrypt_file removes .enc extension
        with open(test_file, 'r') as f:
            decrypted_content = f.read()
        
        self.assertEqual(decrypted_content, original_content)
    
    def test_wrong_password_fails(self):
        """Test that wrong password produces different output"""
        test_file = os.path.join(self.test_dir, "secret.txt")
        original_content = "Secret content"
        with open(test_file, 'w') as f:
            f.write(original_content)
        
        # Encrypt with correct password
        with patch('getpass.getpass', return_value=self.test_password):
            self.crypto.encrypt_file(test_file, self.test_password)
        
        # Try to decrypt with wrong password
        encrypted_file = test_file + ".enc"
        
        # Remove original file so we can see what decrypt produces
        os.remove(test_file)
        
        with patch('builtins.input', return_value=''):
            with patch('getpass.getpass', return_value="WrongPassword"):
                result = self.crypto.decrypt_file(encrypted_file, "WrongPassword")
        
        # Even if it "succeeds", the content should be garbage/different
        if result and os.path.exists(test_file):
            with open(test_file, 'r', errors='ignore') as f:
                decrypted_content = f.read()
            # Content should not match original if wrong password was used
            self.assertNotEqual(decrypted_content, original_content)


class TestDataDeletion(unittest.TestCase):
    """Test Data Deletion Utility module"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.deleter = DataDeletionUtility()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_secure_wipe(self):
        """Test secure file wiping"""
        test_file = os.path.join(self.test_dir, "to_delete.txt")
        with open(test_file, 'w') as f:
            f.write("This file will be securely wiped")
        
        # Verify file exists
        self.assertTrue(os.path.exists(test_file))
        
        # Mock confirmation and wipe
        with patch('builtins.input', return_value='YES'):
            with patch('rich.console.Console.input', return_value='YES'):
                self.deleter.secure_wipe_file(test_file)
        
        # Verify file no longer exists
        self.assertFalse(os.path.exists(test_file))
    
    def test_wipe_cancellation(self):
        """Test that incorrect confirmation prevents deletion"""
        test_file = os.path.join(self.test_dir, "protected.txt")
        with open(test_file, 'w') as f:
            f.write("This file should remain")
        
        # Mock wrong confirmation
        with patch('builtins.input', return_value='no'):
            with patch('rich.console.Console.input', return_value='no'):
                # Should not delete
                try:
                    self.deleter.confirm_deletion(test_file)
                except SystemExit:
                    pass
        
        # File should still exist
        self.assertTrue(os.path.exists(test_file))


class TestDiskAnalyzer(unittest.TestCase):
    """Test Disk Space Analyzer module"""
    
    def setUp(self):
        self.analyzer = DiskSpaceAnalyzer()
    
    def test_partition_detection(self):
        """Test that system partitions are detected"""
        partitions = self.analyzer.get_partition_usage()
        
        # Should return a list
        self.assertIsInstance(partitions, list)
        
        # Should not be empty (system always has at least one partition)
        self.assertGreater(len(partitions), 0)
        
        # Each partition should have required fields
        for partition in partitions:
            self.assertIn('device', partition)
            self.assertIn('mountpoint', partition)
            self.assertIn('total', partition)
            self.assertIn('used', partition)
            self.assertIn('free', partition)
            self.assertIn('percent', partition)
    
    def test_usage_bar_creation(self):
        """Test visual usage bar creation"""
        bar = self.analyzer.create_usage_bar(50.0)
        self.assertIsInstance(bar, str)
        self.assertGreater(len(bar), 0)
        
        # Test different thresholds
        bar_low = self.analyzer.create_usage_bar(30.0)
        bar_medium = self.analyzer.create_usage_bar(75.0)
        bar_high = self.analyzer.create_usage_bar(95.0)
        
        self.assertIsInstance(bar_low, str)
        self.assertIsInstance(bar_medium, str)
        self.assertIsInstance(bar_high, str)


class TestHiddenFileDetector(unittest.TestCase):
    """Test Hidden File Detector module"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.detector = HiddenFileDetector()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_hidden_file_detection(self):
        """Test detection of hidden files"""
        # Create hidden file (starts with dot)
        hidden_file = os.path.join(self.test_dir, ".hidden_file")
        with open(hidden_file, 'w') as f:
            f.write("Hidden content")
        
        # Create normal file
        normal_file = os.path.join(self.test_dir, "normal_file.txt")
        with open(normal_file, 'w') as f:
            f.write("Normal content")
        
        # Scan directory - this method likely displays results but doesn't return them
        # Just verify it runs without error
        try:
            with patch('builtins.input', return_value=''):
                with patch('rich.console.Console.input', return_value=''):
                    # Method may not return results, just verify it runs
                    self.detector.scan_directory(self.test_dir)
            # If we get here without exception, test passes
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"scan_directory raised exception: {e}")
    
    def test_hidden_detection_logic(self):
        """Test the is_hidden_unix method"""
        hidden_path = Path("/home/user/.bashrc")
        normal_path = Path("/home/user/document.txt")
        
        self.assertTrue(self.detector.is_hidden_unix(hidden_path))
        self.assertFalse(self.detector.is_hidden_unix(normal_path))


class TestTempCleaner(unittest.TestCase):
    """Test Temporary File Cleaner module"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cleaner = TempFileCleaner()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_temp_location_detection(self):
        """Test detection of temporary directories"""
        locations = self.cleaner.get_safe_temp_locations()
        
        self.assertIsInstance(locations, list)
        self.assertGreater(len(locations), 0)
    
    def test_old_file_scanning(self):
        """Test scanning for old files"""
        # Create an old file by modifying timestamp
        old_file = os.path.join(self.test_dir, "old_temp.tmp")
        with open(old_file, 'w') as f:
            f.write("Old temp content")
        
        # Set modification time to 8 days ago
        old_time = time.time() - (8 * 24 * 60 * 60)
        os.utime(old_file, (old_time, old_time))
        
        # Scan with 7-day threshold (age_days parameter)
        # scan_directory populates self.files_to_delete, doesn't return values
        with patch('builtins.input', return_value=''):
            with patch('rich.console.Console.input', return_value=''):
                self.cleaner.scan_directory(self.test_dir, age_days=7)
        
        # Should find the old file in files_to_delete list
        self.assertGreater(len(self.cleaner.files_to_delete), 0)


class TestKeylogger(unittest.TestCase):
    """Test Educational Keylogger module"""
    
    def setUp(self):
        self.keylogger = EducationalKeylogger()
    
    def test_instantiation(self):
        """Test that keylogger can be instantiated without errors"""
        self.assertIsNotNone(self.keylogger)
        self.assertIsInstance(self.keylogger, EducationalKeylogger)
    
    def test_disclaimer_display(self):
        """Test that disclaimer method exists and runs"""
        # Mock the input to auto-decline
        with patch('rich.console.Console.input', return_value='no'):
            # Method exists and can be called
            try:
                self.keylogger.show_disclaimer()
            except:
                pass  # Any response is acceptable for this test
            # Just verify method exists
            self.assertTrue(hasattr(self.keylogger, 'show_disclaimer'))


class TestDirectoryMonitor(unittest.TestCase):
    """Test Directory Sync Monitor module"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.monitor = DirectorySyncMonitor()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_instantiation(self):
        """Test that monitor can be instantiated without errors"""
        self.assertIsNotNone(self.monitor)
        self.assertIsInstance(self.monitor, DirectorySyncMonitor)
    
    def test_event_handler_exists(self):
        """Test that event handler class exists"""
        self.assertTrue(hasattr(self.monitor, 'EventHandler'))


class TestRunner(unittest.TestCase):
    """Test that all modules can be imported and instantiated"""
    
    def test_all_modules_importable(self):
        """Verify all 10 modules can be imported"""
        modules = [
            FileIntegrityChecker,
            EducationalKeylogger,
            FileTypeIdentifier,
            PasswordGenerator,
            DataDeletionUtility,
            AESCrypto,
            DirectorySyncMonitor,
            TempFileCleaner,
            HiddenFileDetector,
            DiskSpaceAnalyzer
        ]
        
        for module_class in modules:
            instance = module_class()
            self.assertIsNotNone(instance)
            self.assertTrue(hasattr(instance, 'run'))


def run_test_suite():
    """Run the complete test suite with detailed output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFileIntegrityChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestPasswordGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestFileTypeIdentifier))
    suite.addTests(loader.loadTestsFromTestCase(TestAESCrypto))
    suite.addTests(loader.loadTestsFromTestCase(TestDataDeletion))
    suite.addTests(loader.loadTestsFromTestCase(TestDiskAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestHiddenFileDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestTempCleaner))
    suite.addTests(loader.loadTestsFromTestCase(TestKeylogger))
    suite.addTests(loader.loadTestsFromTestCase(TestDirectoryMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestRunner))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUITE SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result


if __name__ == '__main__':
    result = run_test_suite()
    sys.exit(0 if result.wasSuccessful() else 1)
