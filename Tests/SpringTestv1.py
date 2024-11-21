import time
import tkinter as tk

from numpy import average

#simulation variables and starting conditions

k : float = 10000           #N/m
x : float = 0.5             #m
v : float = 0               #m/s
m : float = 1               #kg
delta_t : float = 0.0001    #s
friction_k : float = -10    #N/m^2

#rendering
target_fps : int = 240
step_pf : int = int((1/target_fps) / delta_t)   #simulation steps per frame
start_time : float = 0                          #start time of simulation step
end_time : float = 0                            #end time of a simulation step
spf : float = 1                                 #seconds per frame
average_precision : int = 60
spf_avrage : list[float] = [(1/target_fps) for _ in range(average_precision)]
usage_percentage_avrage : list[float] = [50 for _ in range(average_precision)]

#debug options
debug_active : bool = False
def debug():
    global f_total, f_spring, f_friction
    print(f"Total : {f_total}, Spring : {f_spring}, Friction : {f_friction}")

#tkinter
#on click function
def move_pendulum(eventorigin):
    global x
    x = ((eventorigin.x + 25) / 500) -1
#inizialization
root = tk.Tk()
c = tk.Canvas(root, bg="white",height=400, width=1000)
c.pack()
#on click map
root.bind("<Button 1>",move_pendulum)
#graphics
pendulum = c.create_oval(0, 0, 50, 50,fill="Red")
line1 = c.create_line(500,0,500,400,fill="Black")
line1 = c.create_line(250,0,250,400,fill="Black")
line1 = c.create_line(750,0,750,400,fill="Black")
fps_text = c.create_text(0,0,font=("FPS",25),text="Test",anchor="nw")


while True: 
    
    #update frame rate
    if(end_time-start_time != 0):
        spf = end_time-start_time
    spf_avrage.pop(0)
    spf_avrage.append(spf)
    
    #saves starting time
    start_time = time.time_ns() / (10 ** 9)
    
    #renders a frame only every {step_pf} times
    for i in range(step_pf):
        f_spring = -1 * k * x      #Hooke law
        f_friction = friction_k * v * (1+abs(v)) #friction
        f_total = f_spring + f_friction
        a = f_total/m             #Newton law
        v += a * delta_t    #change in velocity is time times acceleration
        x += v * delta_t    #change in position is time times speed

    #debug information
    if(debug_active):
        debug()

    #rendering
    #move the position of the mendulum
    c.moveto(pendulum,(1+x) * 500 -25,200)
    #update fps
    usage_percentage_avrage.pop(0)
    usage_percentage_avrage.append(spf*target_fps*100)
    c.itemconfigure(fps_text, text=
                    f"{"{:.4f}".format(1/target_fps)}"+
                    f"/{"{:.4f}".format(sum(spf_avrage)/average_precision)}"+
                    f": {"{:.0f}".format(sum(usage_percentage_avrage)/average_precision)}%"
                    )
    #update rendering
    root.update()
    
    #saves ending time of the frame
    end_time  = time.time_ns() / (10 ** 9)
    
    #leftover time is spent sleeping
    if((1/target_fps) - end_time + start_time >=  0) :
        time.sleep((1/target_fps) - end_time + start_time)
    
