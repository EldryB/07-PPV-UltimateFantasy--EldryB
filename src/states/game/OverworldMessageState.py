from typing import Any, Callable, Optional

import pygame

from gale.state import BaseState
from gale.ui.text_box import TextBox

import settings


class OverworldMessageState(BaseState):
    def enter(
        self,
        party_menu_state: Any,
        message: str = "",
        on_close: Optional[Callable[[], None]] = None,
    ) -> None:
        self.party_menu_state = party_menu_state
        self._on_close = on_close or (lambda: None)
        self.textbox = TextBox(
            0,
            settings.VIRTUAL_HEIGHT - 64,
            settings.VIRTUAL_WIDTH,
            64,
            message,
            font=settings.FONTS["medium"],
            lines_per_page=3,
            on_close=self._on_textbox_close,
        )

    def _on_textbox_close(self) -> None:
        self.state_machine.pop()
        self._on_close()

    def update(self, dt: float) -> None:
        pass

    def on_input(self, input_id: str, input_data: Any) -> None:
        if input_id in ("space", "enter") and input_data.pressed:
            self.textbox.advance()

    def render(self, surface: pygame.Surface) -> None:
        self.party_menu_state.render(surface)
        self.textbox.render(surface)
