
import pygame as pg
import sys
from ui.menus.main_menu import MainMenu
from levels import *
from config import Config
from sound import Sound

class Main():
    """
    Core of the game that manage the main_menu + the gmae
    

    """
    def __init__(self):
        """
        create a new object Main
        """
        # mandatory command by pygame
        pg.init()
        self.window = pg.display.set_mode(Config.WINDOW_SIZE) # , pg.FULLSCREEN)

        # Level Stuff for selection in main menu
        self.levels = levels # levels from levels.py
        self.levels_list = [ (level_name ,False) if i == 0 else (level_name,True) for i , level_name in enumerate(self.levels)] 
        self.current_level_index = 0
        self.max_level_index = len(self.levels)

        self.sound = Sound() # Need to be load before MainMeu  
        self.main_menu = MainMenu(self)
        self.game = None

        # Varible give to game when initialize
        self.delta_time = 1 # utiliser dans le world.update et pour les vitesses
        self.clock = pg.time.Clock() # help managing time
        self.draw2d = False
        self.is_next_game = False


        # Music For main menu
        self.music = pg.mixer.Sound(Config.SOUNDS_FOLDER + "menu/RideOfTheValkyries.mp3")
        self.music.play()

    def loop(self):
        while True :
            game = self.game
            events = self.check_event()
            if game != None: # if game is initialize
                game.run()
                self.game.delta_time = self.delta_time

                if self.game.is_paused and not self.game.is_defeat and not self.game.is_victorious: #when game is paused ,show esc_menu
                    for event in pg.event.get():
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                pg.mouse.get_rel()
                                self.game.is_paused = False
                                self.game.is_esc_menu_active = False
                else:
                    self.game.world.players[0].get_inputs(events) 
                if game.is_game_over() == "defeat" and not self.game.is_defeat: # when game is loose, show defeat menu
                    self.game.is_defeat = True
                    self.game.is_paused = True
                if game.is_game_over() == "victory": # when game is win, show victory menu
                    self.game.is_victorious = True
                    self.game.is_paused = True
                if game.is_abandon: # when game is abandon return to main menu
                    self.unload_game()
                if self.is_next_game:
                    self.next_game()
                    self.is_next_game = False
            else : # else run menu
                self.sound.stop_music()
                self.main_menu.run()

            fps = self.clock.get_fps()
            pg.display.update()
            self.delta_time = self.clock.tick(Config.FRAME_RATE)
            pg.display.set_caption(f"{fps:.2f}")
            pg.event.pump()

    def check_event(self):
        """
        Check if Client ask to quit
        """
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.quit()

            if self.game == None:
                self.main_menu.click(event)
                self.main_menu.hover()
            else:
                self.game.hud.click(event)
                self.game.hud.hover()
        
        self.cursor_visibility()
        return events

    def load_game(self,level):
        self.game = level["type"](level["map_file"], self.draw2d,self.window,self.delta_time,self.clock,self.sound,self)
        pg.mixer.stop()

    def unload_game(self):
        self.game = None
        self.music.play()

    def next_game(self):
        """
        call to switch to the next level
        """
        # backup important player's data
        player = self.game.world.players[0]
        player_health = player.health
        player_health_visual = player.visual_health
        player_current_weapons = player.current_weapon
        player_weapons = player.weapons
        player_ammo = player.ammo

        self.game = None # make sure to clean game
        self.current_level_index += 1
        if self.current_level_index > self.max_level_index:
            self.current_level_index = self.main_level_index 
        level = self.levels[self.levels_list[self.current_level_index][0]]
        self.load_game(level)
        # make sur to remove victorious status
        self.game.is_victorious = False
        self.game.is_paused = False

        # Restore important player's data
        player.health = player_health
        player.visual_health = player_health_visual
        player.current_weapon = player_current_weapons
        player.weapons = player_weapons
        player.ammo = player_ammo


    def quit(self):
        pg.quit()  # quit pygame
        sys.exit()  # better quit, remove some error when  quiting

    def cursor_visibility(self):
        """
        turn on cursor visibility when out of the game or while paused
        """
        if self.game == None or self.game.is_paused:
            pg.event.set_grab(True)
            pg.mouse.set_visible(True)
        else:
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)

if __name__ == "__main__":
    main = Main()
    main.loop()
