from enum import Enum

class ProviderName(Enum):
    apple = 'APPLE'
    facebook = 'FACEBOOK'
    google = 'GOOGLE'
    email = 'EMAIL'


class TokenTypeEnum(Enum):
    access = 'ACCESS'
    refresh = 'REFRESH'
    sign_up = 'SIGN_UP'