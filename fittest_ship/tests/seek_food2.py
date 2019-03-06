import pygame as pg
from pygame.math import Vector2 as vec
from random import randint, uniform


class Vehicle(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()  # init pg.sprite.Sprite
        self.size = size
        self.image = pg.Surface((self.size, self.size//2), pg.SRCALPHA)
        self.poly_coords = [
            (0, 0), (self.size, self.size//4), (0, self.size // 2)]
        pg.draw.polygon(self.image, pg.Color('green'),
                        self.poly_coords)
        self.orig_image = self.image  # Store a reference to the original.
        self.rect = self.image.get_rect(center=pos)

        self.position = pos

        # define vel and max vel, as we are using dt(delta time) it's pixels per second
        self.velocity = vec(0.0, 0.0)
        # self.max_velocity = 120  # trying below to randomize points between max health and max velocity
        # to increase vel each frame
        self.acceleration = vec(0.0, 0.0)

        ## TESTING ##
        total_points = 220
        self.max_velocity = randint(50, total_points - 50)
        self.max_health = total_points - self.max_velocity

        # max steer force
        self.max_steer_force = uniform(1, 3)  # 1.5

        # health of the vehicle
        # self.max_health = 100
        self.health = self.max_health

        # color, which will represent health status too
        self.color = (0, 255, 0)

        # distance at which the vehicle can see food
        self.food_distance = randint(10, 300)
        self.poison_distance = randint(10, 300)

        # attraction to food and poison
        self.food_attraction = uniform(-10, 10)
        self.poison_attraction = uniform(-10, 10)

        # last time a target was adquired in milliseconds
        self.last_target_time = 0
        self.wander_ring_distance = randint(10, 100)  # 50
        self.wander_ring_radius = randint(50, 300)  # 200
        self.wander_ring_wait = randint(500, 4000)
        self.wander_ring_pos = self.position
        self.wander_target = self.position

        # time alive in seconds
        self.age = 0.0

    def change_color_by_health(self):
        # using abs to avoid crashing due to negative colour, anyway the vehicle is going to die
        green = int(abs(self.health) * 255 / self.max_health)
        red = int(255 - green)
        self.color = (red, green, 0)

    def seek(self, target):
        # calculate the desired vector:
        self.desired = (target - self.position).normalize() * self.max_velocity
        # the steer force:
        steer = (self.desired - self.velocity)
        if steer.length() > self.max_steer_force:
            steer.scale_to_length(self.max_steer_force)

        # return the steer force
        return steer

    def seek2(self, target):
        # calculate the desired vector:
        desired = (target - self.position).normalize() * self.max_velocity
        # the steer force:
        steer = (desired - self.velocity)
        if steer.length() > self.max_steer_force:
            steer.scale_to_length(self.max_steer_force)

        # return the steer force
        return steer

    def wander(self):
        now = pg.time.get_ticks()
        if now - self.last_target_time > 500:
            self.last_target_time = now
            target = vec((randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT)))
        return self.seek(target)

    def wander_ring(self):
        now = pg.time.get_ticks()
        if now - self.last_target_time > self.wander_ring_wait:
            self.last_target_time = now

            # this randomizes the waittime a bit more
            # self.wander_ring_wait = randint(500, 4000)

            new_pos = vec((randint(int(-WIN_WIDTH), int(WIN_WIDTH)),
                           randint(int(-WIN_WIDTH), int(WIN_HEIGHT))))
            if self.velocity.length():
                self.wander_ring_pos = new_pos + self.velocity.normalize() * \
                    self.wander_ring_distance
            else:
                self.wander_ring_pos = new_pos * self.wander_ring_distance

        target = self.wander_ring_pos + \
            vec(self.wander_ring_radius, 0).rotate(uniform(0, 360))
        self.wander_target = target  # only for drawing its vector

        return self.seek(target)

    def search_food(self, foods, poisons):
        targets = {}

        for food in foods:
            food_distance = (self.position - food.position).length()
            if food_distance < self.food_distance:
                targets[food] = food_distance

        for poison in poisons:
            poison_distance = (self.position - poison.position).length()
            if poison_distance < self.poison_distance:
                targets[poison] = poison_distance

        steer = None
        if len(targets):
            for fp, dist in targets.items():
                steer_force = (self.seek2(fp.position).normalize())

                if fp.poison:
                    steer_force *= self.poison_attraction
                else:
                    steer_force *= self.food_attraction

                if dist:
                    steer_force = steer_force / dist

                if steer is None:
                    steer = steer_force
                else:
                    steer += steer_force

            steer *= self.max_velocity
            self.desired = steer + self.velocity
            if steer.length() > self.max_steer_force:
                steer.scale_to_length(self.max_steer_force)

            self.acceleration = steer
        else:
            self.acceleration = self.wander_ring()

    def update(self, dt):
        # self.acceleration = self.flee_with_approach(pg.mouse.get_pos())
        # self.acceleration = self.seek_with_approach(pg.mouse.get_pos())

        self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)

        # update position according to velocity, pixels/second
        self.position += self.velocity * dt
        # update rect center to correctly draw on screen
        self.rect.center = self.position

        # we slowly lose health
        self.health -= 0.15
        if self.health < 0:
            self.kill()

        # rotate according to angle
        self.rotate()

        # calculate how much time in seconds the vehicle has been alive
        self.age += dt

    def rotate(self):
        # change color according to current health
        self.change_color_by_health()
        # change original image color
        pg.draw.polygon(self.orig_image, self.color,
                        self.poly_coords)
        # The vector to the target (the mouse position).
        direction = self.velocity
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        _, angle = direction.as_polar()
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pg.transform.rotate(self.orig_image, -angle)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw_vectors(self, screen, opt1=False, opt2=False, opt3=False):
        scale = 1

        if opt2:
            # vel
            pg.draw.line(screen, pg.Color('green'), self.position,
                         (self.position + self.velocity * scale), 4)
            # desired
            pg.draw.line(screen, pg.Color('orange'), self.position,
                         (self.position + self.desired * scale), 4)

        if opt3:
            # wander ring representation
            pg.draw.circle(screen, pg.Color('white'),
                           (int(self.wander_ring_pos.x), int(self.wander_ring_pos.y)), self.wander_ring_radius, 1)
            pg.draw.line(screen, pg.Color('cyan'),
                         self.wander_ring_pos, self.wander_target, 5)

        if opt1:
            # food / poison attraction
            if self.velocity.length():
                direction = self.velocity.normalize()
            else:
                direction = self.velocity
            pg.draw.line(screen, pg.Color('darkgreen'), self.position,
                         (self.position + (direction * self.food_attraction) * scale * 15), 4)
            pg.draw.line(screen, pg.Color('red'), self.position,
                         (self.position + (direction * self.poison_attraction) * scale * 15), 2)
            # food / poison view distance
            pg.draw.circle(screen, pg.Color('darkgreen'),
                           (int(self.position.x), int(self.position.y)), self.food_distance, 1)
            pg.draw.circle(screen, pg.Color('darkred'),
                           (int(self.position.x), int(self.position.y)), self.poison_distance, 1)


class Food(pg.sprite.Sprite):
    def __init__(self, pos, is_poison=False):
        super().__init__()  # init pg.sprite.Sprite
        self.image = pg.Surface((6, 6), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.position = pos
        self.poison = is_poison
        self.color = pg.Color('green')
        if self.poison:
            self.color = pg.Color('red')
        pg.draw.circle(self.image, self.color, (3, 3), 3)


class Game:
    def __init__(self):
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT
        self.fps = FPS
        self.running = True
        pg.init()
        self.screen = screen
        self.clock = clock

        self.draw_vectors = False
        self.draw_vectors2 = False
        self.draw_vectors3 = False

        # to easily use update on all the sprites
        self.all_sprites = pg.sprite.Group()

        # vehicle sprites
        self.vehicle_sprites = pg.sprite.Group()
        self.max_vehicles = 10
        # food sprites
        self.food_sprites = pg.sprite.Group()
        self.max_food = 50
        # poison sprites
        self.poison_sprites = pg.sprite.Group()
        self.max_poison = 50

        # most ancient vehicle
        self.age_record = 0

    def events(self):
        # Events here, without pg.event.get() or pg.event.wait() window becomes irresponsibe
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            # this will process they keystroke once, without repeating if holded down
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_v:
                    self.draw_vectors = not self.draw_vectors
                elif event.key == pg.K_b:
                    self.draw_vectors2 = not self.draw_vectors2
                elif event.key == pg.K_n:
                    self.draw_vectors3 = not self.draw_vectors3
                elif event.key == pg.K_m:
                    for sprite in self.all_sprites:
                        sprite.kill()

    def key_events(self):
        pass
        # this will trigger the action meanwhile the key is pressed down
        # pressed = pg.key.get_pressed()
        # if pressed[pg.K_LEFT]:
        # move left

    def check_newpos_isvalid(self, newpos, dist=35):
        valid = True
        for s in self.all_sprites:
            if (newpos - s.position).length() < dist:
                valid = False
                break

        return valid

    def spawn_food(self):
        # food_distance = (self.position - food.position).length()
        # spawns one kind of food at a time
        if len(self.food_sprites) < self.max_food:
            newpos = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))

            if self.check_newpos_isvalid(newpos):
                f = Food(newpos)
                self.food_sprites.add(f)
                self.all_sprites.add(f)

        if len(self.poison_sprites) < self.max_poison:
            newpos = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))

            if self.check_newpos_isvalid(newpos):
                f = Food((newpos), is_poison=True)
                self.poison_sprites.add(f)
                self.all_sprites.add(f)

    def spawn_vehicles(self):
        # create a Vehicle
        if len(self.vehicle_sprites) < self.max_vehicles:
            newpos = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))

            if self.check_newpos_isvalid(newpos):
                p = Vehicle(newpos, 32)
                self.all_sprites.add(p)
                self.vehicle_sprites.add(p)

    def process_collisions(self):
        # check for food collisions
        hits = pg.sprite.groupcollide(self.vehicle_sprites, self.food_sprites, False, True,
                                      collided=pg.sprite.collide_circle_ratio(0.55))
        if hits:
            for hit in hits:
                # we did eat a good food, increase health
                hit.health += 20
                # we have a maximum health
                hit.health = min(hit.max_health, hit.health)

        # check for poison collisions
        hits = pg.sprite.groupcollide(self.vehicle_sprites, self.poison_sprites, False, True,
                                      collided=pg.sprite.collide_circle_ratio(0.55))
        if hits:
            for hit in hits:
                # we did eat some poison, lower the health
                hit.health -= 40

    def game_loop(self):
        while self.running:
            # get delta time in seconds (default is miliseconds)
            dt = self.clock.get_time() / 1000

            # spawn food & poison
            self.spawn_food()
            # spawn vehicles
            self.spawn_vehicles()

            self.events()
            self.key_events()

            # search for food:
            for vehicle in self.vehicle_sprites:
                vehicle.search_food(self.food_sprites, self.poison_sprites)

            # update all the sprites
            self.all_sprites.update(dt)

            self.process_collisions()

            # fill the screen then draw sprites
            self.screen.fill((25, 25, 25))
            self.all_sprites.draw(self.screen)

            for v in self.vehicle_sprites:
                v.draw_vectors(self.screen, self.draw_vectors,
                               self.draw_vectors2, self.draw_vectors3)
                if v.age > self.age_record:
                    self.age_record = v.age
                    print(f"\nmax hp: {v.max_health}  max vel: {v.max_velocity}  max steer: {v.max_steer_force}\n" +
                          f"food attr: {v.food_attraction} poison attr: {v.poison_attraction}\n" +
                          f"food dist: {v.food_distance}  poison dist: {v.poison_distance}  current HP: {v.health}\n" +
                          f"age: {v.age} seconds.")

            # switch "frame"
            pg.display.flip()

            pg.display.set_caption("{:.2f}".format(clock.get_fps()))
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()
        pg.quit()


if __name__ == "__main__":
    WIN_WIDTH = 1080
    WIN_HEIGHT = 640
    FPS = 60

    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pg.time.Clock()
    game = Game()
    game.run()
