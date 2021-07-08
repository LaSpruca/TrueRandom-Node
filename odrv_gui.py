import tkinter as tk
from odrv_wrapper import Odrive_Arm
from odrive.utils import *

import time

arm = Odrive_Arm()
arm.move_blocking((0.5,0.5,0.5))

# start_liveplotter(lambda:[arm.odrv_X.axis0.encoder.pos_estimate, arm.odrv_X.axis0.controller.pos_setpoint])
start_liveplotter(lambda:[arm.odrv_X.axis0.motor.current_control.Iq_setpoint, arm.odrv_X.axis0.motor.current_control.Iq_measured])

window = tk.Tk()

X_label = tk.Label(text="X").pack()
X_input = tk.Entry(bg="grey", width=50)
X_input.insert(0,"0.5")
X_input.pack()

Y_label = tk.Label(text="Y").pack()
Y_input = tk.Entry(bg="grey", width=50)
Y_input.insert(0,"0.5")
Y_input.pack()

Z_label = tk.Label(text="Z").pack()
Z_input = tk.Entry(bg="grey", width=50)
Z_input.insert(0,"0.5")
Z_input.pack()

vel_integrator_gain_label = tk.Label(text="vel_integrator_gain").pack()
vel_integrator_gain_input = tk.Entry(bg="grey", width=50)
vel_integrator_gain_input.insert(0,arm.odrv_X.axis0.controller.config.vel_integrator_gain)
vel_integrator_gain_input.pack()

pos_gain_label = tk.Label(text="pos_gain").pack()
pos_gain_input = tk.Entry(bg="grey", width=50)
pos_gain_input.insert(0,arm.odrv_X.axis0.controller.config.pos_gain)

pos_gain_input.pack()

vel_gain_label = tk.Label(text="vel_gain").pack()
vel_gain_input = tk.Entry(bg="grey", width=50)
vel_gain_input.insert(0,arm.odrv_X.axis0.controller.config.vel_gain)
vel_gain_input.pack()


vel_limit_label = tk.Label(text="vel_limit").pack()
vel_limit_input = tk.Entry(bg="grey", width=50)
vel_limit_input.insert(0,arm.odrv_X.axis0.trap_traj.config.vel_limit)
vel_limit_input.pack()

accel_limit_label = tk.Label(text="accel_limit").pack()
accel_limit_input = tk.Entry(bg="grey", width=50)
accel_limit_input.insert(0,arm.odrv_X.axis0.trap_traj.config.accel_limit)
accel_limit_input.pack()

decel_limit_label = tk.Label(text="decel_limit").pack()
decel_limit_input = tk.Entry(bg="grey", width=50)
decel_limit_input.insert(0,arm.odrv_X.axis0.trap_traj.config.decel_limit)
decel_limit_input.pack()

# axis.trap_traj.config.vel_limit = 15
#         axis.trap_traj.config.accel_limit = 10
#         axis.trap_traj.config.decel_limit = 10

def get(input):
    return float(input.get())

def goto():
    try:
        arm.move_blocking((get(X_input),get(Y_input),get(Z_input)))
    except AssertionError:
        print("move failed")

def config():
    global arm
    arm.odrv_X.axis0.controller.config.pos_gain = get(pos_gain_input)
    arm.odrv_X.axis0.controller.config.vel_gain = get(vel_gain_input)
    arm.odrv_X.axis0.controller.config.vel_integrator_gain = get(vel_integrator_gain_input)
    arm.odrv_X.axis0.trap_traj.config.vel_limit = get(vel_limit_input)
    arm.odrv_X.axis0.trap_traj.config.accel_limit = get(accel_limit_input)
    arm.odrv_X.axis0.trap_traj.config.decel_limit = get(decel_limit_input)

button = tk.Button(
    text="RUN!",
    width=25,
    height=2,
    fg="yellow",
    command=goto
).pack()

button = tk.Button(
    text="Configure",
    width=25,
    height=5,
    fg="yellow",
    command=config
).pack()



window.mainloop()
