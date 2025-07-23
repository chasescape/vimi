from flask import Blueprint
from .auth import auth_bp
from .resume import resume_bp

__all__ = ['auth_bp', 'resume_bp'] 