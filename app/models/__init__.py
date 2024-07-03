from typing import TYPE_CHECKING
from .person import Person
from .company import Company

if TYPE_CHECKING:
    from flask import Flask

def init_models(app: 'Flask') -> None:
    pass
    return None
