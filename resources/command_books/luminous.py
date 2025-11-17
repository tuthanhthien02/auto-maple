"""Command book for Luminous class."""

import math
import random
import time
from typing import Optional, Tuple

from src.common import config, settings, utils
from src.common.logger import get_logger
from src.common.vkeys import key_down, key_up, press
from src.routine.components import Command

FLOOR1_LABEL_PREFIX = ("f1_", "floor1", "f1 ")
FLOOR2_LABEL_PREFIX = ("f2_", "floor2", "f2 ")
FLOOR1_Y_THRESHOLD = 0.07  # y >= 0.07 → floor 1 (move right)
FLOOR2_Y_THRESHOLD = 0.06  # y <= 0.06 → floor 2 (move left)


log = get_logger(__name__)


# Global timing configuration for random delays
class TimingConfig:
    """Global timing configuration for random delays in commands"""

    # Jump_Teleport_Up timing ranges (in seconds)
    JUMP_TELEPORT_UP = {
        "jump_delay": (0.08, 0.12),  # Delay after jump
        "up_hold": (0.04, 0.06),  # UP key hold time
        "teleport_delay": (0.04, 0.06),  # Delay after teleport
        "combo_delay": (0.15, 0.25),  # Delay between combos
    }

    # Jump_Down timing ranges (in seconds)
    JUMP_DOWN = {
        "down_hold": (0.08, 0.12),  # DOWN key hold time (increased for reliability)
        "jump_hold": (0.030, 0.040),  # Jump key hold time (slightly longer)
        "jump_release": (0.018, 0.028),  # Jump key release delay (slightly longer)
        "combo_delay": (0.12, 0.18),  # Delay between combos
    }

    # Teleport timing ranges (in seconds)
    TELEPORT = {
        "direction_delay": (0.06, 0.10),  # Delay after direction key
        "vertical_jump_hold": (0.025, 0.035),  # Jump key hold for vertical teleport
        "vertical_jump_release": (
            0.015,
            0.025,
        ),  # Jump key release for vertical teleport
        "teleport_hold": (0.025, 0.035),  # Teleport key hold
        "teleport_release": (0.015, 0.025),  # Teleport key release
        "combo_delay": (0.10, 0.15),  # Delay between combos
    }

    # Reflection timing ranges (in seconds)
    REFLECTION = {
        "between_casts": (0.04, 0.09),  # Delay between consecutive casts
        "long_between_casts": (0.18, 0.30),  # Dải sleep lớn hơn
    }

    # Heavy skills timing ranges (in seconds)
    HEAVY = {
        "between_casts": (0.12, 0.25),  # Delay between presses
        "long_between_casts": (0.22, 0.39),
        "between_actions": (0.20, 0.45),  # Delay after action completes
    }

    NUDGE = {
        "x": (0.002, 0.006),  # 0.2~0.6% map width
        "y": (0.002, 0.005),  # 0.2~0.5% map height
    }

    # Step movement configuration
    STEP_MOVEMENT = {
        "hold_threshold_multiplier": 1.1,  # Multiplier for move_tolerance to determine hold vs press
        # Distance > (move_tolerance * multiplier) → hold key (xa)
        # Distance ≤ (move_tolerance * multiplier) → press key (gần)
        # Có thể chỉnh multiplier này nếu test thực tế không work:
        # - Tăng multiplier (vd: 2.0, 3.0, 4.0, 5.0) → nhiều trường hợp dùng press key hơn
        # - Giảm multiplier (vd: 1.0, 1.5, 2.0, 2.5) → nhiều trường hợp dùng hold key hơn
    }


class Key:
    """Keybindings - adjust these to match your in-game settings."""

    # Primary skills
    reflection = "q"  # Main attack skill
    apocalypse = "d"  # Secondary attack
    death_scythe = "e"  # Death Scythe
    light_reflection = "2"  # Light mode skill
    dark_reflection = "4"  # Dark mode skill

    # Utility
    teleport = "w"  # Teleport skill
    flash_jump = "s"  # Flash jump if available

    # Buffs
    buff_main = "a"  # Main buff
    buff_secondary = "3"  # Secondary buff

    # Movement keys - FIXED: Use correct key names for vkeys
    left = "left"
    right = "right"
    up = "up"
    down = "down"
    jump = "alt"


class Attack(Command):
    """Basic attack command."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        for _ in range(self.times):
            press(Key.reflection, 1, down_time=0.1, up_time=0.1)


class Reflection(Command):
    """Reflection skill - Main attack skill."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        for _ in range(self.times):
            press(Key.reflection, 1, down_time=0.1, up_time=0.1)
            time.sleep(random.uniform(*TimingConfig.REFLECTION["long_between_casts"]))


