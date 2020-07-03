import paramiko
from scp import SCPClient, SCPException


class SSHManager:
    def __init__(self):
        self.ssh_client = None

    def create_ssh_client(self, hostname, username, password):
        """Create SSH client session to remote server"""
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password)
        else:
            print("SSH client session exist.")

    def close_ssh_client(self):
        """Close SSH client session"""
        self.ssh_client.close()

    def send_file(self, local_path, remote_path):
        """Send a single file to remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path, preserve_times=True)
        except SCPException:
            raise SCPException.message

    def get_file(self, remote_path, local_path):
        """Get a single file from remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)
        except SCPException:
            raise SCPException.message

    def send_command(self, command):
        """Send a single command"""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()


f = open('auth')
i = f.read().split("\n")
id = i[0]
pw = i[1]

l = ["/etc/config/dhcp", "/etc/config/firewall", "/etc/config/network", "/etc/config/openvpn", "/etc/config/wireless", "/etc/squid/squid.conf", "/etc/nginx/nginx.conf", "/etc/firewall.user", "/etc/dnsmasq.conf"]

ssh_manager = SSHManager()
ssh_manager.create_ssh_client("plus10.postech.ac.kr", id, pw)
for k in l:
    u = k.split("/")
    a = ""
    for wow in u[1:-1]:
        a += f"{wow}/"
    ssh_manager.get_file(k, f"../src/{a}")  # 파일다운로드
ssh_manager.close_ssh_client() # 세션종료
