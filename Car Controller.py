#!/usr/bin/env python

#!/usr/bin/python
# -*- coding: utf-8 -*-
# move a servo from a Tk slider - scruss 2012-10-28
 
import pyfirmata
import tkinter as tk
import time

# don't forget to change the serial port to suit
board = pyfirmata.Arduino('COM3')
 
# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
 
# set up pin D9 as Servo Output
servopin = board.get_pin('d:9:s')
 
def move_servo(a):
    servopin.write(a)

# set up GUI
root = tk.Tk()

dir1 = 0
dir2 = 0
dir1pin = 7
pwm1pin = board.get_pin('d:6:p')
pwm2pin = board.get_pin('d:5:p')
dir2pin = 4

def reverse():
    global dir1
    global dir2
    print("dir1", dir1)
    if dir1 == 1:
        dir1 = 0
        board.digital[dir2pin].write(0)
    elif dir1 == 0:
        dir1 = 1
        board.digital[dir2pin].write(1)
    time.sleep(0.02)
    print("dir1", dir1)
    if dir2 == 1:
        dir2 = 0
        board.digital[dir1pin].write(0)
    elif dir2 == 0:
        dir2 = 1
        board.digital[dir1pin].write(1)
    time.sleep(0.02)
        
def speed(spd):
    val = int(spd) / 255
    print(val)
    pwm1pin.write(val)
    pwm2pin.write(val)
    time.sleep(0.02)
    
def stop():
    pwm1pin.write(0)
    pwm2pin.write(0)
    
revbtn = tk.Button(root, text = "Reverse", command = reverse)
stopbtn = tk.Button(root, text = "Stop", command = stop)

# draw a nice big slider for servo position
servo_scale = tk.Scale(root,
    command = move_servo,
    to = 175,
    orient = tk.HORIZONTAL,
    length = 400,
    label = 'Angle')
motor_scale = tk.Scale(root,
    command = speed,
    to = 255,
    orient = tk.HORIZONTAL,
    length = 400,
    label = 'Speed')
servo_scale.pack(anchor = tk.CENTER)
motor_scale.pack(anchor = tk.CENTER)
revbtn.pack()
stopbtn.pack()
root.mainloop()