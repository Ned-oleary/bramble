from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

def init_integrations(app: 'Flask') -> None:
    '''enables .integrations import'''
    pass