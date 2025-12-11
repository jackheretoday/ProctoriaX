# """
# AES-256-GCM Encryption Service
# CRITICAL: All questions, answers, and results must be encrypted
# """
# import os
# import base64
# from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# from cryptography.hazmat.backends import default_backend
# from app.utils.exceptions import EncryptionError


# class EncryptionService:
#     """AES-256-GCM encryption and decryption service"""
    
#     def __init__(self):
#         """Initialize encryption service with key from environment"""
#         self.key = self._get_encryption_key()
#         self.aesgcm = AESGCM(self.key)
    
#     def _get_encryption_key(self):
#         """
#         Get encryption key from environment or generate new one
        
#         Returns:
#             32-byte encryption key
#         """
#         from flask import current_app
        
#         # Try to get key from app config
#         try:
#             key_str = current_app.config.get('ENCRYPTION_KEY')
#         except RuntimeError:
#             # Not in application context, use environment variable
#             key_str = os.getenv('ENCRYPTION_KEY', 'change-this-encryption-key-32b')
        
#         # Ensure key is exactly 32 bytes for AES-256
#         if isinstance(key_str, str):
#             # Pad or truncate to 32 bytes
#             key = key_str.encode('utf-8')
#             if len(key) < 32:
#                 key = key.ljust(32, b'0')
#             elif len(key) > 32:
#                 key = key[:32]
#         else:
#             key = key_str
        
#         if len(key) != 32:
#             raise EncryptionError("Encryption key must be exactly 32 bytes for AES-256")
        
#         return key
    
#     def generate_key(self):
#         """
#         Generate a new random 32-byte encryption key
        
#         Returns:
#             Base64 encoded key string
#         """
#         key = AESGCM.generate_key(bit_length=256)
#         return base64.b64encode(key).decode('utf-8')
    
#     def encrypt_data(self, plain_text):
#         """
#         Encrypt data using AES-256-GCM
        
#         Args:
#             plain_text: String or bytes to encrypt
            
#         Returns:
#             Encrypted bytes (nonce + ciphertext)
#         """
#         try:
#             # Convert to bytes if string
#             if isinstance(plain_text, str):
#                 plain_text = plain_text.encode('utf-8')
            
#             # Generate random nonce (12 bytes for GCM)
#             nonce = os.urandom(12)
            
#             # Encrypt
#             ciphertext = self.aesgcm.encrypt(nonce, plain_text, None)
            
#             # Return nonce + ciphertext
#             return nonce + ciphertext
            
#         except Exception as e:
#             raise EncryptionError(f"Encryption failed: {str(e)}")
    
#     def decrypt_data(self, encrypted_data):
#         """
#         Decrypt data using AES-256-GCM
        
#         Args:
#             encrypted_data: Encrypted bytes (nonce + ciphertext)
            
#         Returns:
#             Decrypted string
#         """
#         try:
#             # Extract nonce (first 12 bytes)
#             nonce = encrypted_data[:12]
#             ciphertext = encrypted_data[12:]
            
#             # Decrypt
#             plain_text = self.aesgcm.decrypt(nonce, ciphertext, None)
            
#             # Return as string
#             return plain_text.decode('utf-8')
            
#         except Exception as e:
#             raise EncryptionError(f"Decryption failed: {str(e)}")
    
#     def encrypt_file(self, file_path):
#         """
#         Encrypt a file in place
        
#         Args:
#             file_path: Path to file to encrypt
#         """
#         try:
#             # Read file
#             with open(file_path, 'rb') as f:
#                 data = f.read()
            
#             # Encrypt
#             encrypted = self.encrypt_data(data)
            
#             # Write encrypted data back
#             with open(file_path, 'wb') as f:
#                 f.write(encrypted)
            
#             return True
            
#         except Exception as e:
#             raise EncryptionError(f"File encryption failed: {str(e)}")
    
#     def decrypt_file(self, file_path, output_path=None):
#         """
#         Decrypt a file
        
#         Args:
#             file_path: Path to encrypted file
#             output_path: Path to save decrypted file (optional)
            
#         Returns:
#             Decrypted data as bytes
#         """
#         try:
#             # Read encrypted file
#             with open(file_path, 'rb') as f:
#                 encrypted_data = f.read()
            
#             # Decrypt
#             decrypted = self.aesgcm.decrypt(
#                 encrypted_data[:12],  # nonce
#                 encrypted_data[12:],  # ciphertext
#                 None
#             )
            
#             # Save to output file if specified
#             if output_path:
#                 with open(output_path, 'wb') as f:
#                     f.write(decrypted)
            
#             return decrypted
            
#         except Exception as e:
#             raise EncryptionError(f"File decryption failed: {str(e)}")
    
#     def encrypt_dict(self, data_dict):
#         """
#         Encrypt a dictionary (convert to JSON first)
        
#         Args:
#             data_dict: Dictionary to encrypt
            
#         Returns:
#             Encrypted bytes
#         """
#         import json
#         json_str = json.dumps(data_dict)
#         return self.encrypt_data(json_str)
    
