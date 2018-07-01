from multiprocessing import Process
from schedule.ProxyRefreshSchedule import run as refresh_run
from schedule.ProxyValidateSchedule import ProxyValidSchedule


def run():
    process_list = list()
    validate_process = Process(target=ProxyValidSchedule.run, name='ValidRun')
    process_list.append(validate_process)

    refresh_process = Process(target=refresh_run, name='RefreshRun')
    process_list.append(refresh_process)

    for p in process_list:
        p.daemon = True
        p.start()

    for p in process_list:
        p.join()


if __name__ == '__main__':
    run()
