import json
import math
import os
import signal
import threading
import time

def handler(signum, frame):
    raise Exception("timeout")

def probe_port(port, timeout):
    timeout = (math.ceil(timeout))
    #print('probe_port()')
    #print('wget --timeout ' + str(timeout) + ' -qO- portquiz.net:' + str(port))
    stream = os.popen('wget --timeout ' + str(timeout) + ' -qO- portquiz.net:' + str(port))
    output = stream.read()
    #print(output)
    signal.setitimer(signal.ITIMER_REAL, 0)
    if output.find('successful') != 0:
        #print('success!')
        print(output.splitlines()[0])
        return output.splitlines()[0]

def run_test(port_start, port_stop, timout):
    #port = 334
    #port_start = 20
    #port_stop = 1000
    #timeout = 0.2
    output = []
    counter = 0
    for port in range(port_start, port_stop):
        signal.signal(signal.SIGALRM, handler)
        #signal.alarm(1)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        counter += 1
        if counter%1 == 0:
            print(port_start + counter, end='\r')

        try:
            out = probe_port(port, timeout)
            output.append(out)
            time.sleep(timeout)
        except Exception as exc:
            #print(exc)
            #print('Port ' + str(port) + ' is blocked.')
            continue
            
        #time.sleep(2)
        #signal.alarm(0)
        #signal.setitimer(signal.ITIMER_REAL, 0)
        #signal.setitimer(0)
    print(output)
    #json_format = json.dumps(output)
    #print(json_format)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f)

if __name__ == "__main__":
    timeout = 0.5
    #timeout = 1.0
    port_start = 38800
    port_stop = 65536 

    #a = threading.Thread(target=run_test, args=(20, 50, timeout))
    #a.start()
    #a.join()

    #run_test(20, 50, timeout)
    run_test(port_start, port_stop, timeout)

#stream = os.popen('echo Retuned output')
#output = stream.read()
#print(output)
#
#
#stream = os.popen('wget -qO- portquiz.net')
#output = stream.read()
#print(output)
