import datetime
import logging
import shlex
import subprocess

from infection_monkey.utils.auto_new_user import AutoNewUser

logger = logging.getLogger(__name__)


def get_linux_commands_to_add_user(username):
    return [
        "useradd",
        "-M",
        "--expiredate",
        datetime.datetime.now().strftime("%Y-%m-%d"),
        "--inactive",
        "0",
        "-c",
        "MONKEY_USER",
        username,
    ]


def get_linux_commands_to_delete_user(username):
    return ["deluser", username]


class AutoNewLinuxUser(AutoNewUser):
    """
    See AutoNewUser's documentation for details.
    """

    def __init__(self, username, password):
        """
        Creates a user with the username + password.
        :raises: subprocess.CalledProcessError if failed to add the user.
        """
        super(AutoNewLinuxUser, self).__init__(username, password)

        commands_to_add_user = get_linux_commands_to_add_user(username)
        logger.debug(
            f"Trying to add {self.username} with commands {str(commands_to_add_user)}"
        )

        _ = subprocess.check_output(commands_to_add_user, stderr=subprocess.STDOUT)

    def __enter__(self):
        return self  # No initialization/logging on needed in Linux

    def run_as(self, command):
        command_as_new_user = shlex.split(
            "sudo -u {username} {command}".format(username=self.username, command=command)
        )
        return subprocess.call(command_as_new_user)

    def __exit__(self, _exc_type, value, traceback):
        # delete the user.
        commands_to_delete_user = get_linux_commands_to_delete_user(self.username)
        logger.debug(
            f"Trying to delete {self.username} with commands {str(commands_to_delete_user)}"
        )

        _ = subprocess.check_output(commands_to_delete_user, stderr=subprocess.STDOUT)
