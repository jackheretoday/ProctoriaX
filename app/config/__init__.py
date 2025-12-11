"""Configuration package"""
from .base import BaseConfig
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

__all__ = [
    'BaseConfig',
    'DevelopmentConfig',
    'ProductionConfig',
    'TestingConfig'
]

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
