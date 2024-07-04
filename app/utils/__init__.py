from typing import TYPE_CHECKING
from .hubspot_utils import test_hubspot

if TYPE_CHECKING:
    from flask import Flask

def init_utils(app: 'Flask') -> None:
    '''enables .models import'''
    test_hubspot()
    return None
