import multiprocessing
import socket
from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
import time
from gpiozero import LED
from gpiozero import Buzzer
led=LED(5)
buzzer=Buzzer(26)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.IN)

# Set the GPIO pins for the sensor
TRIG_PIN = 24
ECHO_PIN = 17

# Set the GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def process1():
    print("Process 1 running on core:", multiprocessing.current_process()._identity[0])
    host = '192.168.11.209' # replace with your IPv4 address
    port = 12345 # choose a port number
    servo = AngularServo(18, min_pulse_width=0.0007, max_pulse_width=0.0020)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            servo.angle = 90
            while True:
                data = conn.recv(1024)
                if data:
                    print(data.decode("utf-8"))
                    a=data.decode("utf-8")
                    if (a=="close"):
                        servo.angle = 90
                    elif (a=="open"):
                        servo.angle = -90


def process2():
    print("Process 2 running on core:", multiprocessing.current_process()._identity[0])
    while True:
        inp=GPIO.input(20)
        if inp==1:
            print("Motion Detected")
            led.on()
            time.sleep(2)
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
            led.off()
        elif inp==0:
            #print("No Motion")
            #time.sleep(1)
            pass

def process3():
    print("Process 3 running on core:", multiprocessing.current_process()._identity[0])
    while True:
        # Set the trigger pin high for 10 microseconds
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        # Wait for the echo pin to go high
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        # Wait for the echo pin to go low
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        # Calculate the pulse duration and distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150

        # Round the distance to 2 decimal places and return it
        print("Distance {} cm".format(round(distance, 2)))
        sleep(1)


# create two processes
p1 = multiprocessing.Process(target=process1)
p2 = multiprocessing.Process(target=process2)
p3 = multiprocessing.Process(target=process3)

# start the processes
p1.start()
p2.start()
p3.start()

# wait for the processes to complete
#p1.join()
#p2.join()
#p3.join()