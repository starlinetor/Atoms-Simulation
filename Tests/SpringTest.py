import math
import time
import tkinter as tk
from tracemalloc import start

#starting conditions

k : float = 100            #N/m
x : float = 0.5             #m
v : float = 0               #m/s
m : float = 1               #kg
delta_t : float = 0.0001    #s
friction_k : float = -1     #N/m^2

#rendering
target_fps : int = 240
step_pf : int = int((1/target_fps) / delta_t)   #simulation steps per frame
start_time : float = 0                          #start time of simulation step
end_time : float = 0                            #end time of a simulation step
spf : float = 1                                 #seconds per frame

#tkinter
def move_pendulum(eventorigin):
    global x
    x = ((eventorigin.x + 25) / 500) -1

root = tk.Tk()
c = tk.Canvas(root, bg="white",height=400, width=1000)
c.pack()
root.bind("<Button 1>",move_pendulum)

pendulum = c.create_oval(0, 0, 50, 50,fill="Red")
line1 = c.create_line(500,0,500,400,fill="Black")
line1 = c.create_line(250,0,250,400,fill="Black")
line1 = c.create_line(750,0,750,400,fill="Black")
fps_text = c.create_text(0,0,font=("FPS",25),text="Test",anchor="nw")


while True: 
    #renders a frame only every {step_pf} times
    
    start_time = time.time_ns() / (10 ** 9)
    
    for i in range(step_pf):
        f_spring = -1 * k * x      #Hooke law
        f_friction = friction_k * v * (1+abs(v)) 
        f_total = f_spring + f_friction
        a = f_total/m             #Newton law
        v += a * delta_t    #change in velocity is time times acceleration
        x += v * delta_t    #change in position is time times speed
    
    end_time  = time.time_ns() / (10 ** 9)
    
    if((1/target_fps) - end_time + start_time >=  0) :
        time.sleep((1/target_fps) - end_time + start_time)
    
    if(end_time-start_time != 0):
        spf = round(end_time-start_time , 3)
    
    c.itemconfigure(fps_text, text=f"{round(1/target_fps,3)}/{spf} : {spf*target_fps}%")
        
    print(f"Total : {f_total}, Spring : {f_spring}, Friction : {f_friction}")
    c.moveto(pendulum,(1+x) * 500 -25,200)
    root.update()