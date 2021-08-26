import pyglet
from pyglet import shapes
import math as m
import random
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(700,700)
box = shapes.BorderedRectangle(50, 50, 600,600,border = 1, color=(0, 0, 0),border_color=(255,0,100), batch=batch)
bodies = []
trails = []
t_s = .1 #speed of time passage
tail_length = 200;
class Body():
    def __init__(self, mass, radius, vel_x, vel_y,pos_x,pos_y):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mass = mass
        self.radius = radius
        self.F_x = 0
        self.F_y = 0
        self.trail_x = []
        self.trail_y = []
        self.circle = shapes.Circle(self.pos_x, self.pos_y, self.radius, color=(50, 225, 30), batch=batch)


def Calculate_Forces():

    for body in bodies:
        body.F_x = 0
        body.F_y = 0
        destroyed = []
        for other_body in bodies:
            if body == other_body:
                pass
            else:
                x = body.pos_x - other_body.pos_x
                y = body.pos_y - other_body.pos_y
                r = m.sqrt(x ** 2 + y ** 2)
                if r < body.radius + other_body.radius:
                    destroyed.append(other_body)
                try:
                    F = ((0.67 * 10 ** -11) * body.mass * other_body.mass) / r ** 2
                except:
                    F = 0
                if y > 0:
                    theta = m.atan(x / y)
                    Fy = -1 * m.cos(theta) * F
                    Fx = -1 * m.sin(theta) * F
                else:
                    try:
                        theta = m.atan(y / x)
                    except:
                        theta = 4.71238898038
                    if x < 0:
                        Fx = m.cos(theta) * F
                        Fy = m.sin(theta) * F
                    else:
                        Fx = -1 * m.cos(theta) * F
                        Fy = -1 * m.sin(theta) * F
                body.F_y += Fy
                body.F_x += Fx
        if len(destroyed) > 0:
            destroyed.append(body)
        for i in destroyed:
            bodies.remove(i)



def Update():
    for body in bodies:
        accel_x = body.F_x / body.mass
        accel_y = body.F_y / body.mass
        body.vel_x += accel_x * t_s
        body.vel_y += accel_y * t_s
        px = body.pos_x
        py = body.pos_y
        body.pos_x += body.vel_x * t_s
        body.pos_y += body.vel_y * t_s

        trails.append(pyglet.shapes.Line(px,py,body.pos_x,body.pos_y,width = 1,color = (255,255,255),batch=batch))
        if len(trails) > tail_length:
            trails.pop(0)
        body.circle.x = body.pos_x
        body.circle.y = body.pos_y
        

    batch.draw()
    

def update(dt):

    Calculate_Forces()
    Update()
    print(bodies[0].pos_y)

@window.event
def on_draw():
    window.clear()
    batch.draw()
#/////////////////////////////////////////////////////////

#formatting for creating a body......
#bodies.append(Body(mass, radius, X-Velocity, Y-Velocity ,X-Position, Y-Position
bodies.append(Body(10 * 10 ** 11,3,10,0,350,100))
bodies.append(Body(10 * 10 ** 12,3,0,10,0,350))
bodies.append(Body(10 * 10 ** 10,3,0,25,300,350))

bodies.append(Body(10 * 10 ** 11,3,8,0,300,0))
bodies.append(Body(10 * 10 ** 11,3,-2,10,0,0))
bodies.append(Body(10 * 10 ** 10,3,0,-25,500,350))

bodies.append(Body(10 * 10 ** 15,10,0,0,350,350))

#random generating bodies
for i in range(0):
    px = random.randint(0,700)
    py = random.randint(0,700)
    vx = random.randint(-1,1)
    vy = random.randint(-1,1)
    mas = random.randint(10 * 10 ** 12,10 * 10 ** 14)
    bodies.append(Body(10 * 10 ** 13,2,vx,vy,px,py))


pyglet.clock.schedule_interval(update, .001)
pyglet.app.run()





