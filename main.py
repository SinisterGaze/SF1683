import numpy as np
import pygame

pygame.init()

# Set up the drawing window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def map(value, from_range, to_range):
    old_w = from_range[1]-from_range[0]
    new_w = to_range[1]-to_range[0]

    return to_range[0] + (new_w/old_w)*(value-from_range[0])

def plotline(surface, limits, function, color = (0,0,255), width = 1):
    xlim = limits[:2]
    ylim = limits[2:4]

    xlen = xlim[1]-xlim[0]
    ylen = ylim[1]-ylim[0]

    x1 = xlim[0]
    y1 = function(x1)
    for i in range(WIDTH-1):
        x2 = xlim[0] + (i+1)*xlen/WIDTH 
        y2 = function(x2)
        
        start_pos = (map(x1, xlim, (0, WIDTH)), HEIGHT - map(y1, ylim, (0, HEIGHT)))
        end_pos = (map(x2, xlim, (0, WIDTH)), HEIGHT - map(y2, ylim, (0, HEIGHT)))

        pygame.draw.line(surface, color, start_pos, end_pos, width)

        x1 = x2
        y1 = y2

def h_intersect(x, m, b):
    return m*x+b

def v_intersect(y, m, b):
    return (y-b)/m

def draw_line(surface, limits, m, b, color = (255,0,0), width=1):
    
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

        start_pos = intersects[0]
        end_pos = intersects[1]

        start_pos = (map(start_pos[0], xlim, (0, WIDTH)), HEIGHT-map(start_pos[1], ylim, (0, HEIGHT)))
        end_pos = (map(end_pos[0], xlim, (0, WIDTH)), HEIGHT-map(end_pos[1], ylim, (0, HEIGHT)))

        pygame.draw.line(surface, color, start_pos, end_pos, width)

def draw_axislines(surface, limits, color = (255,255,255), width = 1):
    y_xaxis = map(0, limits[2:4], (HEIGHT, 0))
    x_yaxis = map(0, limits[:2], (0, WIDTH))
    pygame.draw.line(surface, color, (0, y_xaxis), (WIDTH, y_xaxis), width)
    pygame.draw.line(surface, color, (x_yaxis, 0), (x_yaxis, HEIGHT), width)


def random_color():
    color = np.random.randint(0, high = 256, size=3)
    return color

# Run until the user asks to quit
def main():

    done = False
    x_width = 5
    y_width = 5
    x_offset, y_offset = (0,0)

    clock = pygame.time.Clock()

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
                    x_width = 5
                    y_width = 5
                    x_offset, y_offset = (0,0)
                if event.key == pygame.K_ESCAPE:
                    done = True



        screen.fill((0,0,0))

        limits = (x_offset-x_width, x_offset + x_width, y_offset - y_width, y_offset + y_width)
        plotline(screen, limits, lambda t: np.exp(t/2) * (2 - 2*t/3), width = 2)
        draw_axislines(screen, limits)        
        

        pygame.display.flip()

   
    pygame.quit()

if __name__ == "__main__":
    main()
