import logging
# from systemd.journal import JournalHandler

def main() -> logging.Logger:
    log = logging.getLogger('scheduled_login_tradetron')
    log_fmt = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    # log_ch = JournalHandler()
    log_ch = logging.FileHandler(filename = './scheduled_login_tradetron/logs/scheduled_login_tradetron.log', mode = 'w', encoding = 'utf8')
    log_ch.setFormatter(log_fmt)
    log.addHandler(log_ch)
    log.setLevel(logging.INFO)
    return log

if not hasattr(__spec__, 'log'):
    log = main()
