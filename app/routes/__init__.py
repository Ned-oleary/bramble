from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

def register_routes(app: 'Flask') -> None:
    '''enables .models import'''
    pass