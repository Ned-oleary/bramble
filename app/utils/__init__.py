from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

def init_utils(app: 'Flask') -> None:
    '''enables .models import'''
    return None
