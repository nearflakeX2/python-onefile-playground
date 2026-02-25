import tkinter as tk
import random, math

W,H=900,560
N=220

class App:
    def __init__(self,root):
        self.c=tk.Canvas(root,width=W,height=H,bg='#090d18',highlightthickness=0);self.c.pack()
        self.t=0
        self.p=[(random.random()*6.28, random.uniform(40,250), random.uniform(0.004,0.02), random.uniform(1.2,3.2)) for _ in range(N)]
        root.bind('<Escape>',lambda e:root.destroy())
        root.bind('<space>',lambda e:self.reset())
        self.loop()
    def col(self,i):
        a=(math.sin(self.t*2+i*0.1)+1)/2
        b=(math.sin(self.t*3+i*0.13+2)+1)/2
        r=int(80+175*a); g=int(80+175*b); bl=255
        return f'#{r:02x}{g:02x}{bl:02x}'
    def reset(self):
        self.t=0
    def loop(self):
        self.t += 0.02
        self.c.create_rectangle(0,0,W,H,fill='#090d18',outline='',stipple='gray75')
        cx,cy=W//2,H//2
        for i,(ang,r,s,sz) in enumerate(self.p):
            ang += s*(1+0.4*math.sin(self.t+i*0.01))
            x=cx+math.cos(ang)*(r+22*math.sin(self.t+i*0.2))
            y=cy+math.sin(ang*1.08)*(r+22*math.cos(self.t+i*0.15))
            self.p[i]=(ang,r,s,sz)
            self.c.create_oval(x-sz,y-sz,x+sz,y+sz,fill=self.col(i),outline='')
        self.c.create_text(10,10,anchor='nw',fill='#9ec8ff',text='Neon Orbit • ESC quit • SPACE reset',font=('Segoe UI',11,'bold'))
        self.c.after(16,self.loop)

root=tk.Tk(); root.title('Neon Orbit'); App(root); root.mainloop()
