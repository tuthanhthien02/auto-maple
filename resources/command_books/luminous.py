"""Command book for Luminous class."""

from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up
from src.common import config, utils, settings
from src.common.logger import get_logger
import time
import random
import math

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
        "hold_threshold_multiplier": 3.0,  # Multiplier for move_tolerance to determine hold vs press
        # Distance > (move_tolerance * multiplier) → hold key (xa)
        # Distance ≤ (move_tolerance * multiplier) → press key (gần)
        # Có thể chỉnh multiplier này nếu test thực tế không work:
        # - Tăng multiplier (vd: 4.0, 5.0) → nhiều trường hợp dùng press key hơn
        # - Giảm multiplier (vd: 2.0, 2.5) → nhiều trường hợp dùng hold key hơn
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
    """Mix skills per call: 85% Reflection (2–3 casts), 10% Apocalypse (2–3 casts), 5% Death Scythe (1 cast)."""

    def __init__(self, min_times=2, max_times=3):
        super().__init__(locals())
        self.min_times = int(min_times)
        self.max_times = int(max_times)

    def main(self):
        roll = random.random()
        if roll < 0.85:
            min_casts = max(2, self.min_times)
            max_casts = max(3, self.max_times)
            times = random.randint(min_casts, max_casts)
            for _ in range(times):
                press(Key.reflection, 1, down_time=0.1, up_time=0.1)
                time.sleep(
                    random.uniform(*TimingConfig.REFLECTION["long_between_casts"])
                )
        elif roll < 0.95:
            times = random.randint(2, 3)
            for _ in range(times):
                press(Key.apocalypse, 1, down_time=0.1, up_time=0.1)
                time.sleep(random.uniform(*TimingConfig.HEAVY["long_between_casts"]))
            time.sleep(random.uniform(*TimingConfig.HEAVY["between_actions"]))
        else:
            press(Key.death_scythe, 1, down_time=0.1, up_time=0.1)
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


class Dark_Reflection(Command):
    """Dark Reflection skill."""

    def main(self):
        press(Key.dark_reflection, 1, down_time=0.1, up_time=0.1)
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
                # Random delay between combos
                if i < self.times - 1:
                    time.sleep(random.uniform(*TimingConfig.TELEPORT["combo_delay"]))


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


class Jump(Command):
    """Jump - Press ALT key."""

    def __init__(self, times=1):
        super().__init__(locals())
        self.times = int(times)

    def main(self):
        # Simple jump - just press ALT key
        for i in range(self.times):
            press(Key.jump, 1, down_time=0.1, up_time=0.1)
            # Small delay between jumps
            if i < self.times - 1:
                time.sleep(0.1)  # 100ms between jumps


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

    def __init__(self):
        super().__init__(locals())
        self.next_buff_time = 0.0

    def main(self):
        now = time.time()
        # Random hóa thời gian buff: 120–170 giây (thay vì cố định 180s)
        if self.next_buff_time == 0.0 or now >= self.next_buff_time:
            press(Key.buff_main, 1)
            time.sleep(0.1)
            # Temporarily disable secondary buff per request
            # press(Key.buff_secondary, 1)
            # time.sleep(0.1)
            # Nghỉ ngẫu nhiên 2–4 giây sau khi buff để anti-detect
            time.sleep(random.uniform(2.0, 4.0))
            # Lên lịch lần buff tiếp theo
            self.next_buff_time = now + random.uniform(120.0, 170.0)


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
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        # Use Luminous teleport up
                        Teleport("up").main()
                    else:
                        # Use Luminous jump down - FIXED: Use Jump_Down class instead of manual press
                        Jump_Down(
                            1
                        ).main()  # Use existing Jump_Down class with proper timing
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle

        # Safety: ensure all movement keys are released
        key_up("left")
        key_up("right")
        key_up("up")
        key_up("down")


def step(direction, target, distance=None):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    Based on Kanna's intelligent step() with Luminous improvements.

    :param direction: Direction to move ('left', 'right', 'up', 'down')
    :param target: Target location
    :param distance: Optional distance to target. If None, will be calculated.
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

    # Check Y distance for vertical movements (from Kanna - SMART!)
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == "down":
            press(Key.jump, 3)
        elif direction == "up":
            press(Key.jump, 1)

    # Handle different directions (hybrid approach)
    if direction in ("left", "right"):
        # Horizontal movement - Distance-based: Hold (xa) vs Press (gần)
        direction_key = getattr(Key, direction)

        if distance > hold_threshold:
            # Distance xa → Hold key với random timing (human-like)
            log.debug(
                "🚶 Human-like: distance xa (%.3f > %.3f) → hold key %s",
                distance,
                hold_threshold,
                direction,
            )
            try:
                key_down(direction_key)
                time.sleep(random.uniform(0.08, 0.15))
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
        try:
            # Hold direction key FIRST with random timing (like Teleport class)
            key_down(direction_key)
            time.sleep(random.uniform(*TimingConfig.TELEPORT["direction_delay"]))

            if direction in ("up", "down"):
                # Vertical teleport: Hold direction + Press ALT + Press W
                key_down(Key.jump)
                time.sleep(random.uniform(*TimingConfig.TELEPORT["vertical_jump_hold"]))
                key_up(Key.jump)
                time.sleep(
                    random.uniform(*TimingConfig.TELEPORT["vertical_jump_release"])
                )

                num_presses = 1  # Vertical = 1 press
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

    def __init__(self):
        super().__init__(locals())
        self.next_buff_time = 0.0

    def main(self):
        now = time.time()
        if self.next_buff_time == 0.0 or now >= self.next_buff_time:
            press(Key.buff_secondary, 1)
            time.sleep(random.uniform(0.1, 0.2))
            self.next_buff_time = now + random.uniform(800.0, 900.0)
