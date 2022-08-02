from monkey_island.cc.environment import Environment


class PasswordEnvironment(Environment):
    _credentials_required = True

    def get_auth_users(self):
        return self._config.get_users() if self._is_registered() else []
