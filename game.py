import pygame
from random import randrange
from random import uniform

align_weight = 0.3
cohesion_weight = 0.3
separation_weight = 0.3

WIDTH,HEIGHT = 800,800

class Boid:
    def __init__(self,x,y):
        self.position = pygame.math.Vector2(x,y)
        self.velocity = pygame.math.Vector2(1,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.max_speed = 1
        self.max_force = 0.1
        self.size = 8

    def update(self):
        self.velocity += self.acceleration

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        
        self.position += self.velocity

        self.acceleration = pygame.math.Vector2(0,0) # Reset acceleration for next frame

        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        if self.position.y > HEIGHT:
            self.position.y = 0 
    
    def draw(self, screen):
        angle = self.velocity.angle_to(pygame.math.Vector2(1, 0))
        forward = pygame.math.Vector2(self.size, 0).rotate(-angle)
        left = pygame.math.Vector2(-self.size * 0.5, -self.size * 0.5).rotate(-angle)
        right = pygame.math.Vector2(-self.size * 0.5, self.size * 0.5).rotate(-angle)

        # Calculate triangle vertices
        p1 = self.position + forward
        p2 = self.position + left
        p3 = self.position + right

        pygame.draw.polygon(screen, (255, 255, 255), (p1,p2,p3))

    def apply_behavior(self, boids, cursor_position):
        local_radius = min(WIDTH,HEIGHT) * 0.05 # Defines the radius for local flockmates
        
        align_force = pygame.math.Vector2(0,0) # Boids steer towards the average direction other local flockmates are headed
        cohesion_force = pygame.math.Vector2(0,0) # Boids steer towards average position of a local flockmates
        separation_force = pygame.math.Vector2(0,0) # Boids steer to avoid crowding local flockmatgs

        total_neighbours=0 # keep track of the number of neighbours to see if we have a new force to apply

        for boid in boids:
            if boid == self:
                continue

            distance = self.position.distance_to(boid.position)

            if distance < local_radius: # We consider only local flockmates
                align_force += boid.velocity 
                cohesion_force += boid.position
                if distance > 0:
                    separation_force += (self.position - boid.position) / max(distance,10)
                total_neighbours +=1

        if total_neighbours > 0:
            align_force = (align_force / total_neighbours) -self.velocity    
            cohesion_force = (cohesion_force / total_neighbours) - self.position

        new_accel = (align_weight*align_force + cohesion_weight*cohesion_force + separation_weight * separation_force)

        if new_accel.length() > self.max_force:
            new_accel.scale_to_length(self.max_force)

        self.acceleration += (new_accel - self.acceleration)*0.1

        noise = pygame.math.Vector2(uniform(-0.1, 0.1), uniform(-0.1, 0.1))
        self.acceleration += noise

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Boid Flocking Simulation")

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    
    FPS = 60
    clock = pygame.time.Clock()

    # Initialize boids with random position
    boids = []
    NUMBEROFBOIDS = 100
    for boid in range(NUMBEROFBOIDS+1):
        position_x = randrange(0,100)* 0.01 * WIDTH
        position_y = randrange(0,100)* 0.01 * HEIGHT
        boids.append(Boid(position_x,position_y))

    running = True
    while running:
        screen.fill(BLACK)
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for boid in boids:
            boid.apply_behavior(boids, mouse_position)
            boid.update()
            boid.draw(screen)

        pygame.display.flip()
        


if __name__ == '__main__':
    main()

