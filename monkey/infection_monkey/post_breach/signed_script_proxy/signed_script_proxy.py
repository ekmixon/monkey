import subprocess

from infection_monkey.post_breach.signed_script_proxy.windows.signed_script_proxy import (
    get_windows_commands_to_delete_temp_comspec,
    get_windows_commands_to_proxy_execution_using_signed_script,
    get_windows_commands_to_reset_comspec,
)
from infection_monkey.utils.environment import is_windows_os


def get_commands_to_proxy_execution_using_signed_script():
    return get_windows_commands_to_proxy_execution_using_signed_script()


def cleanup_changes(original_comspec):
    if is_windows_os():
        subprocess.run(  # noqa: DUO116
            get_windows_commands_to_reset_comspec(original_comspec), shell=True
        )
        subprocess.run(get_windows_commands_to_delete_temp_comspec(), shell=True)  # noqa: DUO116
