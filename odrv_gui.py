import tkinter as tk
from odrv_wrapper import Odrive_Arm

arm = Odrive_Arm()
arm.move_traj((0.5,0.5,0.5))



window = tk.Tk()

X_label = tk.Label(text="X").pack()
X_input = tk.Entry(bg="grey", width=50)
X_input.pack()

Y_label = tk.Label(text="Y").pack()
Y_input = tk.Entry(bg="grey", width=50)
Y_input.pack()

Z_label = tk.Label(text="Z").pack()
Z_input = tk.Entry(bg="grey", width=50)
Z_input.pack()

def goto():
    try:
        arm.move_traj((float(X_input.get()),float(Y_input.get()),float(Z_input.get())))
    except AssertionError:
        print("move failed")

button = tk.Button(
    text="RUN!",
    width=25,
    height=5,
    fg="yellow",
    command=goto
).pack()



window.mainloop()
