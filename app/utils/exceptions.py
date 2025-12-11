"""
Custom exceptions
"""


class ApplicationError(Exception):
    """Base application exception"""
    pass


class AuthenticationError(ApplicationError):
    """Authentication failed"""
    pass


class AuthorizationError(ApplicationError):
    """Authorization failed - insufficient permissions"""
    pass


class ValidationError(ApplicationError):
    """Validation error"""
    pass


class EncryptionError(ApplicationError):
    """Encryption/Decryption error"""
    pass


class SessionError(ApplicationError):
    """Session error"""
    pass


class FileUploadError(ApplicationError):
    """File upload error"""
    pass


class DatabaseError(ApplicationError):
    """Database operation error"""
    pass
