#!/usr/bin/env python3

# Created by: Amir Mersad
# Created on: October 2019
# a game that has a start screen and can play a sound

import ugame
import stage
import constants


def menu_scene():
    # setting text
    NEW_PALETTE = (b'\xff\xaf\x00\x22\xcey\x22\xab\xff\xff\xff\xba\x22\xff\xff\xff'
                   b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
    # image bank
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")
    # set background
    background = stage.Grid(image_bank_1, constants.SCREEN_X,
                            constants.SCREEN_Y)
    # sprite bank
    sprites = []
    # text objects
    text = []
    text1 = stage.Text(width=29, height=12, font=None,
                       palette=NEW_PALETTE, buffer=None)
    text1.move(20, 10)
    text1.text("MT Game Studio")
    text.append(text1)

    text2 = stage.Text(width=29, height=12, font=None,
                       palette=NEW_PALETTE, buffer=None)
    text2.move(40, 110)
    text2.text("Press START")
    text.append(text2)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + sprites + [background]
    game.render_block()

    while True:

        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_START != 0:
            game_scene()

        game.tick()


def game_scene():
    # image bank
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")
    # setting button state
    a_button = constants.button_state["button_up"]
    # setting sound
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    # set background
    background = stage.Grid(image_bank_1, constants.SCREEN_X,
                            constants.SCREEN_Y)
    # sprite bank
    sprites = []
    # load ship sprite
    ship = stage.Sprite(image_bank_1, 4, int(constants.SCREEN_X / 2 -
                        constants.SPRITE_SIZE / 2),
                        int(constants.SCREEN_Y - constants.SPRITE_SIZE +
                        constants.SPRITE_SIZE / 2))
    sprites.append(ship)
    # set game configurations
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = sprites + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        # print (keys)

        if keys & ugame.K_X != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]

        if keys & ugame.K_RIGHT != 0:
            if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
            else:
                ship.move(ship.x + 1, ship.y)

        if keys & ugame.K_LEFT != 0:
            if ship.x < 0:
                ship.move(0, ship.y)
            else:
                ship.move(ship.x - 1, ship.y)

        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)

        game.render_sprites(sprites)
        game.tick()  # wait until refresh rate finishes


if __name__ == "__main__":
    menu_scene()
