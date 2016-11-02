from socket import inet_aton
from multiprocessing import cpu_count

class Utils:
    # get the "good" number of threads, based on CPU
    @staticmethod
    def max_threads():
        return cpu_count() * 3
    # parse time
    # result: seconds or minutes
    @staticmethod
    def time_parser(t):
        if t > 60:
            t_s = int(t / 60)
            if t_s == 1:
                return '1 minute'
            else:
                return '{} minutes'.format(t_s)
        else:
            t_s = int(t)
            if t_s == 1:
                return '1 second'
            else:
                return '{} seconds'.format(t_s)

    # reads the passwords passwords
    @staticmethod
    def read_passwords(passwords_file):
        passwords = []
        with open(passwords_file, 'r') as f:
            for line in f:
                passwords.append(line.strip())
        return passwords
    # check if IP address is valid x.x.x.x, x - [0, 255]
    @staticmethod
    def valid_ip(ip):
        try:
            inet_aton(ip)
            return True
            # legal
        except:
            return False