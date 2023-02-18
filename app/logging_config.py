import logging
# from systemd.journal import JournalHandler

def main() -> logging.Logger:
    log = logging.getLogger('scheduled_login_tradetron')
    log_fmt = logging.Formatter("%(levelname)s %(message)s")
    # log_ch = JournalHandler()
    log_ch = logging.FileHandler('log.log')
    log_ch.setFormatter(log_fmt)
    log.addHandler(log_ch)
    log.setLevel(logging.DEBUG)
    return log

if not hasattr(__spec__, 'log'):
    log = main()
