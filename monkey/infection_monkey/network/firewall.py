import platform
import subprocess
import sys


def _run_netsh_cmd(command, args):
    cmd = subprocess.Popen(
        "netsh %s %s"
        % (
            command,
            " ".join(['%s="%s"' % (key, value) for key, value in list(args.items()) if value]),
        ),
        stdout=subprocess.PIPE,
    )
    return cmd.stdout.read().strip().lower().endswith("ok.")


class FirewallApp(object):
    def is_enabled(self, **kwargs):
        return False

    def add_firewall_rule(self, **kwargs):
        return False

    def remove_firewall_rule(self, **kwargs):
        return False

    def listen_allowed(self, **kwargs):
        return True

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, value, traceback):
        self.close()

    def close(self):
        return


class WinAdvFirewall(FirewallApp):
    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            cmd = subprocess.Popen("netsh advfirewall show currentprofile", stdout=subprocess.PIPE)
            out = cmd.stdout.readlines()

            for line in out:
                if line.startswith("State"):
                    state = line.split()[-1].strip()

            return state == "ON"
        except Exception:
            return None

    def add_firewall_rule(
        self, name="Firewall", direction="in", action="allow", program=sys.executable, **kwargs
    ):
        netsh_args = {
            "name": name,
            "dir": direction,
            "action": action,
            "program": program,
        } | kwargs

        try:
            if _run_netsh_cmd("advfirewall firewall add rule", netsh_args):
                self._rules[name] = netsh_args
                return True
            else:
                return False
        except Exception:
            return None

    def remove_firewall_rule(self, name="Firewall", **kwargs):
        netsh_args = {"name": name} | kwargs
        try:
            if _run_netsh_cmd("advfirewall firewall delete rule", netsh_args):
                if name in self._rules:
                    del self._rules[name]
                return True
            else:
                return False
        except Exception:
            return None

    def listen_allowed(self, **kwargs):
        return (
            any(
                rule.get("program") == sys.executable
                and rule.get("dir") == "in"
                and rule.get("action") == "allow"
                and len(list(rule.keys())) == 4
                for rule in list(self._rules.values())
            )
            if self.is_enabled()
            else True
        )

    def close(self):
        try:
            for rule in list(self._rules.keys()):
                self.remove_firewall_rule(name=rule)
        except Exception:
            pass


class WinFirewall(FirewallApp):
    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            cmd = subprocess.Popen("netsh firewall show state", stdout=subprocess.PIPE)
            out = cmd.stdout.readlines()

            for line in out:
                if line.startswith("Operational mode"):
                    state = line.split("=")[-1].strip()
                elif line.startswith("The service has not been started."):
                    return False

            return state == "Enable"
        except Exception:
            return None

    def add_firewall_rule(
        self,
        rule="allowedprogram",
        name="Firewall",
        mode="ENABLE",
        program=sys.executable,
        **kwargs,
    ):
        netsh_args = {"name": name, "mode": mode, "program": program} | kwargs
        try:
            if _run_netsh_cmd(f"firewall add {rule}", netsh_args):
                netsh_args["rule"] = rule
                self._rules[name] = netsh_args
                return True
            else:
                return False
        except Exception:
            return None

    def remove_firewall_rule(
        self,
        rule="allowedprogram",
        name="Firewall",
        mode="ENABLE",
        program=sys.executable,
        **kwargs,
    ):
        netsh_args = {"program": program} | kwargs
        try:
            if _run_netsh_cmd(f"firewall delete {rule}", netsh_args):
                if name in self._rules:
                    del self._rules[name]
                return True
            else:
                return False
        except Exception:
            return None

    def listen_allowed(self, **kwargs):
        return (
            any(
                rule.get("program") == sys.executable
                and rule.get("mode") == "ENABLE"
                for rule in list(self._rules.values())
            )
            if self.is_enabled()
            else True
        )

    def close(self):
        try:
            for rule in list(self._rules.values()):
                self.remove_firewall_rule(**rule)
        except Exception:
            pass


if sys.platform == "win32":
    try:
        win_ver = int(platform.version().split(".")[0])
    except Exception:
        win_ver = 0
    app = WinAdvFirewall() if win_ver > 5 else WinFirewall()
else:
    app = FirewallApp()
