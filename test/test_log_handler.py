from utils.LogHandler import LogHandler


def test_log_handler():
    """
    test function LogHandler  in utils/LogHandler
    """
    log = LogHandler('test')
    log.info('this is a log from test')

    log.reset_name(name='test1')
    log.info('this is a log from test1')

    log.reset_name(name='test2')
    log.info('this is a log from test2')


if __name__ == '__main__':
    test_log_handler()
