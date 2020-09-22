import os
import signal

def handler(signum, frame):
    raise Exception("timeout")

def probe_port(port):
    #print(str(port))
    stream = os.popen('wget -qO- portquiz.net:' + str(port))
    output = stream.read()
    #print(output)
    signal.setitimer(signal.ITIMER_REAL, 0)
    if output.find('successful') != 0:
        #print('success!')
        print(output.splitlines()[0])

def run_test():
    #port = 334
    port_start = 20
    port_stop = 1000
    timeout = 0.2
    for port in range(port_start, port_stop):
        signal.signal(signal.SIGALRM, handler)
        #signal.alarm(1)
        signal.setitimer(signal.ITIMER_REAL, timeout)

        try:
            probe_port(port)
        except Exception as exc:
            #print(exc)
            #print('Port ' + str(port) + ' is blocked.')
            continue

        #signal.alarm(0)
        #signal.setitimer(signal.ITIMER_REAL, 0)
        #signal.setitimer(0)

run_test()
#stream = os.popen('echo Retuned output')
#output = stream.read()
#print(output)
#
#
#stream = os.popen('wget -qO- portquiz.net')
#output = stream.read()
#print(output)