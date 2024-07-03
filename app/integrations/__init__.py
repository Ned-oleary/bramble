from typing import TYPE_CHECKING
from .bramble_hubspot import init_hubspot

if TYPE_CHECKING:
    from flask import Flask

def init_integrations(app: 'Flask') -> None:
    '''enables .integrations import'''
    init_hubspot()
    return None

