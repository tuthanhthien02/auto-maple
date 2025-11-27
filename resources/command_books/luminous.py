"""Command book for Luminous class."""

import math
import random
import time
from typing import Any, Tuple

from src.common import config, settings, utils
from src.common.logger import get_logger
from src.common.vkeys import key_down, key_up, press
from src.routine.components import Command

log = get_logger(__name__)


# Movement constants
class MovementConstants:
    """Constants for movement and floor transition logic"""

    FLOOR_TRANSITION_THRESHOLD_MULTIPLIER = 1.5  # settings.move_tolerance * this
    SUCCESS_Y_CHANGE_THRESHOLD = 0.03  # Minimum Y change to consider success
    X_ADJUST_THRESHOLD = 0.01  # Minimum X difference to trigger adjustment
    MAX_STUCK_ATTEMPTS = 10  # Max attempts before considering stuck
    MAX_ADJUST_DURATION = 5.0  # Max seconds for Adjust operation
    MAX_WALK_ITERATIONS = 60  # Max iterations in Adjust walk loop
    WALK_SLEEP_INTERVAL = 0.05  # Sleep interval in Adjust walk loop


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
        "direction_delay": (0.12, 0.20),  # Delay after direction key (increased x2)
        "vertical_jump_hold": (
            0.10,
            0.15,
        ),  # Jump key hold for vertical teleport (increased further)
        "vertical_jump_release": (
            0.015,
            0.025,
        ),  # Jump key release for vertical teleport
        "teleport_hold": (0.10, 0.15),  # Teleport key hold
        "teleport_release": (0.015, 0.025),  # Teleport key release
        "combo_delay": (0.10, 0.15),  # Delay between combos
    }

    # Reflection timing ranges (in seconds)
    REFLECTION = {
        "between_casts": (0.04, 0.09),  # Delay between consecutive casts
        "long_between_casts": (0.25, 0.40),  # Dải sleep lớn hơn
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
    buff_third = "7"  # Third buff

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

    """Mix skills per call: 93% Reflection (2–3 casts), 5% Apocalypse (2–3 casts), 2% Death Scythe (1 cast).

    Args:
        probability: percentage chance to execute the rotation (0 = always skip, 100 = always run)
    """

    def __init__(self, probability=100.0, min_times=2, max_times=3):
        super().__init__(locals())

        # Backward compatibility: older configs used positional order (min_times, max_times, probability).
        try:
            prob_val = float(probability)
            min_val = float(min_times)
            max_val = float(max_times)
        except (TypeError, ValueError):
            prob_val = probability
            min_val = min_times
            max_val = max_times
        else:
            if (
                1 <= prob_val <= 5
                and 1 <= min_val <= 5
                and 0.0 <= max_val <= 100.0
                and max_val > 5
            ):
                log.debug(
                    "Reflection_Mix_Random: detected legacy argument order (min,max,probability) → reassigning"
                )
                probability, min_times, max_times = max_times, prob_val, min_val

        def _rounded_int(value: Any, fallback: int) -> int:
            try:
                return int(round(float(value)))
            except (TypeError, ValueError):
                return fallback

        # Bug fix: Ensure min_times <= max_times to prevent ValueError in random.randint
        rounded_min = _rounded_int(min_times, 2)
        self.min_times = max(1, rounded_min)

        rounded_max = _rounded_int(max_times, max(self.min_times, 2))
        self.max_times = max(self.min_times, rounded_max)

        log.debug(
            "Reflection_Mix_Random: resolved min/max casts → min=%d (raw=%s) | max=%d (raw=%s)",
            self.min_times,
            min_times,
            self.max_times,
            max_times,
        )

        self.execute_probability = max(0.0, min(100.0, float(probability)))

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
        # Check execute probability
        if not utils.bernoulli(self.execute_probability / 100.0):
            log.debug(
                "Reflection_Mix_Random: skipped (execute_probability=%.1f%%)",
                self.execute_probability,
            )
            return
        log.debug(
            "Reflection_Mix_Random: execute_probability roll passed (%.1f%%)",
            self.execute_probability,
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

        third_casted = Buff_Third().main()
        if third_casted:
            third_delay = random.uniform(1.0, 2.0)
            log.debug(
                "Reflection_Mix_Random: buff_third cast → sleeping %.2fs", third_delay
            )
            time.sleep(third_delay)
        else:
            log.debug(
                "Reflection_Mix_Random: buff_third skipped (cooldown still active)"
            )

        roll = random.random()
        log.debug(
            "Reflection_Mix_Random: skill roll=%.3f (min_times=%d, max_times=%d)",
            roll,
            self.min_times,
            self.max_times,
        )
        if roll < 0.93:
            log.debug("Reflection_Mix_Random: roll branch → Reflection (<=0.93)")
            # Reflection: 93% chance, Use min_times/max_times with minimum 2 casts
            min_casts = max(2, self.min_times)
            max_casts = max(min_casts, self.max_times)  # Ensure max >= min
            times = random.randint(min_casts, max_casts)
            log.debug(
                "Reflection_Mix_Random: Reflection random.randint(%d, %d) -> %d casts",
                min_casts,
                max_casts,
                times,
            )
            for cast_idx in range(1, times + 1):
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
            log.debug(
                "Reflection_Mix_Random: roll branch → Apocalypse (0.93 ≤ roll < 0.98)"
            )
            # Apocalypse: 5% chance, Use min_times/max_times with minimum 2 casts (consistent with Reflection)
            min_casts = max(2, self.min_times)
            max_casts = max(min_casts, self.max_times)  # Ensure max >= min
            times = random.randint(min_casts, max_casts)
            log.debug(
                "Reflection_Mix_Random: Apocalypse random.randint(%d, %d) -> %d casts",
                min_casts,
                max_casts,
                times,
            )
            for cast_idx in range(1, times + 1):
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
            log.debug("Reflection_Mix_Random: roll branch → Death Scythe (>=0.98)")
            log.debug("Reflection_Mix_Random: executing Death Scythe once")
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
    """
    Teleports in a given direction, jumping if specified. Adds the player's position
    to the current Layout if necessary.
    """

    def __init__(self, direction, jump="False"):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 3
        time.sleep(0.05)
        if self.direction in ["up", "down"]:
            num_presses = 2
        if self.direction != "up":
            key_down(self.direction)
            time.sleep(0.05)
        if self.jump:
            if self.direction == "down":
                press(Key.jump, 3, down_time=0.1)
            else:
                press(Key.jump, 1)
        if self.direction == "up":
            key_down(self.direction)
            time.sleep(0.05)
        press(Key.teleport, num_presses)
        key_up(self.direction)
        if settings.record_layout:
            config.layout.add(*config.player_pos)


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
                teleport_hold_time = random.uniform(
                    *TimingConfig.TELEPORT["teleport_hold"]
                )
                press(Key.teleport, 1, down_time=teleport_hold_time, up_time=0.1)
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
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        start_time = time.time()

        while (
            config.enabled
            and counter > 0
            and error > settings.adjust_tolerance
            and (time.time() - start_time) < MovementConstants.MAX_ADJUST_DURATION
        ):
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
                                and walk_counter < MovementConstants.MAX_WALK_ITERATIONS
                            ):
                                time.sleep(MovementConstants.WALK_SLEEP_INTERVAL)
                                walk_counter += 1
                                d_x = self.target[0] - config.player_pos[0]
                        except Exception as e:
                            log.error(f"Adjust: Error in left movement: {e}")
                        finally:
                            key_up("left")
                    else:
                        try:
                            key_down("right")
                            while (
                                config.enabled
                                and d_x > threshold
                                and walk_counter < MovementConstants.MAX_WALK_ITERATIONS
                            ):
                                time.sleep(MovementConstants.WALK_SLEEP_INTERVAL)
                                walk_counter += 1
                                d_x = self.target[0] - config.player_pos[0]
                        except Exception as e:
                            log.error(f"Adjust: Error in right movement: {e}")
                        finally:
                            key_up("right")
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        try:
                            Teleport("up").main()
                        except Exception as e:
                            log.error(f"Adjust: Error in teleport up: {e}")
                    else:
                        try:
                            key_down("down")
                            time.sleep(0.05)
                            press(Key.jump, 2, down_time=0.1)
                            key_up("down")
                            time.sleep(0.05)
                        except Exception as e:
                            log.error(f"Adjust: Error in jump down: {e}")
                            key_up("down")  # Ensure cleanup
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle

        if (time.time() - start_time) >= MovementConstants.MAX_ADJUST_DURATION:
            log.warning(
                "Adjust: Timeout after %.1fs, breaking (error=%.4f)",
                MovementConstants.MAX_ADJUST_DURATION,
                error,
            )


class Move(Command):
    """Moves to a given position using the shortest path based on the current Layout.
    Includes floor transition retry logic with X-axis adjustment.
    """

    def __init__(self, x, y, max_steps=15):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)
        self.prev_direction = ""
        # Track floor transition attempts per direction
        self._floor_transition_attempts = {}
        self._floor_transition_initial_y = {}
        # Stuck detection
        self._stuck_position = None
        self._stuck_attempts = 0
        self._last_cleanup_time = time.time()

    def _new_direction(self, new):
        """Change direction with error handling."""
        try:
            if self.prev_direction and self.prev_direction != new:
                key_up(self.prev_direction)
            key_down(new)
            self.prev_direction = new
        except Exception as e:
            log.error(f"Move: Error in _new_direction({new}): {e}")
            # Ensure keys are released on error
            if self.prev_direction:
                try:
                    key_up(self.prev_direction)
                except Exception:
                    pass
            raise

    def _cleanup_old_tracking(self, max_age_seconds=300):
        """Remove tracking entries older than max_age_seconds to prevent memory leak."""
        current_time = time.time()
        if current_time - self._last_cleanup_time < 60:  # Only cleanup every 60 seconds
            return

        # Cleanup is done by removing entries that haven't been accessed
        # In practice, we'll just reset if dictionary gets too large
        if len(self._floor_transition_attempts) > 100:
            log.debug("Move: Cleaning up old tracking entries")
            self._floor_transition_attempts.clear()
            self._floor_transition_initial_y.clear()

        self._last_cleanup_time = current_time

    def _detect_stuck(self, point):
        """Detect if bot is stuck at a position."""
        current_pos = config.player_pos
        if self._stuck_position is None:
            self._stuck_position = current_pos
            self._stuck_attempts = 0
            return False

        # Check if position hasn't changed significantly
        distance = utils.distance(current_pos, self._stuck_position)
        if distance < settings.move_tolerance:
            self._stuck_attempts += 1
            if self._stuck_attempts >= MovementConstants.MAX_STUCK_ATTEMPTS:
                log.warning(
                    "Move: Bot appears stuck at position (%.3f, %.3f) after %d attempts",
                    current_pos[0],
                    current_pos[1],
                    self._stuck_attempts,
                )
                return True
        else:
            # Position changed, reset stuck detection
            self._stuck_position = current_pos
            self._stuck_attempts = 0

        return False

    def _handle_floor_transition_retry(self, direction, point):
        """Handle floor transition retry logic with X-axis adjustment."""
        # Cleanup old tracking periodically
        self._cleanup_old_tracking()

        direction_key = (
            f"{direction}_{point[1]:.3f}"  # Unique key per direction+target_y
        )

        # Initialize tracking for this direction/target
        if direction_key not in self._floor_transition_attempts:
            self._floor_transition_attempts[direction_key] = 0
            self._floor_transition_initial_y[direction_key] = config.player_pos[1]

        attempts = self._floor_transition_attempts[direction_key]
        initial_y = self._floor_transition_initial_y[direction_key]

        # If 1 attempt failed, adjust X axis before retrying
        if attempts >= 1:
            log.debug(
                "Move: Floor transition failed, adjusting X axis (current_y=%.3f, target_y=%.3f, direction=%s)",
                config.player_pos[1],
                point[1],
                direction,
            )
            # Small horizontal adjustment to avoid getting stuck
            d_x = point[0] - config.player_pos[0]
            if abs(d_x) > MovementConstants.X_ADJUST_THRESHOLD:
                adjust_direction = "right" if d_x > 0 else "left"
                try:
                    key_down(adjust_direction)
                    time.sleep(random.uniform(0.05, 0.10))
                    key_up(adjust_direction)
                    time.sleep(random.uniform(0.05, 0.10))
                except Exception as e:
                    log.error(f"Move: Error in X-axis adjustment: {e}")
                    try:
                        key_up(adjust_direction)
                    except Exception:
                        pass
            # Reset counter after adjustment
            self._floor_transition_attempts[direction_key] = 0
            self._floor_transition_initial_y[direction_key] = config.player_pos[1]

        return initial_y

    def _check_floor_transition_success(self, direction, point, initial_y):
        """Check if floor transition was successful and update attempt counter."""
        if initial_y is None:
            return

        direction_key = f"{direction}_{point[1]:.3f}"
        y_change = abs(config.player_pos[1] - initial_y)

        # Consider successful if Y changed significantly
        if y_change > MovementConstants.SUCCESS_Y_CHANGE_THRESHOLD:
            # Success - reset counter
            self._floor_transition_attempts[direction_key] = 0
            self._floor_transition_initial_y[direction_key] = None
            log.debug(
                "Move: Floor transition successful (y_change=%.3f, direction=%s)",
                y_change,
                direction,
            )
        else:
            # Failed - increment counter
            self._floor_transition_attempts[direction_key] += 1
            log.debug(
                "Move: Floor transition attempt %d failed (y_change=%.3f, current_y=%.3f, direction=%s)",
                self._floor_transition_attempts[direction_key],
                y_change,
                config.player_pos[1],
                direction,
            )

    def main(self):
        counter = self.max_steps
        path = config.layout.shortest_path(config.player_pos, self.target)
        for i, point in enumerate(path):
            toggle = True
            # Release any direction key from previous point before starting new point
            if self.prev_direction:
                key_up(self.prev_direction)
                self.prev_direction = ""
            local_error = utils.distance(config.player_pos, point)
            global_error = utils.distance(config.player_pos, self.target)
            while (
                config.enabled
                and counter > 0
                and local_error > settings.move_tolerance
                and global_error > settings.move_tolerance
            ):
                if toggle:
                    d_x = point[0] - config.player_pos[0]
                    if abs(d_x) > settings.move_tolerance / math.sqrt(2):
                        if d_x < 0:
                            key = "left"
                        else:
                            key = "right"
                        self._new_direction(key)
                        step(key, point)
                        if settings.record_layout:
                            config.layout.add(*config.player_pos)
                        counter -= 1
                        if i < len(path) - 1:
                            time.sleep(0.15)
                else:
                    d_y = point[1] - config.player_pos[1]
                    if abs(d_y) > settings.move_tolerance / math.sqrt(2):
                        if d_y < 0:
                            key = "up"
                        else:
                            key = "down"
                        self._new_direction(key)

                        # Check if bot is stuck
                        if self._detect_stuck(point):
                            log.warning("Move: Breaking due to stuck detection")
                            break

                        # Check if this is a floor transition
                        is_floor_transition = (
                            abs(d_y)
                            > settings.move_tolerance
                            * MovementConstants.FLOOR_TRANSITION_THRESHOLD_MULTIPLIER
                        )
                        initial_y = None
                        if is_floor_transition:
                            initial_y = self._handle_floor_transition_retry(key, point)

                        step(key, point)

                        # Check floor transition success after step
                        # Note: step() already includes delay for vertical movement
                        # We check success after step() completes (which includes its own delay)
                        if is_floor_transition and initial_y is not None:
                            # step() already waited 0.3-0.4s for vertical, so position should be updated
                            self._check_floor_transition_success(key, point, initial_y)

                        if settings.record_layout:
                            config.layout.add(*config.player_pos)
                        counter -= 1
                        if i < len(path) - 1:
                            time.sleep(0.05)
                local_error = utils.distance(config.player_pos, point)
                global_error = utils.distance(config.player_pos, self.target)
                toggle = not toggle
            if self.prev_direction:
                key_up(self.prev_direction)