class Reflection_Random(Command):
    """Casts only Reflection a random number of times between 1 and 3."""

    def __init__(self, min_times=1, max_times=3):
        super().__init__(locals())
        self.min_times = int(min_times)
        self.max_times = int(max_times)

    def main(self):
        times = random.randint(self.min_times, self.max_times)
        for _ in range(times):
            press(Key.reflection, 1, down_time=0.1, up_time=0.1)
            time.sleep(random.uniform(*TimingConfig.REFLECTION["long_between_casts"]))


class Reflection_Mix_Random(Command):
    # Skill press timing ranges (down_time, up_time)
    REFLECTION_PRESS = ((0.08, 0.12), (0.03, 0.06))
    HEAVY_PRESS = ((0.10, 0.15), (0.04, 0.07))

    """Mix skills per call: 93% Reflection (2–3 casts), 5% Apocalypse (2–3 casts), 2% Death Scythe (1 cast)."""

    def __init__(self, min_times=2, max_times=3):
        super().__init__(locals())
        # Bug fix: Ensure min_times <= max_times to prevent ValueError in random.randint
        self.min_times = int(min_times)
        self.max_times = int(max_times)
        if self.min_times > self.max_times:
            # Swap if min > max to prevent errors
            self.min_times, self.max_times = self.max_times, self.min_times
        # Track last facing direction (True = facing right)
        self._last_face_right: Optional[bool] = True
        # Next direction to face before casting (will be set each run)
        self._next_face_right: Optional[bool] = True

    def _determine_baseline_facing(self) -> Tuple[bool, str]:
        """Determine initial facing direction for this rotation."""
        routine = getattr(config, "routine", None)
        if routine:
            label = None
            current_index = getattr(routine, "index", None)
            try:
                sequence = getattr(routine, "sequence", None)
                if (
                    sequence
                    and isinstance(current_index, int)
                    and 0 <= current_index < len(sequence)
                ):
                    label = getattr(sequence[current_index], "label", None)
            except Exception:
                label = None
            if isinstance(label, str):
                label_lower = label.lower()
                if label_lower.startswith(FLOOR1_LABEL_PREFIX):
                    self._last_face_right = True
                    return True, f"label:{label}"
                if label_lower.startswith(FLOOR2_LABEL_PREFIX):
                    self._last_face_right = False
                    return False, f"label:{label}"
            try:
                floor1_indices = list(getattr(routine, "floor1_indices", []) or [])
                floor2_indices = list(getattr(routine, "floor2_indices", []) or [])
            except Exception:
                floor1_indices = []
                floor2_indices = []
            if current_index is not None:
                if floor1_indices and current_index in floor1_indices:
                    self._last_face_right = True
                    return True, "floor1"
                if floor2_indices and current_index in floor2_indices:
                    self._last_face_right = False
                    return False, "floor2"
            current_variant = getattr(routine, "current_variant", "normal")
            if current_variant in {"floor1_only", "floor2_only"}:
                floor_direction = getattr(routine, "floor_direction", None)
                if floor_direction == "reverse":
                    self._last_face_right = False
                    return False, "routine.reverse"
                if floor_direction in {"forward", "right"}:
                    self._last_face_right = True
                    return True, "routine.forward"
        player_pos = getattr(config, "player_pos", None)
        if player_pos:
            player_y = player_pos[1]
            if player_y >= FLOOR1_Y_THRESHOLD:
                self._last_face_right = True
                return True, f"player_y:{player_y:.3f}"
            if player_y <= FLOOR2_Y_THRESHOLD:
                self._last_face_right = False
                return False, f"player_y:{player_y:.3f}"
        # Fallback to previous state if available
        if self._last_face_right is not None:
            return self._last_face_right, "state"
        # Default to facing right
        return True, "default"

    def _next_facing_direction(self) -> bool:
        """Return the next facing direction (True = right) and toggle state."""
        if self._next_face_right is None:
            self._next_face_right = True
        face_right = self._next_face_right
        self._last_face_right = face_right
        self._next_face_right = not face_right
        return face_right

    def _face_direction(
        self, skill_name: str, cast_index: int, total_casts: int
    ) -> str:
        """Tap the direction key to face before casting a skill."""
        face_right = self._next_facing_direction()
        direction = "right" if face_right else "left"
        key = Key.right if face_right else Key.left
        down_time = random.uniform(0.04, 0.07)
        up_time = random.uniform(0.02, 0.05)
        log.debug(
            "Reflection_Mix_Random: Facing %s before %s (cast %d/%d, down=%.3fs, up=%.3fs)",
            direction,
            skill_name,
            cast_index,
            total_casts,
            down_time,
            up_time,
        )
        press(key, 1, down_time=down_time, up_time=up_time)
        return direction

    def _press_skill(
        self,
        key: str,
        skill_name: str,
        cast_index: int,
        total_casts: int,
        down_range: Tuple[float, float],
        up_range: Tuple[float, float],
    ) -> None:
        """Press a skill key with human-like random timing."""
        down_time = random.uniform(*down_range)
        up_time = random.uniform(*up_range)
        log.debug(
            "Reflection_Mix_Random: Casting %s (cast %d/%d, down=%.3fs, up=%.3fs)",
            skill_name,
            cast_index,
            total_casts,
            down_time,
            up_time,
        )
        press(key, 1, down_time=down_time, up_time=up_time)

    def main(self):
        # Check if alternate facing is enabled via bot_config (default: True)
        face_alternate = True
        try:
            bot_cfg = getattr(config, "bot_config", None)
            if bot_cfg is not None:
                face_alternate = bool(
                    bot_cfg.get("luminous.facing.alternate.enabled", True)
                )
        except Exception:
            face_alternate = True

        baseline_face_right, baseline_source = self._determine_baseline_facing()
        self._next_face_right = baseline_face_right
        log.debug(
            "Reflection_Mix_Random: baseline facing %s (source=%s, last_state=%s, alternate=%s)",
            "right" if baseline_face_right else "left",
            baseline_source,
            "right" if self._last_face_right else "left",
            face_alternate,
        )
        # Always validate buffs before executing attack rotation
        buff_casted = Buff().main()
        if buff_casted:
            buff_delay = random.uniform(2.0, 4.0)
            log.debug(
                "Reflection_Mix_Random: buff_main cast → sleeping %.2fs before attacks",
                buff_delay,
            )
            time.sleep(buff_delay)
        else:
            log.debug(
                "Reflection_Mix_Random: buff_main skipped (cooldown still active)"
            )

        secondary_casted = Buff_Secondary().main()
        if secondary_casted:
            secondary_delay = random.uniform(1.0, 1.5)
            log.debug(
                "Reflection_Mix_Random: buff_secondary cast → sleeping %.2fs",
                secondary_delay,
            )
            time.sleep(secondary_delay)
        else:
            log.debug(
                "Reflection_Mix_Random: buff_secondary skipped (cooldown still active)"
            )

        roll = random.random()
        log.debug(
            "Reflection_Mix_Random: skill roll=%.3f (min_times=%d, max_times=%d)",
            roll,
            self.min_times,
            self.max_times,
        )
        if roll < 0.93:
            # Reflection: 93% chance, Use min_times/max_times with minimum 2 casts
            min_casts = max(2, self.min_times)
            max_casts = max(min_casts, self.max_times)  # Ensure max >= min
            times = random.randint(min_casts, max_casts)
            log.debug(
                "Reflection_Mix_Random: executing Reflection %d times (range %d-%d, alternate_facing=%s)",
                times,
                min_casts,
                max_casts,
                face_alternate,
            )
            for cast_idx in range(1, times + 1):
                if face_alternate:
                    self._face_direction("reflection", cast_idx, times)
                self._press_skill(
                    Key.reflection,
                    "reflection",
                    cast_idx,
                    times,
                    *self.REFLECTION_PRESS,
                )
                time.sleep(
                    random.uniform(*TimingConfig.REFLECTION["long_between_casts"])
                )
        elif roll < 0.98:
            # Apocalypse: 5% chance, Use min_times/max_times with minimum 2 casts (consistent with Reflection)
            min_casts = max(2, self.min_times)
            max_casts = max(min_casts, self.max_times)  # Ensure max >= min
            times = random.randint(min_casts, max_casts)
            log.debug(
                "Reflection_Mix_Random: executing Apocalypse %d times (range %d-%d, alternate_facing=%s)",
                times,
                min_casts,
                max_casts,
                face_alternate,
            )
            for cast_idx in range(1, times + 1):
                if face_alternate:
                    self._face_direction("apocalypse", cast_idx, times)
                self._press_skill(
                    Key.apocalypse,
                    "apocalypse",
                    cast_idx,
                    times,
                    *self.HEAVY_PRESS,
                )
                time.sleep(random.uniform(*TimingConfig.HEAVY["long_between_casts"]))
            time.sleep(random.uniform(*TimingConfig.HEAVY["between_actions"]))
        else:
            # Death Scythe: 2% chance, 1 cast (fixed)
            log.debug(
                "Reflection_Mix_Random: executing Death Scythe once (alternate_facing=%s)",
                face_alternate,
            )
            if face_alternate:
                self._face_direction("death_scythe", 1, 1)
            self._press_skill(
                Key.death_scythe,
                "death_scythe",
                1,
                1,
                *self.HEAVY_PRESS,
            )
            time.sleep(random.uniform(*TimingConfig.HEAVY["between_actions"]))


