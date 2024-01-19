import pygame
import math

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

class Snake:
    def __init__(self):
        self.segments = [GameObject(50, 50, 20, 20, (0, 128, 0))]
        self.direction = (5, 0)

    def move(self, dx, dy):
        new_head = self.segments[0].rect.move(dx, dy)

        # Border collision check
        if new_head.left < 0 or new_head.right > 500 or new_head.top < 0 or new_head.bottom > 500:
            return

        self.segments = [GameObject(new_head.x, new_head.y, 20, 20, (0, 128, 0))] + self.segments[:-1]

    def grow(self):
        self.segments.append(self.segments[-1])

    def draw(self, window, draw_features=False):
        for segment in self.segments:
            segment.draw(window)

        # Optionally add eyes and tongue to the head segment
        if draw_features:
            head = self.segments[0]
            eye1_pos = (head.rect.centerx - 5, head.rect.centery - 5)
            eye2_pos = (head.rect.centerx + 5, head.rect.centery - 5)
            tongue_pos1 = (head.rect.centerx - 2, head.rect.centery + 8)
            tongue_pos2 = (head.rect.centerx + 2, head.rect.centery + 8)

            pygame.draw.circle(window, (255, 255, 255), eye1_pos, 2)
            pygame.draw.circle(window, (255, 255, 255), eye2_pos, 2)
            pygame.draw.line(window, (255, 0, 0), tongue_pos1, tongue_pos2, 2)


class Food(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10, (255, 0, 0))


class PowerUp(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10, (0, 255, 255))  # Added the color argument

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)



# Predator class
class Predator(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (0, 0, 255))
        self.chomp = False

    def move_towards(self, target):
        dx, dy = 0, 0
        if self.rect.centerx < target.rect.centerx:
            dx = 2
        elif self.rect.centerx > target.rect.centerx:
            dx = -2

        if self.rect.centery < target.rect.centery:
            dy = 2
        elif self.rect.centery > target.rect.centery:
            dy = -2

        # Border collision check
        new_position = self.rect.move(dx, dy)
        if new_position.left >= 0 and new_position.right <= 500 and new_position.top >= 0 and new_position.bottom <= 500:
            self.rect = new_position


    def draw(self, window, target):
        pygame.draw.circle(window, self.color, (self.rect.centerx, self.rect.centery), 10)
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)
        
        if self.chomp:
            mouth_x1 = self.rect.centerx + 10 * math.cos(angle + 0.4)
            mouth_y1 = self.rect.centery + 10 * math.sin(angle + 0.4)
            mouth_x2 = self.rect.centerx + 10 * math.cos(angle - 0.4)
            mouth_y2 = self.rect.centery + 10 * math.sin(angle - 0.4)

            pygame.draw.polygon(window, (0, 0, 0), [
                (self.rect.centerx, self.rect.centery),
                (mouth_x1, mouth_y1),
                (mouth_x2, mouth_y2)
            ])
        self.chomp = not self.chomp