def step(direction, target, distance=None, waypoint_jumped=False):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    Simple implementation - retry logic is handled by Move class.

    Args:
        direction: Direction to move ('left', 'right', 'up', 'down')
        target: Target location (x, y)
        distance: Optional distance to target. If None, will be calculated.
        waypoint_jumped: If True, skip auto-jump to prevent duplicate jumps.
    """
    # Validate direction
    if direction not in ("left", "right", "up", "down"):
        log.error(f"step: Invalid direction '{direction}'")
        return

    # Use distance parameter if provided for optimization
    if distance is None:
        distance = utils.distance(config.player_pos, target)

    # num_presses = 2
    # if direction in ("up", "down"):
    #     num_presses = 1

    if config.stage_fright and direction != "up" and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))

    d_y = target[1] - config.player_pos[1]
    is_floor_transition = (
        abs(d_y)
        > settings.move_tolerance
        * MovementConstants.FLOOR_TRANSITION_THRESHOLD_MULTIPLIER
    )

    # Use waypoint_jumped to skip jump if already jumped for this waypoint
    should_jump = is_floor_transition and not waypoint_jumped

    if should_jump:
        try:
            if direction == "down":
                press(
                    Key.jump,
                    2,
                    down_time=random.uniform(0.12, 0.18),
                    up_time=random.uniform(0.05, 0.08),
                )
            elif direction == "up":
                press(
                    Key.jump,
                    1,
                    down_time=random.uniform(0.08, 0.12),
                    up_time=random.uniform(0.04, 0.06),
                )
        except Exception as e:
            log.error(f"step: Error pressing jump key: {e}")

    try:
        press(
            Key.teleport,
            1,
            down_time=random.uniform(0.1, 0.16),
            up_time=random.uniform(0.05, 0.08),
        )
    except Exception as e:
        log.error(f"step: Error pressing teleport key: {e}")

    # Delay after teleport to allow game to update player position
    # Vertical teleports need longer delay due to floor transitions
    if direction in ("up", "down"):
        time.sleep(random.uniform(0.4, 0.5))  # Longer delay for vertical movement
    else:
        time.sleep(random.uniform(0.3, 0.4))  # Shorter delay for horizontal movement


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
                teleport_hold_time = random.uniform(
                    *TimingConfig.TELEPORT["teleport_hold"]
                )
                press(Key.teleport, 1, down_time=teleport_hold_time, up_time=0.1)
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
                teleport_hold_time = random.uniform(
                    *TimingConfig.TELEPORT["teleport_hold"]
                )
                press(Key.teleport, 1, down_time=teleport_hold_time, up_time=0.02)
                press(Key.right, 1)
        else:
            # Execute action2
            if self.action2 == "attack":
                press(Key.reflection, 1)
            elif self.action2 == "teleport":
                teleport_hold_time = random.uniform(
                    *TimingConfig.TELEPORT["teleport_hold"]
                )
                press(Key.teleport, 1, down_time=teleport_hold_time, up_time=0.02)
                press(Key.up, 1)

        time.sleep(0.1)


class Face_Right(Command):
    """Tap right key briefly to ensure character faces right."""

    def __init__(self, probability=100.0):
        super().__init__(locals())
        self.probability = float(probability)

    def main(self):
        if not utils.bernoulli(self.probability / 100.0):
            return
        # Release left key if held (to avoid conflict with Move class)
        key_up(Key.left)
        press(
            Key.right,
            1,
            down_time=random.uniform(0.05, 0.1),
            up_time=random.uniform(0.05, 0.1),
        )
        time.sleep(random.uniform(0.03, 0.08))


class Face_Left(Command):
    """Tap left key briefly to ensure character faces left."""

    def __init__(self, probability=100.0):
        super().__init__(locals())
        self.probability = float(probability)

    def main(self):
        if not utils.bernoulli(self.probability / 100.0):
            return
        # Release right key if held (to avoid conflict with Move class)
        key_up(Key.right)
        press(
            Key.left,
            1,
            down_time=random.uniform(0.05, 0.1),
            up_time=random.uniform(0.05, 0.1),
        )
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


class Buff_Third(Command):
    """Casts the third buff on a randomized 27-32 minute cooldown."""

    _next_buff_time = 0.0

    def __init__(self):
        super().__init__(locals())

    def main(self):
        now = time.time()
        if Buff_Third._next_buff_time <= 0.0 or now >= Buff_Third._next_buff_time:
            press(Key.buff_third, 1)
            time.sleep(random.uniform(0.1, 0.2))
            Buff_Third._next_buff_time = now + random.uniform(1620.0, 1920.0)
            log.debug(
                "Buff Third casted, next buff in %.1f seconds",
                Buff_Third._next_buff_time - now,
            )
            return True

        remaining = Buff_Third._next_buff_time - now
        log.debug("Buff Third skipped (cooldown: %.1f seconds remaining)", remaining)
        return False
