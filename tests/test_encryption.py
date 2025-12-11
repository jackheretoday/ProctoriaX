"""Test encryption service"""
import pytest
from app.services.encryption_service import EncryptionService


class TestEncryptionService:
    """Test EncryptionService"""
    
    def test_encrypt_decrypt(self):
        """Test basic encryption/decryption"""
        plaintext = "Hello, World!"
        encrypted = EncryptionService.encrypt(plaintext)
        decrypted = EncryptionService.decrypt(encrypted)
        
        assert encrypted != plaintext
        assert decrypted == plaintext
    
    def test_encrypt_unicode(self):
        """Test Unicode encryption"""
        plaintext = "Hello 世界 🌍"
        encrypted = EncryptionService.encrypt(plaintext)
        decrypted = EncryptionService.decrypt(encrypted)
        
        assert decrypted == plaintext
    
    def test_encrypt_empty_string(self):
        """Test empty string encryption"""
        encrypted = EncryptionService.encrypt("")
        decrypted = EncryptionService.decrypt(encrypted)
        
        assert decrypted == ""
    
    def test_encrypt_long_text(self):
        """Test long text encryption"""
        plaintext = "A" * 10000
        encrypted = EncryptionService.encrypt(plaintext)
        decrypted = EncryptionService.decrypt(encrypted)
        
        assert decrypted == plaintext
    
    def test_encrypt_different_each_time(self):
        """Test encryption produces different ciphertext each time"""
        plaintext = "Test"
        encrypted1 = EncryptionService.encrypt(plaintext)
        encrypted2 = EncryptionService.encrypt(plaintext)
        
        # Different nonces should produce different ciphertext
        assert encrypted1 != encrypted2
        
        # But both decrypt to same plaintext
        assert EncryptionService.decrypt(encrypted1) == plaintext
        assert EncryptionService.decrypt(encrypted2) == plaintext
    
    def test_decrypt_invalid_data(self):
        """Test decryption with invalid data"""
        with pytest.raises(Exception):
            EncryptionService.decrypt("invalid-encrypted-data")
    
    def test_decrypt_corrupted_data(self):
        """Test decryption with corrupted data"""
        plaintext = "Test"
        encrypted = EncryptionService.encrypt(plaintext)
        corrupted = encrypted[:-5] + "12345"
        
        with pytest.raises(Exception):
            EncryptionService.decrypt(corrupted)