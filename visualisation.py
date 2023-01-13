import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import json

#print(len('{ "TSS": "0000:00:05:54", "HV": 74, "BI":  0, "BV": 14, "PI":  0, "MI":  2, "DYN":   5, "DIS":  24, "BO": (102,  90) }'))


ser = serial.Serial('/dev/ttyUSB0', 115200)
print(ser.name)

fig, ax = plt.subplots(2, 2)

heart = []
breath = []
dynamic = []
distance = []
horizontal = []
vertical = []

time = [0]

cos_ = [np.cos(i) for i in range(0, 360, 5)]
sin_ = [np.sin(i) for i in range(0, 360, 5)]
sin_neg = [-v for v in sin_]


def animate(i, heart, breath, time, distance, dynamic, horizontal, vertical): 
    
    char_b = ser.readline()
    char = char_b.decode()
    p_char = char.replace("\r\n", "")
    print(p_char)

    p_char = p_char.replace(" ", "")
    response = json.loads(p_char)

    #heart = heart[-20:]
    #time = time[-20:]
    #breath = breath[-20:]
    #distance = distance[-20:]
    #dynamic = dynamic[-20:]
    #horizontal = horizontal[-20:]
    #vertical = vertical[-20:]

    heart.append(response["HV"])
    #time.append(response["TSS"])
    breath.append(response["BV"])
    distance.append(response["DIS"])
    dynamic.append(response["DYN"])

    h_angle = (response["BO"][0]-180)/360
    v_angle = (response["BO"][1]-180)/360


    horizontal.append(h_angle)
    vertical.append(v_angle)

    ax[0, 0].clear()
    ax[0, 0].set_ylim(-1, 110)
    ax[0, 0].set_xlabel("Seconds")
    ax[0, 0].set_title("Hearth and Breath")
    ax[0, 0].plot(time,heart, 'r', time, breath, 'b')

    ax[0, 1].clear()
    ax[0, 1].set_ylim(0, 105)
    ax[0, 1].set_xlabel("Seconds")
    ax[0, 1].set_title("Dynamic")
    ax[0, 1].plot(time, dynamic, "g")

    ax[1, 0].clear()
    ax[1, 0].set_ylim(0, 105)
    ax[1, 0].set_xlabel("Seconds")
    ax[1, 0].set_title("Distance (m)")
    ax[1, 0].plot(time, distance, "y")




    ax[1, 1].clear()
    ax[1, 1].set_ylim(-1.1, 1.1)
    ax[1, 1].set_xlim(-1.1, 1.1)
    
    ax[1, 1].set_title("Orientation")
    
    ax[1, 1].plot(cos_, sin_, "b+", horizontal, vertical, 'r+')
    
    time.append(time[-1] + 1) 



anim = animation.FuncAnimation(fig, animate, fargs=(heart, breath, time, distance, dynamic, horizontal, vertical))
plt.show()
anim.save("test")

