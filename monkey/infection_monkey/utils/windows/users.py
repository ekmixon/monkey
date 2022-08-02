import logging
import subprocess

from infection_monkey.utils.auto_new_user import AutoNewUser
from infection_monkey.utils.new_user_error import NewUserError

ACTIVE_NO_NET_USER = "/ACTIVE:NO"
WAIT_TIMEOUT_IN_MILLISECONDS = 60 * 1000

logger = logging.getLogger(__name__)


def get_windows_commands_to_add_user(username, password, should_be_active=False):
    windows_cmds = ["net", "user", username, password, "/add"]
    if not should_be_active:
        windows_cmds.append(ACTIVE_NO_NET_USER)
    return windows_cmds


def get_windows_commands_to_delete_user(username):
    return ["net", "user", username, "/delete"]


def get_windows_commands_to_deactivate_user(username):
    return ["net", "user", username, ACTIVE_NO_NET_USER]


class AutoNewWindowsUser(AutoNewUser):
    """
    See AutoNewUser's documentation for details.
    """

    def __init__(self, username, password):
        """
        Creates a user with the username + password.
        :raises: subprocess.CalledProcessError if failed to add the user.
        """
        super(AutoNewWindowsUser, self).__init__(username, password)

        windows_cmds = get_windows_commands_to_add_user(self.username, self.password, True)
        logger.debug(
            f"Trying to add {self.username} with commands {str(windows_cmds)}"
        )

        _ = subprocess.check_output(windows_cmds, stderr=subprocess.STDOUT)

    def __enter__(self):
        # Importing these only on windows, as they won't exist on linux.
        import win32con
        import win32security

        try:
            # Logon as new user: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf
            # -winbase-logonusera
            self.logon_handle = win32security.LogonUser(
                self.username,
                ".",  # Use current domain.
                self.password,
                # Logon type - interactive (normal user), since we're using a shell.
                win32con.LOGON32_LOGON_INTERACTIVE,
                win32con.LOGON32_PROVIDER_DEFAULT,
            )  # Which logon provider to use - whatever Windows offers.
        except Exception as err:
            raise NewUserError(f"Can't logon as {self.username}. Error: {str(err)}")
        return self

    def run_as(self, command):
        # Importing these only on windows, as they won't exist on linux.
        import win32api
        import win32event
        import win32process
        from winsys import _advapi32

        exit_code = -1
        process_handle = None
        thread_handle = None

        try:
            # Open process as that user
            # https://github.com/tjguk/winsys/blob/master/winsys/_advapi32.py
            proc_info = _advapi32.CreateProcessWithLogonW(
                username=self.username, domain=".", password=self.password, command_line=command
            )
            process_handle = proc_info.hProcess
            thread_handle = proc_info.hThread

            logger.debug(
                f"Waiting for process to finish. Timeout: {WAIT_TIMEOUT_IN_MILLISECONDS}ms"
            )


            # https://social.msdn.microsoft.com/Forums/vstudio/en-US/b6d6a7ae-71e9-4edb-ac8f
            # -408d2a41750d/what-events-on-a-process-handle-signal-satisify-waitforsingleobject
            # ?forum=vcgeneral
            # Ignoring return code, as we'll use `GetExitCode` to determine the state of the
            # process later.
            _ = win32event.WaitForSingleObject(
                # Waits until the specified object is signaled, or time-out.
                process_handle,  # Ping process handle
                WAIT_TIMEOUT_IN_MILLISECONDS,  # Timeout in milliseconds
            )

            exit_code = win32process.GetExitCodeProcess(process_handle)
        finally:
            try:
                if process_handle is not None:
                    win32api.CloseHandle(process_handle)
                if thread_handle is not None:
                    win32api.CloseHandle(thread_handle)
            except Exception as err:
                logger.error(f"Close handle error: {str(err)}")

        return exit_code

    def __exit__(self, _exc_type, value, traceback):
        # Logoff
        self.logon_handle.Close()

        # Try to disable and then delete the user.
        self.try_deactivate_user()
        self.try_delete_user()

    def try_deactivate_user(self):
        try:
            commands_to_deactivate_user = get_windows_commands_to_deactivate_user(self.username)
            logger.debug(
                f"Trying to deactivate {self.username} with commands {str(commands_to_deactivate_user)}"
            )

            _ = subprocess.check_output(commands_to_deactivate_user, stderr=subprocess.STDOUT)
        except Exception as err:
            raise NewUserError(f"Can't deactivate user {self.username}. Info: {err}")

    def try_delete_user(self):
        try:
            commands_to_delete_user = get_windows_commands_to_delete_user(self.username)
            logger.debug(
                f"Trying to delete {self.username} with commands {str(commands_to_delete_user)}"
            )

            _ = subprocess.check_output(commands_to_delete_user, stderr=subprocess.STDOUT)
        except Exception as err:
            raise NewUserError(f"Can't delete user {self.username}. Info: {err}")
