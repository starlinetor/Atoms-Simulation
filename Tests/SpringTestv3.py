from framerate_starlinetor.framerate import frame_handler
import tkinter as tk

class spring_simulation:
    
    def get_frame_handler(self,frame_handler : frame_handler):
        self.fh = frame_handler
    
    def move_pendulum(self,eventorigin):
        self.x = ((eventorigin.x + 25) / 500) -1
        self.y = ((eventorigin.y + 25) / 500) -1
        
    def start(self):
        return
        
    def loop(self):
        f_spring = -1 * self.k * self.x      #Hooke law
        f_friction = self.friction_k * self.vx * (1+abs(self.vx)) #friction
        f_total = f_spring + f_friction
        a = f_total/self.m             #Newton law
        self.vx += a * self.delta_t    #change in velocity is time times acceleration
        self.x += self.vx * self.delta_t    #change in position is time times speed
        
        f_spring = -1 * self.k * self.y      #Hooke law
        f_friction = self.friction_k * self.vy * (1+abs(self.vy)) #friction
        f_total = f_spring + f_friction
        a = f_total/self.m             #Newton law
        self.vy += a * self.delta_t    #change in velocity is time times acceleration
        self.y += self.vy * self.delta_t    #change in position is time times speed
        
    def end(self):
        #rendering
        #move the position of the mendulum
        self.c.moveto(self.pendulum,(1+self.x) * 500 -25,(1+self.y) * 500 -25)
        
        self.c.itemconfigure(self.fps_text, text=
                        f"{"{:.4f}".format(self.fh.average_fps())}"+
                        f"/{"{:.4f}".format(self.fh.average_spf())}"
                        )
        #update rendering
        self.root.update()
    
    def __init__(self):
        #simulation variables and starting conditions
        self.k : float = 1000           #N/m
        self.x : float = 0.5             #m
        self.y : float = 0             #m
        self.vx : float = 0               #m/s
        self.vy : float = 1               #m/s
        self.m : float = 1               #kg
        self.delta_t : float = 0.0001    #s
        self.friction_k : float = -10    #N/m^2
        
        #inizialization
        self.root = tk.Tk()
        self.c = tk.Canvas(self.root, bg="white",height=1000, width=1000)
        self.c.pack()
        self.root.attributes("-fullscreen", True)
        #on click map
        self.root.bind("<Button 1>",self.move_pendulum)
        #graphics
        self.pendulum = self.c.create_oval(0, 0, 50, 50,fill="Red")
        self.line1 = self.c.create_line(500,0,500,1000,fill="Black")
        self.line2 = self.c.create_line(250,0,250,1000,fill="Black")
        self.line3 = self.c.create_line(750,0,750,1000,fill="Black")
        self.fps_text = self.c.create_text(0,0,font=("FPS",25),text="Test",anchor="nw")

simulation : spring_simulation = spring_simulation()

fh = frame_handler(main_class=simulation, target_fps=60, executions_pf=167, fps_precision=30)

simulation.get_frame_handler(fh)

while True:
    fh.basic()