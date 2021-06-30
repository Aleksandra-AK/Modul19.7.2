
def log_wrapper(method):

    method()

    with open('log.txt', 'a') as log_file:
        log_file.write(f'headers: [arg1], path parametrs: [arg2]')
        log_file.write(f'string parametrs: [arg3], body: [arg4]######')
        log_file.write(f'######response: [arg5], response body: [arg6]\n')

