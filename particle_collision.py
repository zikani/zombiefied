import pygame
import random
from config import *

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.lifetime = random.randint(10, 20)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.size = max(0, self.size - 0.1)
        self.lifetime -= 1

    def draw(self, screen, camera_x=0, camera_y=0):
        if self.lifetime > 0:
            pygame.draw.circle(
                screen, 
                self.color, 
                (int(self.x - camera_x), int(self.y - camera_y)), 
                int(self.size)
            )

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_explosion(self, x, y, color=COLORS['red'], count=20):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, screen, camera_x=0, camera_y=0):
        for particle in self.particles:
            particle.draw(screen, camera_x, camera_y)
