from enum import Enum
from .user import UserIn, UserOut, UserInDB
from .item import Image, Item, Offer
from .execption import UnicornException

__all__ = [
    'UserIn',
    'UserOut',
    'UserInDB',
    'Image',
    'Item',
    'Offer',
    'UnicornException',
]

class ModelName(str, Enum):
    '''
    Class for the model information
    '''
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'
