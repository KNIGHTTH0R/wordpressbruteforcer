# Controller class
from bruteforcer import Bruteforcer
from xmlrpc import Xmlrpc
from utils import Utils
from view import View

class Controller:
    # init the arguments provided by user
    def __init__(self, args):
        self._args = args
        self._bruteforcer = None

    def start(self):
        View.normal('Reading passwords from file ...')

        # read passwords
        try:
            passwords = Utils.read_passwords(self._args['passwordsfile'])
        except Exception, ex:
            View.error(ex)
            return
        except KeyboardInterrupt:
            View.ctrl_c_pressed()
            return

        View.normal('{} passwords'.format(len(passwords)))

        # check if xmlrpc enabled
        View.normal('Checking if XMLRPC interface is enabled ...')

        # test xmlrpc before bruteforce
        try:
            if not Xmlrpc.test_xmlrpc(self._args['target_url'], self._args['proxy']):
                View.warning('XMLRPC interface is not enabled, stopping')
                return      # not enabled, stop
            else:
                View.normal('XMLRPC interface is enabled')
        except Exception, ex:
            # for some reason
            View.error(ex)
            return
        except KeyboardInterrupt:
            View.ctrl_c_pressed()
            return

        View.new_line()

        # start bruteforcing
        try:
            self._bruteforcer = Bruteforcer(self._args, passwords)
            View.normal('Bruteforce will start in few moments ...')
            self._bruteforcer.start()    # start thread pool
        except Exception, ex:
            View.error(ex)
            return
        except KeyboardInterrupt:
            View.ctrl_c_pressed()
            return

        View.normal('Finished !')

    # CTRL+C pressed
    def stopped(self):
        pass