class Apocalypse(Command):
    """Apocalypse skill."""

    def main(self):
        press(Key.apocalypse, 1, down_time=0.1, up_time=0.1)
        time.sleep(0.2)


class Death_Scythe(Command):
    """Death Scythe skill."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        for _ in range(self.times):
            press(Key.death_scythe, 1, down_time=0.1, up_time=0.1)
            time.sleep(random.uniform(*TimingConfig.HEAVY["between_casts"]))


class Apocalypse_Or_Scythe(Command):
    """Randomly uses Apocalypse or Death Scythe.

    Args:
        p_apoc: Probability to cast Apocalypse (0.0–1.0). Remaining goes to Scythe.
        min_times/max_times: Random number of casts each time this command runs.
    """

    def __init__(self, p_apoc=0.5, min_times=1, max_times=1):
        super().__init__(locals())
        self.p_apoc = float(p_apoc)
        self.min_times = int(min_times)
        self.max_times = int(max_times)

    def main(self):
        times = random.randint(self.min_times, self.max_times)
        for _ in range(times):
            if random.random() < self.p_apoc:
                press(Key.apocalypse, 1, down_time=0.1, up_time=0.1)
            else:
                press(Key.death_scythe, 1, down_time=0.1, up_time=0.1)
            time.sleep(random.uniform(*TimingConfig.HEAVY["between_casts"]))
        time.sleep(random.uniform(*TimingConfig.HEAVY["between_actions"]))


class Light_Reflection(Command):
    """Light Reflection skill."""

    def main(self):
        press(Key.light_reflection, 1, down_time=0.1, up_time=0.1)
        time.sleep(0.2)


class Teleport(Command):
    """Teleport in a direction - CONFIGURABLE RANDOM TIMING."""

    def __init__(self, direction="right", times=1):
        super().__init__(locals())
        self.direction = direction
        self.times = int(times)

    def main(self):
        # Luminous teleport with configurable random timing
        direction_key = getattr(Key, self.direction)

        for i in range(self.times):
            try:
                # Hold direction key FIRST with random timing
                key_down(direction_key)
                time.sleep(random.uniform(*TimingConfig.TELEPORT["direction_delay"]))

                # Check direction type for different combos
                if self.direction in ["up", "down"]:
                    # Vertical teleport: Hold direction + Press ALT + Press W
                    key_down(Key.jump)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["vertical_jump_hold"])
                    )
                    key_up(Key.jump)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["vertical_jump_release"])
                    )

                    key_down(Key.teleport)
                    time.sleep(random.uniform(*TimingConfig.TELEPORT["teleport_hold"]))
                    key_up(Key.teleport)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["teleport_release"])
                    )
                else:
                    # Horizontal teleport: Hold direction + Press W (NO ALT)
                    key_down(Key.teleport)
                    time.sleep(random.uniform(*TimingConfig.TELEPORT["teleport_hold"]))
                    key_up(Key.teleport)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["teleport_release"])
                    )

            finally:
                # ALWAYS Release direction key (even if error occurs)
                key_up(direction_key)
                # Small delay after releasing direction key to ensure game processes input
                if i < self.times - 1:
                    time.sleep(random.uniform(*TimingConfig.TELEPORT["combo_delay"]))
                elif i == self.times - 1:
                    # Small delay after last combo to ensure smooth transition
                    time.sleep(random.uniform(0.02, 0.05))


class Teleport_Up(Command):
    """Teleport Up - Hold UP + Press ALT + Press W - FIXED TIMING."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        # Teleport Up combo with fixed timing (150ms total)
        log.debug("🚀 Teleport_Up: Starting %d teleport(s)", self.times)
        for i in range(self.times):
            try:
                # Step 1: Hold UP key (minimal delay for key registration)
                log.debug("🚀 Teleport_Up [%d/%d]: Holding UP key", i + 1, self.times)
                key_down(Key.up)
                time.sleep(0.01)  # 10ms - just enough for key registration

                # Step 2: Press ALT (instant but with micro-pause)
                log.debug(
                    "🚀 Teleport_Up [%d/%d]: Pressing ALT (jump)", i + 1, self.times
                )
                key_down(Key.jump)
                key_up(Key.jump)
                time.sleep(0.005)  # 5ms micro-pause

                # Step 3: Press W (instant but with micro-pause)
                log.debug(
                    "🚀 Teleport_Up [%d/%d]: Pressing W (teleport)", i + 1, self.times
                )
                key_down(Key.teleport)
                key_up(Key.teleport)
                time.sleep(0.005)  # 5ms micro-pause

                log.debug(
                    "🚀 Teleport_Up [%d/%d]: Completed successfully", i + 1, self.times
                )
            except Exception as e:
                log.error(
                    "🚀 Teleport_Up [%d/%d]: Error during execution: %s",
                    i + 1,
                    self.times,
                    e,
                    exc_info=True,
                )
                raise
            finally:
                # Step 4: Release UP key
                key_up(Key.up)
                # Small delay between combos
                if i < self.times - 1:
                    time.sleep(0.01)  # 10ms between combos
        log.debug("🚀 Teleport_Up: Completed all %d teleport(s)", self.times)


