import paramiko
import re

#设置主机列表
host_list=({'ip':'192.168.98.130', 'port':22, 'username':'root', 'password':'123'},
           {'ip':'192.168.98.131', 'port':22, 'username':'root', 'password':'123'},)

ssh = paramiko.SSHClient()
# 设置为接受不在known_hosts 列表的主机可以进行ssh连接
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for host in host_list:
    ssh.connect(hostname=host['ip'], port=host['port'], username=host['username'], password=host['password'])
    print(host['ip'])
    stdin, stdout, stderr = ssh.exec_command('df -lm')
    str_out = stdout.read().decode()
    str_err = stderr.read().decode()

    if str_err != "":
        print(str_err)
        continue

    print(str_out)

    ssh.close()
