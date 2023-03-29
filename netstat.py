import os
import psutil


STATE = {
    'ESTABLISHED': 'ESTABLISHED',
    'SYN_SENT': 'SYN_SENT',
    'SYN_RECV': 'SYN_RECV',
    'FIN_WAIT1': 'FIN_WAIT1',
    'FIN_WAIT2': 'FIN_WAIT2',
    'TIME_WAIT': 'TIME_WAIT',
    'CLOSE': 'CLOSE',
    'CLOSE_WAIT': 'CLOSE_WAIT',
    'LAST_ACK': 'LAST_ACK',
    'LISTEN': 'LISTEN',
    'CLOSING': 'CLOSING',
}


def netstat():
    result = []
    for conn in psutil.net_connections(kind='tcp'):
        l_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
        r_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ''
        state = STATE.get(conn.status)
        pid = conn.pid
        try:
            process = psutil.Process(pid)
            user = process.username()
            exe = process.exe()
        except(psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            user = ''
            exe = ''

        nline = [user, l_addr, r_addr, state, pid, exe]
        result.append(nline)
    return result



if __name__ == '__main__':
    for conn in netstat():
        print(conn)