from typing import TYPE_CHECKING
from .apollo_routes import bp as ar

if TYPE_CHECKING:
    from flask import Flask

def register_routes(app: 'Flask') -> None:
    '''enables .models import'''
    return None
