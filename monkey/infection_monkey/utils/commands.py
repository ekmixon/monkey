from infection_monkey.config import GUID
from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG
from infection_monkey.model.host import VictimHost


def build_monkey_commandline(
    target_host: VictimHost, depth: int, vulnerable_port: str, location: str = None
) -> str:

    return " " + " ".join(
        build_monkey_commandline_explicitly(
            GUID,
            target_host.default_tunnel,
            target_host.default_server,
            depth,
            location,
            vulnerable_port,
        )
    )


def build_monkey_commandline_explicitly(
    parent: str = None,
    tunnel: str = None,
    server: str = None,
    depth: int = None,
    location: str = None,
    vulnerable_port: str = None,
) -> list:
    cmdline = []

    if parent is not None:
        cmdline.extend(("-p", parent))
    if tunnel is not None:
        cmdline.extend(("-t", tunnel))
    if server is not None:
        cmdline.extend(("-s", server))
    if depth is not None:
        depth = max(depth, 0)
        cmdline.extend(("-d", str(depth)))
    if location is not None:
        cmdline.extend(("-l", location))
    if vulnerable_port is not None:
        cmdline.extend(("-vp", vulnerable_port))
    return cmdline


def get_monkey_commandline_windows(destination_path: str, monkey_cmd_args: list) -> list:
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args


def get_monkey_commandline_linux(destination_path: str, monkey_cmd_args: list) -> list:
    monkey_cmdline = [destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args
