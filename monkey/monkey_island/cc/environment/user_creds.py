from __future__ import annotations

from typing import Dict

from monkey_island.cc.resources.auth.auth_user import User


class UserCreds:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __bool__(self) -> bool:
        return bool(self.username and self.password_hash)

    def to_dict(self) -> Dict:
        cred_dict = {}
        if self.username:
            cred_dict["user"] = self.username
        if self.password_hash:
            cred_dict["password_hash"] = self.password_hash
        return cred_dict

    def to_auth_user(self) -> User:
        return User(1, self.username, self.password_hash)