#     def decrypt_dict(self, encrypted_data):
#         """
#         Decrypt to dictionary (from JSON)
        
#         Args:
#             encrypted_data: Encrypted bytes
            
#         Returns:
#             Decrypted dictionary
#         """
#         import json
#         json_str = self.decrypt_data(encrypted_data)
#         return json.loads(json_str)

"""
AES-256-GCM Encryption Service
CRITICAL: All questions, answers, and results must be encrypted
"""
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from app.utils.exceptions import EncryptionError


class EncryptionService:
    """AES-256-GCM encryption and decryption service"""
    
    @staticmethod
    def _get_encryption_key():
        """
        Get encryption key from environment or generate new one
        
        Returns:
            32-byte encryption key
        """
        from flask import current_app
        
        # Try to get key from app config
        try:
            key_str = current_app.config.get('ENCRYPTION_KEY')
        except RuntimeError:
            # Not in application context, use environment variable
            key_str = os.getenv('ENCRYPTION_KEY', 'change-this-encryption-key-32b')
        
        # Ensure key is exactly 32 bytes for AES-256
        if isinstance(key_str, str):
            # Pad or truncate to 32 bytes
            key = key_str.encode('utf-8')
            if len(key) < 32:
                key = key.ljust(32, b'0')
            elif len(key) > 32:
                key = key[:32]
        else:
            key = key_str
        
        if len(key) != 32:
            raise EncryptionError("Encryption key must be exactly 32 bytes for AES-256")
        
        return key
    
    @staticmethod
    def generate_key():
        """
        Generate a new random 32-byte encryption key
        
        Returns:
            Base64 encoded key string
        """
        key = AESGCM.generate_key(bit_length=256)
        return base64.b64encode(key).decode('utf-8')
    
    @staticmethod
    def encrypt_data(plain_text):
        """
        Encrypt data using AES-256-GCM
        
        Args:
            plain_text: String or bytes to encrypt
            
        Returns:
            Encrypted bytes (nonce + ciphertext)
        """
        try:
            # Get encryption key
            key = EncryptionService._get_encryption_key()
            aesgcm = AESGCM(key)
            
            # Convert to bytes if string
            if isinstance(plain_text, str):
                plain_text = plain_text.encode('utf-8')
            
            # Generate random nonce (12 bytes for GCM)
            nonce = os.urandom(12)
            
            # Encrypt
            ciphertext = aesgcm.encrypt(nonce, plain_text, None)
            
            # Return nonce + ciphertext
            return nonce + ciphertext
            
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt_data(encrypted_data):
        """
        Decrypt data using AES-256-GCM
        
        Args:
            encrypted_data: Encrypted bytes (nonce + ciphertext)
            
        Returns:
            Decrypted string
        """
        try:
            # Get encryption key
            key = EncryptionService._get_encryption_key()
            aesgcm = AESGCM(key)
            
            # Extract nonce (first 12 bytes)
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            
            # Decrypt
            plain_text = aesgcm.decrypt(nonce, ciphertext, None)
            
            # Return as string
            return plain_text.decode('utf-8')
            
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def encrypt_file(input_path, output_path):
        """
        Encrypt a file
        
        Args:
            input_path: Path to file to encrypt
            output_path: Path to save encrypted file
        """
        try:
            # Read file
            with open(input_path, 'rb') as f:
                data = f.read()
            
            # Encrypt
            encrypted = EncryptionService.encrypt_data(data)
            
            # Write encrypted data
            with open(output_path, 'wb') as f:
                f.write(encrypted)
            
            return True
            
        except Exception as e:
            raise EncryptionError(f"File encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt_file(file_path, output_path=None):
        """
        Decrypt a file
        
        Args:
            file_path: Path to encrypted file
            output_path: Path to save decrypted file (optional)
            
        Returns:
            Decrypted data as bytes
        """
        try:
            # Get encryption key
            key = EncryptionService._get_encryption_key()
            aesgcm = AESGCM(key)
            
            # Read encrypted file
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            decrypted = aesgcm.decrypt(
                encrypted_data[:12],  # nonce
                encrypted_data[12:],  # ciphertext
                None
            )
            
            # Save to output file if specified
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(decrypted)
            
            return decrypted
            
        except Exception as e:
            raise EncryptionError(f"File decryption failed: {str(e)}")
    
    @staticmethod
    def encrypt_dict(data_dict):
        """
        Encrypt a dictionary (convert to JSON first)
        
        Args:
            data_dict: Dictionary to encrypt
            
        Returns:
            Encrypted bytes
        """
        import json
        json_str = json.dumps(data_dict)
        return EncryptionService.encrypt_data(json_str)
    
    @staticmethod
    def decrypt_dict(encrypted_data):
        """
        Decrypt to dictionary (from JSON)
        
        Args:
            encrypted_data: Encrypted bytes
            
        Returns:
            Decrypted dictionary
        """
        import json
        json_str = EncryptionService.decrypt_data(encrypted_data)
        return json.loads(json_str)