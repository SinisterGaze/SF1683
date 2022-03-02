import numpy as np
import pygame

pygame.init()

# Set up the drawing window
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def map(value, from_range, to_range):
    old_w = from_range[1]-from_range[0]
    new_w = to_range[1]-to_range[0]
    try:
        return to_range[0] + (new_w/old_w)*(value-from_range[0])
    except ZeroDivisionError:
        return to_range[0]

def plotf(surface, limits, function, color=(0, 0, 255), width=1):
    xlim = limits[:2]
    ylim = limits[2:4]

    xlen = xlim[1]-xlim[0]
    ylen = ylim[1]-ylim[0]

    x1 = xlim[0]
    y1 = function(x1)
    for i in range(WIDTH-1):
        x2 = xlim[0] + (i+1)*xlen/WIDTH

        try:
            y2 = function(x2)
        except ZeroDivisionError:
            continue

        start_pos = (map(x1, xlim, (0, WIDTH)),
                     HEIGHT - map(y1, ylim, (0, HEIGHT)))
        end_pos = (map(x2, xlim, (0, WIDTH)),
                   HEIGHT - map(y2, ylim, (0, HEIGHT)))

        pygame.draw.line(surface, color, start_pos, end_pos, width)

        x1 = x2
        y1 = y2

def plotfimplicit(surface, limits, function, color=(0, 0, 255), width=1):
    xlim = limits[:2]
    ylim = limits[2:4]

    prevx = xlim[0]-1
    prevy = ylim[0]-1

    for scr_x in range(WIDTH):
        for scr_y in range(HEIGHT):
            x = map(scr_x, (0, WIDTH), xlim)
            y = map(scr_y, (HEIGHT, 0), ylim)

            if abs(function(x,y)) < 1e-2:
                if prevx>=xlim[0] and prevy >= ylim[0]:
                    start_pos = (scr_x, scr_y)
                    end_pos = (map(prevx, xlim, (0, WIDTH)), HEIGHT - map(prevy, ylim, (0, HEIGHT)))
                    pygame.draw.line(screen, color, start_pos, end_pos, width = width)

            prevx = x
            prevy = y

def h_intersect(x, m, b):
    return m*x+b


def v_intersect(y, m, b):
    return (y-b)/m


def line(surface, limits, m, b, color=(255, 0, 0), width=1):

    xlim = limits[0:2]
    ylim = limits[2:4]

    if m == 0:
        if ylim[0] <= b <= ylim[1]:
            y = map(b, ylim,  HEIGHT-(0, HEIGHT))
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    else:

        intersects = []

        if ylim[0] <= h_intersect(xlim[0], m, b) <= ylim[1]:
            intersects.append((xlim[0], h_intersect(xlim[0], m, b)))

        if ylim[0] <= h_intersect(xlim[1], m, b) <= ylim[1]:
            intersects.append((xlim[1], h_intersect(xlim[1], m, b)))

        if xlim[0] <= v_intersect(ylim[0], m, b) <= xlim[1]:
            intersects.append((v_intersect(ylim[0], m, b), ylim[0]))

        if xlim[0] <= v_intersect(ylim[1], m, b) <= xlim[1]:
            intersects.append((v_intersect(ylim[1], m, b), ylim[1]))

        if len(intersects) >= 2:
            start_pos = intersects[0]
            end_pos = intersects[1]

            start_pos = (map(start_pos[0], xlim, (0, WIDTH)),
                         HEIGHT-map(start_pos[1], ylim, (0, HEIGHT)))
            end_pos = (map(end_pos[0], xlim, (0, WIDTH)),
                       HEIGHT-map(end_pos[1], ylim, (0, HEIGHT)))

            pygame.draw.line(surface, color, start_pos, end_pos, width)


def vline(surface, x, limits,  color=(255, 0, 0), width=1):
    xlim = limits[:2]
    ylim = limits[2:4]
    start_pos = (map(x, xlim, (0, WIDTH)), 0)
    end_pos = (map(x, xlim, (0, WIDTH)), HEIGHT)
    pygame.draw.line(surface, color, start_pos, end_pos, width)


def hline(surface, y, limits,  color=(255, 0, 0), width=1):
    xlim = limits[:2]
    ylim = limits[2:4]
    start_pos = (0, HEIGHT-map(y, ylim, (0, HEIGHT)))
    end_pos = (WIDTH, HEIGHT-map(y, ylim, (0, HEIGHT)))
    pygame.draw.line(surface, color, start_pos, end_pos, width)


def draw_axislines(surface, limits, color=(255, 255, 255), width=1):
    hline(screen, 0, limits, color, width)
    vline(screen, 0, limits, color, width)


def random_color():
    color = np.random.randint(0, high=256, size=3)
    return color

