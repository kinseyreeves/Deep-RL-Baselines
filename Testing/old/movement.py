import pyglet
from pyglet.gl import *
 
win = pyglet.window.Window()


def draw_square(x,y):
    
    #Setting Matrix Mode
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
     
    #moving object left and right
    glTranslatef(0.0, 0.0  , -0.0 ) #x,y,z,
    #rotating object
    glRotatef(rz, 0.0, 0.0, 1.0) #by 10 degrees around the x, y or z axis
     
    #colouration
    glColor3f(1.0, 1.0, 0.0)

    draw_square(500,100)
 
    #Draw rectangle
    glBegin( GL_QUADS )
    glVertex2f( x, y )
    glVertex2f( x+100, y )
    glVertex2f( x+100, y+100 )
    glVertex2f( x,  y+100 )
    glEnd()

@win.event
def on_draw():
    #SETUP
    glClearColor(0.5, 0.69, 1.0, 1)
 
    #SETSCENE
    glClear(GL_COLOR_BUFFER_BIT)
    draw_square(500,100)
 
    #Draw rectangle
    
 
 
def update(dt):
    global rz
    rz += dt * 10
    rz %= 360
 
rz = 0
pyglet.clock.schedule(update)
pyglet.app.run()
