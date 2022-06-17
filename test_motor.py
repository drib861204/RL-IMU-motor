import time

from torch import avg_pool1d
from rmdx8 import *
import matplotlib.pyplot as plt
from collections import deque
import os

Iq_cmd = 50

object = RmdX8()

Iq_feedback = np.int(0)
speed_feedback = np.int(0)

fig = plt.figure()
ax = plt.axes()
fig.suptitle(f"Iq {Iq_cmd}")

speed_buff = deque(maxlen=10)
avg_speed = 0

object.cmd_send("TORQUE", np.uint16(0))
time.sleep(2)

for _ in range(50):
    object.cmd_send("TORQUE", np.uint16(Iq_cmd))
    time.sleep(0.005)

    Iq_feedback = object.Iq_feedback
    speed_feedback = object.speed_feedback
    position_feedback = object.position_feedback
    if speed_feedback == 0:
        speed_feedback = avg_speed
    speed_buff.append(speed_feedback)
    avg_speed = np.mean(speed_buff)
    print(avg_speed)

    ax.plot(time.clock(), Iq_feedback, 'bo')
    ax.plot(time.clock(), speed_feedback, 'r*')
    #ax.plot(time.clock(), position_feedback, 'g*')
    ax.plot(time.clock(), avg_speed, 'b*')
    plt.draw()
    plt.pause(0.005)
    time.sleep(0.005)

fig_dir = "fig/"
if not os.path.exists(fig_dir):
    os.makedirs(fig_dir)
current_num_files = next(os.walk(fig_dir))[2]
run_num = len(current_num_files)
plt.savefig(f"{fig_dir}/fig{run_num}")

object.cmd_send("TORQUE", np.uint16(0))

#object.cmd_send("TORQUE", np.uint16(0))
#time.sleep(2)

#object.cmd_send("OFF", np.uint16(0))
#time.sleep(2)


'''
T=Fd
1Nm=3N*0.33m
10Nm=30N*0.33m
15Nm=45N*0.33m
20Nm=60N*0.33m

Iq      force
100     5.7
200     12.7
300     19.3
400     24
500     28
600     34
700     40
800     46
900     52
1000    58
1100    62
1200    63
1300    63

'''