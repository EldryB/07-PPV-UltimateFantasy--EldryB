# Ultimate Fantasy

### 🎨 1. Interfaz Gráfica de Usuario (GUI) y Curación
*   **Panel de estado:** Se creó la clase `PartyMenuState` a la cual se accede desde el menú de pausa. Esta dibuja 4 paneles alineados (usando la clase `Panel`), mostrando de forma limpia el Nivel, HP (con barra de vida), Magia y Experiencia (con barra) de cada héroe.
*   **Visualización de acciones:** Al seleccionar a un héroe, se abre `OverworldActionState`. El código renderiza las habilidades de tipo "enemigo" con `set_alpha(100)` para hacerlas translúcidas, mientras que las curativas conservan su opacidad normal.
*   **Curación individual:** Si se selecciona "Heal", el juego entra en `OverworldTargetState`, apareciendo un cursor sobre los paneles de la Party para seleccionar al aliado herido.
*   **Curación global:** Al elegir "Global Heal", el código llama automáticamente a la función de curación en área (`_character_heal_aoe`) y muestra un recuadro de texto en la pantalla (`OverworldMessageState`) indicando cuánta vida recuperaron todos.

### ⏱️ 2. Sistema de Turnos de Batalla por Tiempo de Descanso
*   **Mecánica y Gestión:** En lugar de cronómetros en tiempo real, se diseñó un sistema híbrido por rondas y salto de turnos. Se agregó el atributo `rest_turns` a `BattleEntity`. En el método `update()` de `BattleState`, el juego recorre una fila (queue). Si a la entidad le toca actuar pero su `rest_turns` es mayor a 0, se le resta 1, pierde el turno y aparece un mensaje en pantalla indicando cuántos turnos de espera le faltan. Si es 0, actúa normalmente. 
*   **Penalizaciones por ataque (`wait_turns`):** 
    *   **Guerrero:** `Attack` (0 turnos de penalización).
    *   **Ranger:** `Attack` (0 turnos), `Arrows` (1 turno).
    *   **Mago:** `Flame` (1 turno).
    *   **Sanadora:** `Heal` individual (1 turno), `Global Heal` (2 turnos).
    *   **Enemigos Regulares (Slimes, Worms, Snakes, Pumpkings):** `Attack` (0 turnos).
    *   **Jefe (Man-Eater Flower):** `Attack` (0 turnos), `Flame` (1 turno), `Global Heal` (2 turnos).
