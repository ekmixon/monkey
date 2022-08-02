class VictimHost(object):
    def __init__(self, ip_addr, domain_name=""):
        self.ip_addr = ip_addr
        self.domain_name = str(domain_name)
        self.os = {}
        self.services = {}
        self.icmp = False
        self.monkey_exe = None
        self.default_tunnel = None
        self.default_server = None

    def as_dict(self):
        return self.__dict__

    def __hash__(self):
        return hash(self.ip_addr)

    def __eq__(self, other):
        return (
            self.ip_addr.__eq__(other.ip_addr)
            if isinstance(other, VictimHost)
            else False
        )

    def __cmp__(self, other):
        return (
            self.ip_addr.__cmp__(other.ip_addr)
            if isinstance(other, VictimHost)
            else -1
        )

    def __repr__(self):
        return "VictimHost({0!r})".format(self.ip_addr)

    def __str__(self):
        victim = f"Victim Host {self.ip_addr}: "
        victim += "OS - ["
        for k, v in list(self.os.items()):
            victim += f"{k}-{v} "
        victim += "] Services - ["
        for k, v in list(self.services.items()):
            victim += f"{k}-{v} "
        victim += f"] ICMP: {self.icmp} "
        victim += f"target monkey: {self.monkey_exe}"
        return victim

    def set_default_server(self, default_server):
        self.default_server = default_server