class Teleport_Down(Command):
    """Teleport Down - Hold DOWN + Press ALT + Press W (BALANCED - Speed + Anti-Detect)."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        # Teleport Down combo with balanced timing (20ms total)
        for i in range(self.times):
            try:
                # Step 1: Hold DOWN key (minimal delay for key registration)
                key_down(Key.down)
                time.sleep(0.01)  # 10ms - just enough for key registration

                # Step 2: Press ALT (instant but with micro-pause)
                key_down(Key.jump)
                key_up(Key.jump)
                time.sleep(0.005)  # 5ms micro-pause

                # Step 3: Press W (instant but with micro-pause)
                key_down(Key.teleport)
                key_up(Key.teleport)
                time.sleep(0.005)  # 5ms micro-pause

            finally:
                # Step 4: Release DOWN key
                key_up(Key.down)
                # Small delay between combos
                if i < self.times - 1:
                    time.sleep(0.01)  # 10ms between combos


class Jump_Teleport_Up(Command):
    """Jump + Teleport Up combo - Jump + UP + W - SIMPLIFIED VERSION."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        # Jump + Teleport Up combo with configurable random timing
        log.debug("🚀 Jump_Teleport_Up: Starting %d combo(s)", self.times)
        for i in range(self.times):
            try:
                # Step 1: Press ALT (jump) with random timing
                log.debug(
                    "🚀 Jump_Teleport_Up [%d/%d]: Pressing ALT (jump)",
                    i + 1,
                    self.times,
                )
                press(Key.jump, 1, down_time=0.1, up_time=0.1)
                jump_delay = random.uniform(
                    *TimingConfig.JUMP_TELEPORT_UP["jump_delay"]
                )
                time.sleep(jump_delay)

                # Step 2: Hold UP key
                log.debug(
                    "🚀 Jump_Teleport_Up [%d/%d]: Holding UP key", i + 1, self.times
                )
                key_down(Key.up)
                up_hold = random.uniform(*TimingConfig.JUMP_TELEPORT_UP["up_hold"])
                time.sleep(up_hold)

                # Step 3: Press W (teleport) with random timing
                log.debug(
                    "🚀 Jump_Teleport_Up [%d/%d]: Pressing W (teleport)",
                    i + 1,
                    self.times,
                )
                press(Key.teleport, 1, down_time=0.1, up_time=0.1)
                teleport_delay = random.uniform(
                    *TimingConfig.JUMP_TELEPORT_UP["teleport_delay"]
                )
                time.sleep(teleport_delay)

                log.debug(
                    "🚀 Jump_Teleport_Up [%d/%d]: Completed successfully (jump_delay=%.3fs, up_hold=%.3fs, teleport_delay=%.3fs)",
                    i + 1,
                    self.times,
                    jump_delay,
                    up_hold,
                    teleport_delay,
                )
            except Exception as e:
                log.error(
                    "🚀 Jump_Teleport_Up [%d/%d]: Error during execution: %s",
                    i + 1,
                    self.times,
                    e,
                    exc_info=True,
                )
                raise
            finally:
                # Step 4: Release UP key
                key_up(Key.up)
                # Random delay between combos
                if i < self.times - 1:
                    combo_delay = random.uniform(
                        *TimingConfig.JUMP_TELEPORT_UP["combo_delay"]
                    )
                    time.sleep(combo_delay)
        log.debug("🚀 Jump_Teleport_Up: Completed all %d combo(s)", self.times)