def dir_field(surface, limits, function, size = 10, n = 30, color = (255,255,255), heatmap = False, scale = False):
    xlim = limits[:2]
    ylim = limits[2:4]
    scl_x = WIDTH/n
    scl_y = HEIGHT/n

    size_range = (size/3, size*3)

    valrange = [np.inf, np.NINF]
    abs_valrange = [np.inf, 0]

    if heatmap or scale:
        for i in range(n):
            for j in range(n):
                scr_x = scl_x*(i+0.5)
                scr_y = scl_y*(j+0.5)

                x = map(scr_x, (0, WIDTH), xlim)
                y = map(HEIGHT - scr_y, (0, HEIGHT), ylim)

                ydot = function(x,y)
                absydot = abs(ydot)

                valrange[0] = ydot if ydot < valrange[0] else valrange[0]
                valrange[1] = ydot if ydot > valrange[1] else valrange[1]

                abs_valrange[0] = absydot if absydot < abs_valrange[0] else abs_valrange[0]
                abs_valrange[1] = absydot if absydot > abs_valrange[1] else abs_valrange[1]

    for i in range(n):
        for j in range(n):
            scr_x = scl_x*(i+0.5)
            scr_y = scl_y*(j+0.5)

            x = map(scr_x, (0,WIDTH), xlim)
            y = map(HEIGHT - scr_y, (0, HEIGHT), ylim)

            ydot = function(x,y)
            den = 1/np.sqrt(1+ydot*ydot)

            if scale:
                size = map(abs(ydot), abs_valrange, size_range)

            dx = size*den
            dy = dx*ydot

            start_pos = (scr_x, scr_y)
            end_pos = (scr_x + dx, scr_y - dy)

            c = color

            if heatmap:
                if abs(valrange[1]-valrange[0]) > 0:
                    c = map(ydot, valrange, (0,1))
                    color = (255*c, 0, 255 * (1-c))


            pygame.draw.line(surface, color, start_pos, end_pos, width = 1)

def plotint(surface, int_lim, limits, function, color=(0,255,0)):

    a, b = int_lim

    xlim = limits[:2]
    ylim = limits[2:4]

    x = map(0, (0, WIDTH), xlim)
    try:
        y = function(x)
    except ZeroDivisionError:
        y = 0

    a = max(int(np.floor(map(a, xlim, (0, WIDTH)))), 0)
    b = min(int(np.ceil(map(b, xlim, (0, WIDTH)))), WIDTH)
    for i in range(a,b):
        x = map(i, (0, WIDTH), xlim)
        try:
            y = function(x)
        except ZeroDivisionError:
            y = y

        start_pos = (i,
                     HEIGHT - map(0, ylim, (0, HEIGHT)))
        end_pos = (i,
                   HEIGHT - map(y, ylim, (0, HEIGHT)))

        pygame.draw.line(surface, color, start_pos, end_pos, width = 1)



def main():

    def v_coeff(k, t):
        kp = k * np.pi
        factor = 2 * (-1) ** k 
        result = (1/kp + 1/(kp**2-1)) * np.exp(-t*kp**2) + (1/(1-kp**2))*np.exp(-t)
        return factor*result 
        
    def v(x, t, N):
        result = 0
        for k in range(1,N+1):
            result += v_coeff(k, t) * np.sin(k*np.pi*x)
        return result
    
    def u(x,t, N):
        return v(x, t, N) + x*np.exp(-t)

    def f(x,t):
        c = 1
        if (np.abs(x-c*t) <= np.pi/2):
            return 0.5*np.power(np.cos(x-c*t), 2)
        else:
            return 0

    def fsps(x,t):
        c = 1
        return f(x,t) + f(x,-t)

    def ydot(x,y):
        try:
            r = 5
            if x**2 + (y-r)**2 <= r**2:
                return np.sqrt(x**2 + y**2)*(-x/y)
            else:
                return 0
        except ZeroDivisionError:
            return 0


    x_width = 1
    y_width = 1
    x_offset, y_offset = (0, 0)
    startvalues = (x_width, y_width, x_offset, y_offset)

    done = False
    clock = pygame.time.Clock()
    
    t = 0
    while not done:

        dt = clock.tick(144)

        keys = pygame.key.get_pressed()
        if keys[43]:
            x_width -= 0.003*dt*x_width
            y_width -= 0.003*dt*y_width
        if keys[45]:
            x_width += 0.003*dt*x_width
            y_width += 0.003*dt*y_width
        if keys[pygame.K_w]:
            y_offset += 0.004*dt*y_width
        if keys[pygame.K_s]:
            y_offset -= 0.004*dt*y_width
        if keys[pygame.K_d]:
            x_offset += 0.004*dt*x_width
        if keys[pygame.K_a]:
            x_offset -= 0.004*dt*x_width

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    x_width, y_width, x_offset, y_offset = startvalues
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((0,0,0))

        limits = (x_offset-x_width, x_offset + x_width,
                  y_offset - y_width, y_offset + y_width)
    
        t = t + 0.0001*dt
        # Endimensionell värmeledning (Fourierserie)
        plotf(screen, limits, lambda x:u(x,t,3),color = (255,0,0), width = 2)
        #plotf(screen, limits, lambda x:u(x,t,10),color = (255,0,0), width = 2)
        #plotint(screen, (0,1), limits, lambda x:np.abs(u(x,t,4)-u(x,t,10)))
        #plotf(screen, limits, lambda x:u(x,t), width = 2)
        
        #Vågkollision
        #plotf(screen, limits, lambda x:f(x,t), color = (100,100,255))
        #plotf(screen, limits, lambda x:f(x,-t), color = (100,100,255))
        #plotf(screen, limits, lambda x:fsps(x,t/5))
        draw_axislines(screen, limits)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
