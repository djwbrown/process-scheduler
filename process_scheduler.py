import threading
import time
import os

interval_A = 4
interval_B = 7
interval_C = 11

runtime_A = 2.0
runtime_B = 4.0
runtime_C = 7.0

# Create a threading module Event object for the heartbeat pulse and run flags.
pulse = threading.Event()
run_A = threading.Event()
run_B = threading.Event()
run_C = threading.Event()

# Subclass threading module Thread object for each Process A, B, and C.
class Process_A(threading.Thread):
    def run(self):
        while True:
            run_A.wait()
            time.sleep(runtime_A)
            run_A.clear()

class Process_B(threading.Thread):
    def run(self):
        while True:
            run_B.wait()
            time.sleep(runtime_B)
            run_B.clear()

class Process_C(threading.Thread):
    def run(self):
        while True:
            run_C.wait()
            time.sleep(runtime_C)
            run_C.clear()

# Create a 'server' thread, that generates a heartbeat pulse lasting 0.1s every 1s.
class Pulse_Generator(threading.Thread):
    def run(self):
        while True:
            pulse.set()
            time.sleep(0.1)
            pulse.clear()
            time.sleep(0.9)

# Create a 'client' thread for each process, that listens for pulses, counts them, and triggers each process.
class Client_A(threading.Thread):
    def run(self):
        while True:
            count = 0
            pulse.wait()
            run_A.set()
            time.sleep(0.4)
            while count < interval_A - 1:
                pulse.wait() # Event.wait() is not edge triggered, but will continue to return True until pulse is reset.
                time.sleep(0.4) # These time.sleep() calls give the heartbeat pulse a chance to reset its flag.
                count += 1

class Client_B(threading.Thread):
    def run(self):
        while True:
            count = 0
            pulse.wait()
            run_B.set()
            time.sleep(0.4)
            while count < interval_B - 1:
                pulse.wait()
                time.sleep(0.4)
                count += 1

class Client_C(threading.Thread):
    def run(self):
        while True:          
            count = 0
            pulse.wait()
            run_C.set()
            time.sleep(0.4)
            while count < interval_C - 1:
                pulse.wait()
                time.sleep(0.4)
                count += 1

# Instatitate one of each of these Thread subclasses.
client_A = Client_A()
client_B = Client_B()
client_C = Client_C()
process_A = Process_A()
process_B = Process_B()
process_C = Process_C()
pulse_generator = Pulse_Generator()

# Start each client, the 'ready' processes, and then the pulse generator server.
client_A.start()
client_B.start()
client_C.start()
process_A.start()
process_B.start()
process_C.start()
pulse_generator.start()

# Print the output indicating a running process.
def output_running_processes(second_index):
    status_A = " "
    status_B = " "
    status_C = " "

    if run_A.is_set(): status_A = "A"
    if run_B.is_set(): status_B = "B"
    if run_C.is_set(): status_C = "C"

    print "{:2}s: {} {} {}".format(second_index, status_A, status_B, status_C)

# Print the status of each process on a 1s interval.
print "\nThe following 'processes' (really threads) are now running..."

try:
    for i in xrange(0,22):
        time.sleep(0.1)
        output_running_processes(i)
        time.sleep(0.4)
        pulse.wait()
    os._exit(0)

# This catches a KeyboardInterrupt exception and exits all threads.
except KeyboardInterrupt:
    os._exit(-1)
