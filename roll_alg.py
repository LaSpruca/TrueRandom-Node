from odrv_wrapper import Odrive_Arm
import time
import random

print("Initialize")
arm = Odrive_Arm()
print("ODrive Booted")
def roll_dice():
    for i in range(10):
        x_direction = i%2==0
        x_pos = random.random()/2+0.5*x_direction
        pos = (x_pos,random.random(),random.random())
        arm.move_traj(pos)
    arm.move_traj((0.5,0.5,0.5))
    time.sleep(3)

