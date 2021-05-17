import requests
import os

# from dotenv import load_dotenv
# load_dotenv("../../.env")

KONG_HOST_IP = os.environ.get("KONG_HOST_IP")
KONG_PORT = os.environ.get("KONG_PORT")

KONG_URL = os.environ.get("KONG_URL", f"http://{KONG_HOST_IP}:{KONG_PORT}")

KEYCLOAK_HOST_IP = os.environ.get("KEYCLOAK_HOST_IP")
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT")
IS_PROD = os.environ.get("PROD") == "true"

BACKEND_URI = os.environ.get("BACKEND_URI")
FRONTEND_URI = os.environ.get("FRONTEND_URI")
FRONTEND_TEST_URI = FRONTEND_URI + "test"
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SGE_API_KEY = os.environ.get("SGE_API_KEY")
REALM_NAME = "enki"
AUTH_URI = os.environ.get("AUTH_URI", f"http://{KEYCLOAK_HOST_IP}:{KEYCLOAK_PORT}")

ENKI_BACKEND_SERVICE_ID = os.environ.get("ENKI_BACKEND_SERVICE_ID")
ENKI_FRONT_SERVICE_ID = os.environ.get("ENKI_FRONT_SERVICE_ID")

introspection_url = f'{AUTH_URI}/auth/realms/{REALM_NAME}/protocol/openid-connect/token/introspect'
discovery_url = f'{AUTH_URI}/auth/realms/{REALM_NAME}/.well-known/openid-configuration'

services = [
    {
        'name': "enki_api",
        'url': BACKEND_URI,

        "routes": [
            {
                "path": '/api',
                'auth': 'oidc'
            },
            {
                'path': '/echanges',
                'auth': 'api_key'
            }
        ]
    },
    {
        'name': "enki_front",
        'url': FRONTEND_URI,
        'routes': [
            {
                'path': '/',
                "auth": "oidc"
            },
        ]
    },
    {
        'name': "enki_front_test",
        'url': FRONTEND_TEST_URI,
        'routes': [
            {
                'path': '/test',
            },
        ]
    }
]

response = requests.get(f'{KONG_URL}/routes')
for _id in [e["id"] for e in response.json()["data"]]:
    response = requests.delete(f'{KONG_URL}/routes/{_id}')

response = requests.get(f'{KONG_URL}/services')
for _id in [e["id"] for e in response.json()["data"]]:
    reponse = requests.delete(f'{KONG_URL}/services/{_id}')

for service in services:
    print(f"Start configuring {service['name']}")
    response = requests.post(f'{KONG_URL}/services', data={
        'name': service["name"],
        'url': service["url"]
    })
    created_service_id = response.json()["id"]
    for route in service["routes"]:
        auth_type = route.get("auth")

        print(f"configuring route {route['path']}... with {auth_type}")
        response = requests.post(f'{KONG_URL}/services/{service["name"]}/routes', data={
            'service.id': created_service_id,
            'paths[]': route["path"],
        })
        route_id = response.json()["id"]

        if auth_type == "api_key":
            response = requests.post(f'{KONG_URL}/routes/{route_id}/plugins', data={
                'name': "key-auth",
                'config.key_names': "x-api-key",
            })
            response = requests.post(f'{KONG_URL}/consumers', data={
                'username': "sge-hub",
            })
            response = requests.post(f'{KONG_URL}/consumers/sge-hub/key-auth', data={
                'key': SGE_API_KEY,
            })

        elif auth_type == "oidc":
            data = {
                'name': 'oidc',
                'config.client_id': f'{CLIENT_ID}',
                'config.client_secret': f'{CLIENT_SECRET}',
                'config.realm': f'{REALM_NAME}',
                'config.bearer_only': 'false',
                'config.introspection_endpoint': introspection_url,
                'config.discovery': discovery_url
            }

            response = requests.post(f'{KONG_URL}/routes/{route_id}/plugins', data=data)
        else:
            print("No oidc")
            pass
