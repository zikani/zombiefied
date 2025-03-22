import pygame
import random
import math
from config import *

class Particle:
    def __init__(self, x, y, color, particle_type="default"):
        self.x = x
        self.y = y
        self.color = color
        self.type = particle_type
        self.size = random.randint(2, 5)
        self.lifetime = random.randint(10, 20)
        self.alpha = 255
        self.max_lifetime = self.lifetime
        
        # Set particle behavior based on type
        if self.type == "explosion":
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-3, 3)
            self.decay_rate = 0.15
            self.size_decay = random.uniform(0.1, 0.2)
        elif self.type == "blood":
            self.vx = random.uniform(-1.5, 1.5)
            self.vy = random.uniform(-1.5, 1.5) + 0.5  # Blood falls down slightly
            self.decay_rate = 0.1
            self.size_decay = random.uniform(0.05, 0.1)
        elif self.type == "impact":
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.decay_rate = 0.2
            self.size_decay = random.uniform(0.1, 0.15)
        elif self.type == "sparkle":
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-0.5, 0.5) - 0.2  # Sparkles rise slightly
            self.decay_rate = 0.15
            self.size_decay = random.uniform(0.05, 0.1)
            self.pulsing = True
            self.pulse_rate = random.uniform(0.2, 0.4)
            self.pulse_offset = random.uniform(0, 2 * math.pi)
        else:  # default
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            self.decay_rate = 0.1
            self.size_decay = 0.1
            self.pulsing = False

    def update(self):
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Apply physics based on type
        if self.type == "blood":
            # Blood slows down due to friction
            self.vx *= 0.95
            self.vy *= 0.95
            # Blood is affected by gravity
            self.vy += 0.05
        elif self.type == "sparkle":
            # Sparkles slow down less
            self.vx *= 0.98
            self.vy *= 0.98
        elif self.type == "explosion":
            # Explosion particles slow down
            self.vx *= 0.9
            self.vy *= 0.9
        
        # Update appearance
        self.size = max(0, self.size - self.size_decay)
        self.lifetime -= 1
        
        # Update alpha for fading
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        # For pulsing particles, make them pulse
        if hasattr(self, 'pulsing') and self.pulsing:
            pulse_factor = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 100 * self.pulse_rate + self.pulse_offset)
            self.size *= pulse_factor

    def draw(self, screen, camera_x=0, camera_y=0):
        if self.lifetime > 0 and self.size > 0:
            # Create a surface with per-pixel alpha
            particle_surface = pygame.Surface((int(self.size * 2) + 1, int(self.size * 2) + 1), pygame.SRCALPHA)
            
            # Draw different shapes based on particle type
            if self.type == "sparkle":
                # For sparkles, draw a star-like shape
                color_with_alpha = (*self.color, self.alpha)
                center = (int(self.size) + 1, int(self.size) + 1)
                
                # Draw star shape
                points = []
                outer_radius = self.size
                inner_radius = self.size * 0.4
                for i in range(8):  # 8-pointed star
                    angle = i * math.pi / 4
                    if i % 2 == 0:
                        radius = outer_radius
                    else:
                        radius = inner_radius
                    x = center[0] + radius * math.cos(angle)
                    y = center[1] + radius * math.sin(angle)
                    points.append((x, y))
                
                pygame.draw.polygon(particle_surface, color_with_alpha, points)
            
            elif self.type == "blood":
                # For blood, draw irregular shapes
                color_with_alpha = (*self.color, self.alpha)
                pygame.draw.circle(particle_surface, color_with_alpha, 
                                  (int(self.size) + 1, int(self.size) + 1), int(self.size))
                
                # Add some splatter effect
                if self.size > 2:
                    for _ in range(2):
                        offset_x = random.uniform(-self.size/2, self.size/2)
                        offset_y = random.uniform(-self.size/2, self.size/2)
                        pygame.draw.circle(particle_surface, color_with_alpha,
                                          (int(self.size + offset_x) + 1, int(self.size + offset_y) + 1), 
                                           int(self.size / 2))
            
            else:
                # Standard circle for other particle types
                color_with_alpha = (*self.color, self.alpha)
                pygame.draw.circle(particle_surface, color_with_alpha, 
                                  (int(self.size) + 1, int(self.size) + 1), int(self.size))
            
            # Blit the particle surface
            screen.blit(particle_surface, 
                       (int(self.x - self.size - camera_x), 
                        int(self.y - self.size - camera_y)))


class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 500  # Limit to prevent performance issues

    def add_explosion(self, x, y, color=COLORS['red'], count=20):
        """Add explosion effect"""
        for _ in range(min(count, self.max_particles - len(self.particles))):
            self.particles.append(Particle(x, y, color, "explosion"))

    def add_blood_effect(self, x, y, count=15):
        """Add blood splatter effect"""
        for _ in range(min(count, self.max_particles - len(self.particles))):
            self.particles.append(Particle(x, y, COLORS['dark_red'], "blood"))
    
    def add_impact(self, x, y, color=COLORS['white'], count=10):
        """Add impact/collision effect"""
        for _ in range(min(count, self.max_particles - len(self.particles))):
            self.particles.append(Particle(x, y, color, "impact"))
    
    def add_sparkle(self, x, y, color=COLORS['gold'], count=5):
        """Add sparkle/powerup effect"""
        for _ in range(min(count, self.max_particles - len(self.particles))):
            self.particles.append(Particle(x, y, color, "sparkle"))

    def add_trail(self, x, y, color, trail_length=5):
        """Add trail effect (for fast movement)"""
        for i in range(trail_length):
            if len(self.particles) < self.max_particles:
                p = Particle(x, y, color)
                p.size = max(1, 3 - i * 0.5)  # Decreasing size
                p.vx = random.uniform(-0.5, 0.5)
                p.vy = random.uniform(-0.5, 0.5)
                p.lifetime = max(5, 10 - i * 2)  # Decreasing lifetime
                self.particles.append(p)

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0 or particle.size <= 0:
                self.particles.remove(particle)

    def draw(self, screen, camera_x=0, camera_y=0):
        for particle in self.particles:
            particle.draw(screen, camera_x, camera_y)
