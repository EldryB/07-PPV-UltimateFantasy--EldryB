from typing import Any

import pygame

from gale.state import BaseState

import settings
from gale.ui.cursor import Cursor

from src.states.game.OverworldMessageState import OverworldMessageState


class OverworldTargetState(BaseState):
    def enter(
        self,
        play_state: Any,
        party_menu_state: Any,
        action: Any,
        entity: Any
    ) -> None:
        self.play_state = play_state
        self.party_menu_state = party_menu_state
        self.action = action
        self.entity = entity

        self.targets = self.party_menu_state.characters
        self.current_selection = 0
        for i, target in enumerate(self.targets):
            if not target.dead:
                self.current_selection = i
                break

        self.cursor = Cursor(settings.TEXTURES["cursor-right"])

    def _next_alive(self) -> None:
        n = len(self.targets)
        for step in range(1, n + 1):
            i = (self.current_selection + step) % n
            if not self.targets[i].dead:
                self.current_selection = i
                settings.SOUNDS["blip"].stop()
                settings.SOUNDS["blip"].play()
                return

    def _prev_alive(self) -> None:
        n = len(self.targets)
        for step in range(1, n + 1):
            i = (self.current_selection - step) % n
            if not self.targets[i].dead:
                self.current_selection = i
                settings.SOUNDS["blip"].stop()
                settings.SOUNDS["blip"].play()
                return

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
            target = self.targets[self.current_selection]
            self._resolve(target)
        elif input_id == "back":
            self.state_machine.pop()

    def _resolve(self, target: Any) -> None:
        amount = self.action["func"](self.entity, target, self.action.get("strength", 1))
        settings.SOUNDS[self.action["sound_effect"]].play()
        
        self.state_machine.pop()
        self.state_machine.pop()
        
        self.state_machine.push(
            OverworldMessageState(self.state_machine),
            party_menu_state=self.party_menu_state,
            message=f"Healed {target.name} for {amount} HP!",
            on_close=lambda: None
        )

    def render(self, surface: pygame.Surface) -> None:
        self.party_menu_state.render(surface)

        panel = self.party_menu_state.panels[self.current_selection]
        #Posicion del cursor
        self.cursor.render(surface, (panel.x - 8, panel.y + 40))
