
from typing import Any

import pygame

from gale.state import BaseState

import settings
from src.gui.Panel import Panel
from gale.ui.progress_bar import ProgressBar
from src.gui.theme import BAR_THEME
from gale.ui.cursor import Cursor


class PartyMenuState(BaseState):
    def enter(self, play_state: Any) -> None:
        self.play_state = play_state
        self.party = play_state.world.party

        #Los 4 paneles de los personajes
        self.panels = []
        self.characters = []
        
        panel_width = settings.VIRTUAL_WIDTH // 4
        panel_height = 100
        y_pos = (settings.VIRTUAL_HEIGHT - panel_height) // 2

        for i, character_key in enumerate(sorted(self.party.characters.keys())):
            char = self.party.characters[character_key]
            self.characters.append(char)
            x_pos = i * panel_width
            panel = Panel(x_pos, y_pos, panel_width, panel_height)
            self.panels.append(panel)

        self.current_selection = 0
        for i, char in enumerate(self.characters):
            if not char.dead:
                self.current_selection = i
                break

        self.cursor = Cursor(settings.TEXTURES["cursor-right"])

    def update(self, dt: float) -> None:
        pass

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "move_left":
            self._prev_alive()
        elif input_id == "move_right":
            self._next_alive()
        elif input_id == "enter":
            self._select_character()
        elif input_id == "back":
            self.state_machine.pop()

    def _next_alive(self) -> None:
        n = len(self.characters)
        for step in range(1, n + 1):
            i = (self.current_selection + step) % n
            if not self.characters[i].dead:
                self.current_selection = i
                settings.SOUNDS["blip"].stop()
                settings.SOUNDS["blip"].play()
                return

    def _prev_alive(self) -> None:
        n = len(self.characters)
        for step in range(1, n + 1):
            i = (self.current_selection - step) % n
            if not self.characters[i].dead:
                self.current_selection = i
                settings.SOUNDS["blip"].stop()
                settings.SOUNDS["blip"].play()
                return

    def _select_character(self) -> None:
        settings.SOUNDS["blip"].stop()
        settings.SOUNDS["blip"].play()
        
        from src.states.game.OverworldActionState import OverworldActionState

        char = self.characters[self.current_selection]
        self.state_machine.push(
            OverworldActionState(self.state_machine),
            play_state=self.play_state,
            party_menu_state=self,
            entity=char,
        )

    def render(self, surface: pygame.Surface) -> None:
        font = settings.FONTS["small"]
        for i, panel in enumerate(self.panels):
            panel.render(surface)
            char = self.characters[i]
            
            #informacion del personaje
            color = settings.COLOR_WHITE if not char.dead else settings.COLOR_GRAY
            name_surf = font.render(char.name, False, color)
            surface.blit(name_surf, (panel.x + 8, panel.y + 8))
            
            lvl_surf = font.render(f"LVL: {char.level}", False, settings.COLOR_WHITE)
            surface.blit(lvl_surf, (panel.x + 8, panel.y + 24))

            hp_surf = font.render(f"HP: {char.current_hp}/{char.hp}", False, settings.COLOR_WHITE)
            surface.blit(hp_surf, (panel.x + 8, panel.y + 40))
            
            hp_bar = ProgressBar(
                panel.x + 8,
                panel.y + 56,
                panel.width - 16,
                4,
                value=char.current_hp,
                max_value=char.hp,
                color=settings.COLOR_HP_BAR,
                theme=BAR_THEME,
            )
            hp_bar.render(surface)

            mag_surf = font.render(f"MAG: {char.magic}", False, settings.COLOR_WHITE)
            surface.blit(mag_surf, (panel.x + 8, panel.y + 64))

            exp_bar = ProgressBar(
                panel.x + 8,
                panel.y + 80,
                panel.width - 16,
                4,
                value=char.current_exp,
                max_value=char.exp_to_level,
                color=settings.COLOR_MAG_BAR,
                theme=BAR_THEME,
            )
            exp_bar.render(surface)
            
        #Cursor(manito)
        if self.cursor:
            panel = self.panels[self.current_selection]
            self.cursor.render(surface, (panel.x - 8, panel.y + 8))
