import json
from typing import Union

from flask import current_app
from keycloak import KeycloakAdmin


class KeycloakHelper:
    def __init__(self, base_url: str, realm: str, username: str, password: str):
        self.base_url: str = base_url
        self.realm: str = realm
        self.username: str = username
        self.password: str = password
        self.keycloak_admin: Union[KeycloakAdmin, None] = None
        self._authentificate()
        self.user_endpoint = f"{self.base_url}/admin/realms/{self.realm}/users"
        self.group_endpoint = f"{self.base_url}/admin/realms/{self.realm}/groups"

    def _authentificate(self):
        self.keycloak_admin = KeycloakAdmin(server_url=self.base_url,
                                            username=self.username,
                                            password=self.password,
                                            verify=True)

        self.keycloak_admin.realm_name = self.realm

    @classmethod
    def from_config(cls, config):
        return cls(
            base_url=config.KEYCLOAK_BASE_URL,
            realm=config.KEYCLOAK_REALM,
            username=config.KEYCLOAK_USERNAME,
            password=config.KEYCLOAK_PASSWORD
        )

    def update_user_at_creation(self, user_id: str, first_name: str, last_name: str, attributes: dict) -> bool:
        self._authentificate()
        body = {
            "firstName": first_name,
            "lastName": last_name,
            "attributes": attributes
        }
        self.keycloak_admin.update_user(user_id=user_id, payload=body)

        return True

    def update_user_attributes(self, user_id: str, attributes: dict) -> bool:
        self._authentificate()
        body = {
            "attributes": attributes
        }
        self.keycloak_admin.update_user(user_id=user_id, payload=body)

        return True

    def assign_to_group(self, user_id: str, group_name: str) -> bool:
        self._authentificate()
        group_id = self.keycloak_admin.get_group_by_path(f"/{group_name}")["id"]
        self.keycloak_admin.group_user_add(user_id=user_id, group_id=group_id)
        return True

    def create_user_from_invitation(self, email: str):
        self._authentificate()
        user_id = self.keycloak_admin.create_user({"email": email,
                                                   "username": email,
                                                   "enabled": True,
                                                   "requiredActions": ["UPDATE_PASSWORD",
                                                                       "UPDATE_PROFILE",
                                                                       "VERIFY_EMAIL"]})
        return user_id

    def send_update_email(self, user_id):
        self._authentificate()
        response = self.keycloak_admin.send_update_account(user_id=user_id,
                                                           payload=json.dumps(
                                                               ['UPDATE_PASSWORD', 'UPDATE_PROFILE', 'VERIFY_EMAIL']))
