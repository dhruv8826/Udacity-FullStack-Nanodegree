import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = 'dev-cbsboi1u.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'empComp'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    authorisation = request.headers.get('Authorization', None)

    if not authorisation:
        raise AuthError({'code': 'header issue', 'description': 'authorisation missing in header'}, 401)
    
    auth_token = authorisation.split(' ')
    if auth_token[0].upper() != 'BEARER':
        raise AuthError({'code': 'authorisation token issue', 'description': 'authorisation header does not start with Bearer keyword'}, 401)
    elif len(auth_token) < 2:
        raise AuthError({'code': 'authorisation token issue', 'description': 'authorisation token missing'}, 401)
    elif len(auth_token) > 2:
        raise AuthError({'code': 'authorisation token issue', 'description': 'invalid authorisation token'}, 401)
    
    return auth_token[1]

def check_permissions(permission, payload):
    if not 'permissions' in payload:
        raise AuthError({'code': 'permission issue', 'description': 'permission not in token info'}, 400)
    if not permission in payload['permissions']:
        raise AuthError({'code': 'permission issue', 'description': 'permission not found'}, 403)
    return True

def verify_decode_jwt(token):
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key={}
    if 'kid' not in unverified_header:
        raise AuthError({'code': 'header issue', 'description': 'Authorisation malformed.'}, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
        }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError({'code': 'jwt token issue', 'description': 'Invalid Token'}, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator