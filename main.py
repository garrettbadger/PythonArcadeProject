import arcade
from pyglet.math import Vec2
from Platformer import constants


class MyGame(arcade.Window):
    

    def __init__(self, width, height, title):
       
        super().__init__(width, height, title)

        
        self.static_wall_list = None
        self.moving_wall_list = None

        self.player_list = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None
        self.game_over = False

        # Create the cameras
        self.camera_sprites = arcade.Camera(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

        self.left_down = False
        self.right_down = False

        # Establish a sound
        self.sound = arcade.Sound("Platformer/assets/boing.wav")

    def setup(self):
        
        self.static_wall_list = arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("Platformer/assets/Blocky.png",
                                           constants.SPRITE_SCALING)
        self.player_sprite.center_x = 2 * constants.GRID_PIXEL_SIZE
        self.player_sprite.center_y = 3 * constants.GRID_PIXEL_SIZE
        self.player_list.append(self.player_sprite)

        # Create floor
        for i in range(200):
            if i % 2 == 0:
                #Floor
                wall = arcade.Sprite("Platformer/assets/tile.png", constants.SPRITE_SCALING)
                wall.bottom = 0
                wall.center_x = i * constants.GRID_PIXEL_SIZE
                self.static_wall_list.append(wall)
        for i in range(200):
            if i % 5 == 0:
                # Side to side
                wall = arcade.Sprite("Platformer/assets/tile.png", constants.SPRITE_SCALING)
                wall.center_y = 1.5 * constants.GRID_PIXEL_SIZE
                wall.center_x = i * constants.GRID_PIXEL_SIZE
                wall.boundary_left = i + 2 * constants.GRID_PIXEL_SIZE
                wall.boundary_right = i * 2 * constants.GRID_PIXEL_SIZE
                wall.change_x = 2 * constants.SPRITE_SCALING
                self.moving_wall_list.append(wall)
        for i in range(200):
            if i % 10 == 0:
                # Up and Down
                wall = arcade.Sprite("Platformer/assets/tile.png", constants.SPRITE_SCALING)
                wall.center_y = .5 * constants.GRID_PIXEL_SIZE
                wall.center_x = i * constants.GRID_PIXEL_SIZE
                wall.boundary_top = 4 * constants.GRID_PIXEL_SIZE
                wall.boundary_bottom =  0.5 * constants.GRID_PIXEL_SIZE
                wall.change_y = 2 * constants.SPRITE_SCALING
                self.moving_wall_list.append(wall)

        for i in range(200):
            if i % 8 == 0:
                # Side to side
                wall = arcade.Sprite("Platformer/assets/tile.png", constants.SPRITE_SCALING)
                wall.center_y = 4 * constants.GRID_PIXEL_SIZE
                wall.center_x = i * constants.GRID_PIXEL_SIZE
                wall.boundary_left = 5 * constants.GRID_PIXEL_SIZE
                wall.boundary_right = i* 3 * constants.GRID_PIXEL_SIZE
                wall.change_x = -2 * constants.SPRITE_SCALING
                self.moving_wall_list.append(wall)

        for i in range(200):
            if i % 6 == 0:
                # Diagonal
                wall = arcade.Sprite("Platformer/assets/tile.png", constants.SPRITE_SCALING)
                wall.center_y = 5 * constants.GRID_PIXEL_SIZE
                wall.center_x = i * constants.GRID_PIXEL_SIZE
                wall.boundary_left = 7 * constants.GRID_PIXEL_SIZE
                wall.boundary_right = i * 3 * constants.GRID_PIXEL_SIZE
                wall.boundary_top = 8 * constants.GRID_PIXEL_SIZE
                wall.boundary_bottom = 3 * constants.GRID_PIXEL_SIZE
                wall.change_x = 2 * constants.SPRITE_SCALING
                wall.change_y = 2 * constants.SPRITE_SCALING
                self.moving_wall_list.append(wall)

        # Create our physics engine
        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.player_sprite,
                                           [self.static_wall_list, self.moving_wall_list],
                                           gravity_constant=constants.GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.GRAY)

        self.game_over = False

    def on_draw(self):
       

        # Make sure the screen is clear to draw on
        self.clear()

        # Select the camera 
        self.camera_sprites.use()

        # Draw  sprites.
        self.static_wall_list.draw()
        self.moving_wall_list.draw()
        self.player_list.draw()

        self.camera_gui.use()

        
        distance = self.player_sprite.right
        
        output = f"Distance: {distance}"
        # Draw the text on the screen.
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def set_x_speed(self):
        if self.left_down and not self.right_down:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED
        elif self.right_down and not self.left_down:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        # Jumping
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.JUMP_SPEED
                self.sound.play()
        # Move left
        elif key == arcade.key.LEFT:
            self.left_down = True
            self.set_x_speed()
        # Move right
        elif key == arcade.key.RIGHT:
            self.right_down = True
            self.set_x_speed()

    def on_key_release(self, key, modifiers):
        # Stop moving left
        if key == arcade.key.LEFT:
            self.left_down = False
            self.set_x_speed()
        # Stop moving right
        elif key == arcade.key.RIGHT:
            self.right_down = False
            self.set_x_speed()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()

        # End the game if you fall
        if self.player_sprite.center_y <= 1:
            arcade.exit()

    def scroll_to_player(self):
        
        # Scroll the window to the player.
        

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, constants.CAMERA_SPEED)


def main():
    """ Main function """
    window = MyGame(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()