import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1280, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(space, window, draw_options, line = None):
    window.fill('white')        
    space.debug_draw(draw_options)

    if line: #line existis
        pygame.draw.line(window, 'black', line[1], line[0])

    pygame.display.update()

def create_boundaries(space, width, height):
    rects = [
        #primeira tupla define a posição do centro geométrico e a segundo, o tamanho
        [(width/2, height-10), (width, 20)], #floor
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0
        shape.friction = 0.5
        space.add(body, shape)

def create_inicial_position(space, width, height, altura):
    rects = [
        #primeira tupla define a posição do centro geométrico e a segundo, o tamanho
        [(width/8, height), (30, altura*2)], #floor
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 1
        shape.friction = 0.5
        space.add(body, shape)        


def create_ball(space, radius, mass, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    shape.elasticity = 0
    shape.friction = 0.5
    space.add(body, shape)
    return shape

def calculate_alcance(width, ball_x_position):
    return abs(width/8 - ball_x_position)


def run(window, widht, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0, 981)


    draw_options = pymunk.pygame_util.DrawOptions(window)
    click_count = 0
    ball = None
    line = None
    angle = 0
    module = 0
 
    create_boundaries(space, widht, height)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_count == 0:
                    altura = height - pygame.mouse.get_pos()[1]
                    create_inicial_position(space, widht, height, altura)
                    ball = create_ball(space, 20, 1, (widht/8, pygame.mouse.get_pos()[1]))
                    click_count += 1

                elif click_count == 1 and ball:
                    start_pos = (ball.body.position.x, ball.body.position.y)
                    end_pos = pygame.mouse.get_pos()
                    line = (start_pos, end_pos)

                    module = calculate_distance(line[1], line[0])
                    angle = calculate_angle(line[0], line[1])

                    click_count += 1

                elif click_count == 2 and ball:
                    # calculate the impulses (momento linear)
                    fx = math.cos(angle) * module * 2
                    fy = math.sin(angle) * module * 2

                    # calculate the velocity
                    vx = fx/ball.body.mass
                    vy = fy/ball.body.mass

                    ball.body.velocity = (vx, vy)

                    line = None
                    click_count += 1

        if ball and abs(ball.body.position.y - height) < 40:
            ball.body.velocity = (0, 0)
            

        draw(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    run(window, WIDTH, HEIGHT)
