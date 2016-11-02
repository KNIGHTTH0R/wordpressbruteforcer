import argparse
from os.path import exists as file_exists
from utils import Utils

# class that handles the arguments given by user
class ArgumentParser:
    def __init__(self):
        pass

    # takes care of the arguments (gets and validates)
    def args(self):
        # arguments given by user
        args = self.retrieve_args()
        # gets validated args otherwise exception is raised
        validated_args = self.validate_arguments(args)
        # return the validated args
        return validated_args
    # gets the arguments given by user using argparse
    def retrieve_args(self):
        parser = argparse.ArgumentParser(description='Wordpress bruteforcer')
        parser.add_argument('--target',
                            action='store',
                            dest='target_url',
                            help='Wordpress URL (eg. http://mywp.com or http://mywp.com:80)')
        parser.add_argument('--username',
                            action='store',
                            dest='username',
                            help='Wordpress username')
        parser.add_argument('--passwordsfile',
                            action='store',
                            dest='passwordsfile',
                            help='File containing passwords')
        parser.add_argument('--threads',
                            action='store',
                            dest='threads',
                            help='Number of threads to run (default 1)')
        parser.add_argument('--proxy',
                            action='store',
                            dest='proxy',
                            help='A proxy chain in this format type[socks5/socks4/http]:host:port (eg. socks5:127.0.0.1:8080)')
        parser.add_argument('--timeout',
                            type=int,
                            action='store',
                            dest='timeout',
                            help='Requests timeout (in seconds)')
        parser.add_argument('--verbose',
                            action='store_true',
                            dest='verbose',
                            help='Prints details about the scanning')
        args = parser.parse_args()
        return args

    # validates the arguments given
    def validate_arguments(self, args):
        if not args.target_url:
            raise Exception('Target url missing')
        if not args.target_url.startswith('http'):
            raise Exception('Invalid url: {}, missing protocol (http or https)'.format(args.target_url))
        if not args.username:
            raise Exception('Username not given')
        if not args.passwordsfile:
            raise Exception('Passwords file not given')

        if not file_exists(args.passwordsfile):
            raise Exception('Passwords file does not exist')

        new_args = {}
        new_args['target_url'] = args.target_url
        new_args['username'] = args.username
        new_args['passwordsfile'] = args.passwordsfile

        # threads
        if not args.threads:
            new_args['threads'] = 1     # threads arguments not given, set to 1
        else:
            if args.threads == 'MAX':
                # threads argument set to max
                # set threads number based on cpu count
                new_args['threads'] = Utils.max_threads()
            else:
                # should be a number here
                try:
                    new_args['threads'] = int(args.threads)
                except:
                    # no number, wrong threads argument format
                    raise Exception('Threads argument can be a number or MAX')

        # proxy enabled
        if args.proxy:
            p = args.proxy
            s = p.split(':')
            proxy = {}
            if len(s) is not 3:
                raise Exception('Invalid proxy format: {}'.format(p))

            # wrong protocol
            if s[0] != 'socks5' and s[0] != 'socks4' and s[0] != 'http':
                raise Exception('Unknown proxy protocol: {}'.format(s[0]))

            if not Utils.valid_ip(s[1]):
                raise Exception('Invalid IP address: {}'.format(s[1]))

            # proxy port is not a number
            try:
                i = int(s[2])
            except:
                raise Exception('Invalid port number: {}'.format(s[2]))

            proxy = {}

            # if http proxy, set the https connections
            # to go through it as well
            if s[0] == 'http':
                proxy['http'] = 'http://{}:{}'.format(s[1], s[2])
                proxy['https'] = 'http://{}:{}'.format(s[1], s[2])
            else:
                # socks4 or socks5
                proxy[s[0]] = '{}:{}'.format(s[1], s[2])

            # save it in dict
            new_args['proxy'] = proxy
        else:
            new_args['proxy'] = None

        # timeout given
        if args.timeout:
            new_args['timeout'] = args.timeout
        else:
            new_args['timeout'] = None

        # verbose
        if args.verbose:
            new_args['verbose'] = args.verbose
        else:
            new_args['verbose'] = False

        return new_args