
from typing import Any

import pygame

from gale.state import BaseState
from gale.timer import Timer

import settings
from src.gui.Panel import Panel
from gale.ui.cursor import Cursor


class OverworldActionState(BaseState):
    def enter(self, play_state: Any, party_menu_state: Any, entity: Any) -> None:
        self.play_state = play_state
        self.party_menu_state = party_menu_state
        self.entity = entity

        self.panel = Panel(
            settings.VIRTUAL_WIDTH / 2 - 50,
            settings.VIRTUAL_HEIGHT / 2 - 60,
            100,
            120
        )
        self.cursor = Cursor(settings.TEXTURES["cursor-right"])
        
        self.actions = entity.actions + [{"name": "Nothing", "func": self._nothing, "target_type": "none"}]
        self.current_selection = 0

    def _nothing(self, *args, **kwargs) -> None:
        self.state_machine.pop()

    def update(self, dt: float) -> None:
        pass

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "move_up":
            self.current_selection = (self.current_selection - 1) % len(self.actions)
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "move_down":
            self.current_selection = (self.current_selection + 1) % len(self.actions)
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
        elif input_id == "enter":
            self._select_action()
        elif input_id == "back":
            self.state_machine.pop()

    def _select_action(self) -> None:
        action = self.actions[self.current_selection]
        
        if action["name"] == "Nothing":
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()
            self._nothing()
            return
            
        if action["target_type"] != "character":
            settings.SOUNDS["error"].play() if "error" in settings.SOUNDS else None
            return
            
        settings.SOUNDS["blip"].stop()
        settings.SOUNDS["blip"].play()

        if action.get("require_target", False):
            from src.states.game.OverworldTargetState import OverworldTargetState
            self.state_machine.push(
                OverworldTargetState(self.state_machine),
                play_state=self.play_state,
                party_menu_state=self.party_menu_state,
                action=action,
                entity=self.entity
            )
        else:
            targets = [char for char in self.play_state.world.party.characters.values() if not char.dead]
            amount = action["func"](self.entity, targets, action.get("strength", 1))
            settings.SOUNDS[action["sound_effect"]].play()
            
            from src.states.game.OverworldMessageState import OverworldMessageState
            self.state_machine.pop() # Pop ActionState
            self.state_machine.push(
                OverworldMessageState(self.state_machine),
                party_menu_state=self.party_menu_state,
                message=f"Healed everyone for {amount} HP!",
                on_close=lambda: None
            )

    def render(self, surface: pygame.Surface) -> None:
        # Render the party menu underneath
        self.party_menu_state.render(surface)
        
        self.panel.render(surface)
        
        font = settings.FONTS["small"]
        
        for i, action in enumerate(self.actions):
            x = self.panel.x + 16
            y = self.panel.y + 8 + i * 16
            
            text_surf = font.render(action["name"], False, settings.COLOR_WHITE)
            
            if action["target_type"] == "enemy":
                text_surf.set_alpha(100)
            else:
                text_surf.set_alpha(255)
                
            surface.blit(text_surf, (x, y))
            
            if i == self.current_selection:
                self.cursor.render(surface, (x - 12, y + 2))