class Jump_Down(Command):
    """Jump Down - Hold DOWN + Press ALT, then release DOWN - FIXED TIMING."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        # Jump Down combo with configurable random timing (double-tap jump for reliability)
        for i in range(self.times):
            try:
                # Step 1: Hold DOWN key with random timing
                key_down(Key.down)
                time.sleep(random.uniform(*TimingConfig.JUMP_DOWN["down_hold"]))

                # Step 2: Double-tap ALT while holding DOWN with random timing
                # First tap
                key_down(Key.jump)
                time.sleep(random.uniform(*TimingConfig.JUMP_DOWN["jump_hold"]))
                key_up(Key.jump)
                time.sleep(random.uniform(*TimingConfig.JUMP_DOWN["jump_release"]))

                # Second tap (helps pass one-way platform more reliably)
                key_down(Key.jump)
                time.sleep(random.uniform(*TimingConfig.JUMP_DOWN["jump_hold"]))
                key_up(Key.jump)
                time.sleep(random.uniform(*TimingConfig.JUMP_DOWN["jump_release"]))

                # Brief settle time while still holding DOWN
                time.sleep(0.02)

            finally:
                # Step 3: Release DOWN key
                key_up(Key.down)
                # Random delay between combos
                if i < self.times - 1:
                    time.sleep(random.uniform(*TimingConfig.JUMP_DOWN["combo_delay"]))


class Buff(Command):
    """Required buff command - buffs periodically."""

    # Class-level variable to persist state across instances
    _next_buff_time = 0.0

    def __init__(self):
        super().__init__(locals())

    def main(self):
        now = time.time()
        # Random hóa thời gian buff: 120–170 giây (thay vì cố định 180s)
        if Buff._next_buff_time <= 0.0 or now >= Buff._next_buff_time:
            press(Key.buff_main, 1)
            time.sleep(random.uniform(0.1, 0.2))
            # Lên lịch lần buff tiếp theo
            Buff._next_buff_time = now + random.uniform(120.0, 170.0)
            log.debug(
                "Buff casted, next buff in %.1f seconds",
                Buff._next_buff_time - now,
            )
            return True
        else:
            # Log when buff is skipped due to cooldown
            remaining = Buff._next_buff_time - now
            log.debug("Buff skipped (cooldown: %.1f seconds remaining)", remaining)
        return False


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    # NOTE: This class uses while loops with key_down/key_up pairs.
    # Keys are properly released in the while loop conditions.

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        # Chèn nudge random nhỏ vào position
        nudge_x = random.uniform(*TimingConfig.NUDGE["x"]) * (
            1 if random.random() < 0.5 else -1
        )
        nudge_y = random.uniform(*TimingConfig.NUDGE["y"]) * (
            1 if random.random() < 0.5 else -1
        )
        self.target = (float(x) + nudge_x, float(y) + nudge_y)
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        try:
                            key_down("left")
                            while (
                                config.enabled
                                and d_x < -1 * threshold
                                and walk_counter < 60
                            ):
                                time.sleep(0.05)
                                walk_counter += 1
                                d_x = self.target[0] - config.player_pos[0]
                        finally:
                            key_up("left")
                    else:
                        try:
                            key_down("right")
                            while (
                                config.enabled and d_x > threshold and walk_counter < 60
                            ):
                                time.sleep(0.05)
                                walk_counter += 1
                                d_x = self.target[0] - config.player_pos[0]
                        finally:
                            key_up("right")
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                # Handle Y adjustment (similar to Kanna)
                # Only adjust for small fine-tuning, NOT large floor transitions
                # Large floor transitions should be handled by Move/step() during movement
                y_threshold = settings.adjust_tolerance / math.sqrt(2)
                large_y_change = abs(d_y) > settings.move_tolerance * 1.5

                # Only adjust Y for small fine-tuning, skip if large floor transition
                # (large transitions are handled by step() during Move walk)
                if abs(d_y) > y_threshold and not large_y_change:
                    if d_y < 0:
                        # Moving up: Use Luminous teleport up for small adjustments only
                        Teleport("up").main()
                    else:
                        # Moving down: Use Luminous jump down for small adjustments only
                        Jump_Down(1).main()
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle

        # Safety: ensure all movement keys are released
        key_up("left")
        key_up("right")
        key_up("up")
        key_up("down")


def step(direction, target, distance=None, waypoint_jumped=False):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    Based on Kanna's intelligent step() with Luminous improvements.

    :param direction: Direction to move ('left', 'right', 'up', 'down')
    :param target: Target location
    :param distance: Optional distance to target. If None, will be calculated.
    :param waypoint_jumped: If True, skip auto-jump to prevent duplicate jumps for same waypoint.
    """

    # Calculate distance if not provided
    if distance is None:
        distance = utils.distance(config.player_pos, target)

    # Threshold để quyết định hold vs press
    # Distance > threshold → hold key (xa), ≤ threshold → press key (gần)
    # Configurable via TimingConfig.STEP_MOVEMENT['hold_threshold_multiplier']
    hold_threshold = (
        settings.move_tolerance
        * TimingConfig.STEP_MOVEMENT["hold_threshold_multiplier"]
    )

    # Anti-detect delay (from Kanna)
    if config.stage_fright and direction != "up" and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))

    # Handle different directions (hybrid approach)
    if direction in ("left", "right"):
        # Horizontal movement - Distance-based: Hold (xa) vs Press (gần)
        direction_key = getattr(Key, direction)

        if distance > hold_threshold:
            # Distance xa → Hold key với timing dựa trên distance (human-like)
            # Tính toán hold time dựa trên distance: distance càng xa, hold càng lâu
            # Base hold time: 0.2s, thêm 0.15s cho mỗi 0.1 distance vượt threshold
            base_hold_time = 0.2
            extra_distance = max(
                0.0, distance - hold_threshold
            )  # Bug fix: Ensure non-negative
            # Scale extra time: 0.15s per 0.1 distance, max 0.8s extra
            extra_hold_time = min(extra_distance * 1.5, 0.8)  # Max 0.8s extra
            # Bug fix: Ensure minimum extra_hold_time when distance is just above threshold
            # This prevents hold_time from being too close to base when distance is barely above threshold
            # Minimum 0.01s extra ensures meaningful difference from base
            extra_hold_time = max(0.01, extra_hold_time)
            hold_time = base_hold_time + extra_hold_time
            hold_time = random.uniform(
                hold_time * 0.85, hold_time * 1.15
            )  # Add randomness
            # Bug fix: Ensure minimum hold_time to prevent too-short key presses
            # Minimum 0.05s to ensure key is registered properly
            hold_time = max(0.05, hold_time)

            log.debug(
                "🚶 Human-like: distance xa (%.3f > %.3f) → hold key %s for %.3fs",
                distance,
                hold_threshold,
                direction,
                hold_time,
            )
            try:
                key_down(direction_key)
                time.sleep(hold_time)
            finally:
                key_up(direction_key)
            time.sleep(random.uniform(0.03, 0.08))
        else:
            # Distance gần → Press key (tap ngắn, human-like)
            log.debug(
                "👆 Human-like: distance gần (%.3f ≤ %.3f) → press key %s",
                distance,
                hold_threshold,
                direction,
            )
            press(direction_key, 1, down_time=random.uniform(0.05, 0.08), up_time=0.02)
            time.sleep(random.uniform(0.02, 0.05))
    else:
        # Teleport for vertical movement - FIXED: Hold direction key first
        direction_key = getattr(Key, direction)

        # Check for large Y distance changes (floor transitions) - similar to Kanna
        # Auto-jump BEFORE teleport for large Y changes
        # NOTE: Only jump once per step() call to prevent duplicate jumps when step() is called
        # multiple times in Move loop. After teleport, Y distance will decrease, so subsequent
        # step() calls won't trigger jump again.
        d_y = target[1] - config.player_pos[1]
        large_y_change = abs(d_y) > settings.move_tolerance * 1.5
        has_auto_jumped = False

        # Only auto-jump if:
        # 1. Large Y change detected (floor transition)
        # 2. Direction is vertical
        # 3. Haven't already jumped for this waypoint (prevents duplicate jumps)
        # This prevents duplicate jumps when step() is called multiple times for same waypoint
        if large_y_change and direction in ("up", "down") and not waypoint_jumped:
            # Large Y change indicates floor transition - jump before teleport (like Kanna)
            if direction == "down":
                log.debug(
                    "🔄 Auto-jump: Large Y change (%.3f) detected, jumping down before teleport (waypoint_jumped=%s)",
                    d_y,
                    waypoint_jumped,
                )
                press(Key.jump, 3)
                has_auto_jumped = True
            elif direction == "up":
                log.debug(
                    "🔄 Auto-jump: Large Y change (%.3f) detected, jumping up before teleport (waypoint_jumped=%s)",
                    d_y,
                    waypoint_jumped,
                )
                press(Key.jump, 1)
                has_auto_jumped = True

        try:
            # Hold direction key FIRST with random timing (like Teleport class)
            key_down(direction_key)
            time.sleep(random.uniform(*TimingConfig.TELEPORT["direction_delay"]))

            if direction in ("up", "down"):
                # Vertical teleport: Hold direction + Press ALT + Press W
                log.debug(
                    "step: vertical move start → dir=%s target_y=%.3f current_y=%.3f d_y=%.3f large_change=%s",
                    direction,
                    target[1],
                    config.player_pos[1],
                    d_y,
                    large_y_change,
                )
                # NOTE: Skip jump in teleport combo if already auto-jumped OR waypoint_jumped
                # to avoid duplicate jumps when step() is called multiple times in Move loop
                if not has_auto_jumped and not waypoint_jumped:
                    # Only jump in teleport combo if:
                    # 1. Not already auto-jumped in this step() call
                    # 2. Not already jumped for this waypoint (prevents duplicate when step() called again)
                    key_down(Key.jump)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["vertical_jump_hold"])
                    )
                    key_up(Key.jump)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["vertical_jump_release"])
                    )

                num_presses = 2 if large_y_change else 1
                log.debug(
                    "step: executing %d vertical teleports (direction=%s, large_change=%s)",
                    num_presses,
                    direction,
                    large_y_change,
                )
                for _ in range(num_presses):
                    key_down(Key.teleport)
                    time.sleep(random.uniform(*TimingConfig.TELEPORT["teleport_hold"]))
                    key_up(Key.teleport)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["teleport_release"])
                    )
            else:
                # Horizontal teleport: Hold direction + Press W (NO ALT)
                num_presses = 2
                for _ in range(num_presses):
                    key_down(Key.teleport)
                    time.sleep(random.uniform(*TimingConfig.TELEPORT["teleport_hold"]))
                    key_up(Key.teleport)
                    time.sleep(
                        random.uniform(*TimingConfig.TELEPORT["teleport_release"])
                    )
        finally:
            # ALWAYS Release direction key
            key_up(direction_key)
            # Allow time for floor transition to register after vertical teleport
            if direction in ("up", "down"):
                transition_delay = random.uniform(0.15, 0.25)
                log.debug(
                    "step: vertical transition delay %.3fs applied (direction=%s, waypoint_jumped=%s)",
                    transition_delay,
                    direction,
                    waypoint_jumped,
                )
                time.sleep(transition_delay)
                remaining_y = abs(target[1] - config.player_pos[1])
                log.debug(
                    "step: post-teleport y delta=%.4f (target_y=%.3f, current_y=%.3f)",
                    remaining_y,
                    target[1],
                    config.player_pos[1],
                )
                if large_y_change and remaining_y > settings.move_tolerance * 1.2:
                    log.warning(
                        "step: vertical transition incomplete (delta=%.4f>threshold). Retrying teleport %s.",
                        remaining_y,
                        direction,
                    )
                    try:
                        Teleport(direction, 1).main()
                    except Exception as retry_error:
                        log.error(
                            "step: retry teleport failed for direction %s: %s",
                            direction,
                            retry_error,
                            exc_info=True,
                        )


