class View:
    # banner
    @staticmethod
    def banner():
        View.new_line()
        print '[+] Wordpress bruteforcer'
        print '[+] getyourbots.com'
        View.new_line()

    # prints a message
    @staticmethod
    def normal(msg):
        print '[+] {}'.format(msg)

    # password check print
    @staticmethod
    def password(password, status_code, resp_length):
        print '[+] {} - {} - {}'.format(password, status_code, resp_length)

    # found passwords
    @staticmethod
    def found_password(password):
        View.new_line()
        print '[+] FOUND PASSWORD: {}'.format(password)
        View.new_line()

    # prints a warning
    @staticmethod
    def warning(warning):
        print '[-] {}'.format(warning)

    # prints an error
    @staticmethod
    def error(error):
        print '[!] Error: {}'.format(error)

    # ctrl+c key combination was pressed
    @staticmethod
    def ctrl_c_pressed():
        View.warning('CTRL+C was pressed, stopping')
    # prints a line with dashes
    @staticmethod
    def new_line():
        print '--------------------------------------------------------------------------------'