# ==================== RANDOM ACTIONS ====================
# Custom commands with probability/randomness


class Random_Teleport(Command):
    """Randomly teleports in a direction with a given probability."""

    def __init__(self, direction, probability=0.5, count=1):
        super().__init__(locals())
        self.direction = str(direction)
        self.probability = float(probability)
        self.count = int(count)

    def main(self):
        # Roll the dice: only execute if random() < probability
        if utils.bernoulli(self.probability):
            for _ in range(self.count):
                press(Key.teleport, 1, down_time=0.1, up_time=0.1)
                if self.direction == "right":
                    press(Key.right, 1)
                elif self.direction == "left":
                    press(Key.left, 1)
                elif self.direction == "up":
                    key_down(Key.up)
                    time.sleep(0.05)
                    key_up(Key.up)
                time.sleep(0.15)


class Random_Attack(Command):
    """Randomly chooses between different attack skills."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        for _ in range(self.times):
            # 70% reflection, 30% apocalypse
            if utils.bernoulli(0.7):
                press(Key.reflection, 1, down_time=0.1, up_time=0.1)
            else:
                press(Key.apocalypse, 1, down_time=0.1, up_time=0.1)
            time.sleep(0.1)


class Random_Skill(Command):
    """Executes one of multiple skills randomly."""

    def __init__(self, *skills):
        super().__init__(locals())
        self.skills = skills  # e.g., ('reflection', 'apocalypse', 'light_reflection')

    def main(self):
        # Pick a random skill
        import random

        skill_name = random.choice(self.skills)

        # Execute the skill
        if hasattr(Key, skill_name):
            key = getattr(Key, skill_name)
            press(key, 1, down_time=0.1, up_time=0.1)
        else:
            print(f"[!] Unknown skill: {skill_name}")


class Conditional_Action(Command):
    """Executes different actions based on probability distribution."""

    def __init__(self, action1="attack", p1=0.5, action2="teleport", p2=0.5):
        super().__init__(locals())
        self.action1 = str(action1)
        self.p1 = float(p1)
        self.action2 = str(action2)
        self.p2 = float(p2)

    def main(self):
        # Normalize probabilities
        total = self.p1 + self.p2
        p1_normalized = self.p1 / total

        if utils.bernoulli(p1_normalized):
            # Execute action1
            if self.action1 == "attack":
                press(Key.reflection, 1)
            elif self.action1 == "teleport":
                press(Key.teleport, 1)
                press(Key.right, 1)
        else:
            # Execute action2
            if self.action2 == "attack":
                press(Key.reflection, 1)
            elif self.action2 == "teleport":
                press(Key.teleport, 1)
                press(Key.up, 1)

        time.sleep(0.1)


class Face_Right(Command):
    """Tap right key briefly to ensure character faces right."""

    def main(self):
        press(Key.right, 1, down_time=0.05, up_time=0.05)
        time.sleep(random.uniform(0.03, 0.08))


class Face_Left(Command):
    """Tap left key briefly to ensure character faces left."""

    def main(self):
        press(Key.left, 1, down_time=0.05, up_time=0.05)
        time.sleep(random.uniform(0.03, 0.08))


class Buff_Secondary(Command):
    """Casts the secondary buff on a random cooldown between 800-900 seconds."""

    # Class-level variable to persist state across instances
    _next_buff_time = 0.0

    def __init__(self):
        super().__init__(locals())

    def main(self):
        now = time.time()
        if (
            Buff_Secondary._next_buff_time <= 0.0
            or now >= Buff_Secondary._next_buff_time
        ):
            press(Key.buff_secondary, 1)
            time.sleep(random.uniform(0.1, 0.2))
            Buff_Secondary._next_buff_time = now + random.uniform(800.0, 900.0)
            log.debug(
                "Buff Secondary casted, next buff in %.1f seconds",
                Buff_Secondary._next_buff_time - now,
            )
            return True
        else:
            # Log when buff is skipped due to cooldown
            remaining = Buff_Secondary._next_buff_time - now
            log.debug(
                "Buff Secondary skipped (cooldown: %.1f seconds remaining)", remaining
            )
        return False
