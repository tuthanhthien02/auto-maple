"""A collection of classes used to execute a Routine."""

import math
import random
import time
from collections import namedtuple

from src.common import config, settings, utils
from src.common.anti_detect import get_human_delay, update_activity
from src.common.logger import get_action_logger, get_logger
from src.common.metrics_logger import get_metrics_logger
from src.common.vkeys import key_down, key_up, press

log = get_logger(__name__)
action_log = get_action_logger()
CommandDecision = namedtuple("CommandDecision", "command skip_reason wait_duration")


#################################
#       Routine Components      #
#################################
class Component:
    id = "Routine Component"
    PRIMITIVES = {int, str, bool, float}

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError(
                "Component superclass __init__ only accepts 1 (optional) argument: LOCALS"
            )
        if len(kwargs) != 0:
            raise TypeError(
                "Component superclass __init__ does not accept any keyword arguments"
            )
        if len(args) == 0:
            self.kwargs = {}
        elif not isinstance(args[0], dict):
            raise TypeError(
                "Component superclass __init__ only accepts arguments of type 'dict'."
            )
        else:
            self.kwargs = args[0].copy()
            self.kwargs.pop("__class__")
            self.kwargs.pop("self")

    @utils.run_if_enabled
    def execute(self):
        self.main()

    def main(self):
        pass

    def update(self, *args, **kwargs):
        """Updates this Component's constructor arguments with new arguments."""

        self.__class__(
            *args, **kwargs
        )  # Validate arguments before actually updating values
        self.__init__(*args, **kwargs)

    def info(self):
        """Returns a dictionary of useful information about this Component."""

        return {"name": self.__class__.__name__, "vars": self.kwargs.copy()}

    def encode(self):
        """Encodes an object using its ID and its __init__ arguments."""

        arr = [self.id]
        for key, value in self.kwargs.items():
            if key != "id" and type(self.kwargs[key]) in Component.PRIMITIVES:
                arr.append(f"{key}={value}")
        return ", ".join(arr)


class Point(Component):
    """Represents a location in a user-defined routine."""

    id = "*"

    def __init__(self, x, y, frequency=1, skip="False", adjust="False"):
        super().__init__(locals())
        self.x = float(x)
        self.y = float(y)
        self.location = (self.x, self.y)
        self.frequency = settings.validate_nonnegative_int(frequency)
        self.counter = int(settings.validate_boolean(skip))
        self.adjust = settings.validate_boolean(adjust)
        if not hasattr(self, "commands"):  # Updating Point should not clear commands
            self.commands = []
        # Store shuffled command order for accurate display
        self._shuffled_command_order = None  # List of command names in shuffled order
        self._shuffled_skip_flags = None  # List of skip flags for each command

    def main(self):
        """Executes the set of actions associated with this Point."""

        if self.counter == 0:
            # Reset shuffled command order when starting new execution cycle
            self._shuffled_command_order = None
            self._shuffled_skip_flags = None

            # Update activity for anti-detect
            update_activity()

            target_location = (
                config.routine.get_position_with_offset(self.location)
                if hasattr(config, "routine") and config.routine
                else self.location
            )

            # Track position offset if different from original
            if target_location != self.location:
                try:
                    get_metrics_logger().record_position_offset()
                except Exception:
                    pass

            move = config.bot.command_book["move"]
            move(*target_location).execute()
            if self.adjust:
                adjust = config.bot.command_book[
                    "adjust"
                ]  # TODO: adjust using step('up')?
                adjust(*target_location).execute()

            # Check if we're in reverse variant or floor-only variant with reverse direction
            # Skip teleport commands in routine because they're designed for normal direction
            # and will conflict with reverse movement
            current_variant = getattr(config.routine, "current_variant", "normal")
            is_reverse = current_variant == "reverse"
            is_floor_only = current_variant in ["floor1_only", "floor2_only"]
            floor_direction = getattr(config.routine, "floor_direction", "forward")
            is_floor_reverse = is_floor_only and floor_direction == "reverse"

            for decision in self._iter_commands(is_reverse, is_floor_reverse):
                if decision.skip_reason:
                    log.info(
                        "🔀 Command Sequence: Skipping command '%s' (%s)",
                        decision.command.__class__.__name__,
                        decision.skip_reason,
                    )
                    # Track command skip (only for probabilistic skips, not teleport skips)
                    if decision.skip_reason == "probabilistic skip":
                        try:
                            get_metrics_logger().record_command_skip()
                            # Update routine stats
                            if hasattr(config, "routine") and config.routine:
                                config.routine.command_sequence_stats[
                                    "total_skips"
                                ] += 1
                                config.routine.command_sequence_stats[
                                    "last_skip_time"
                                ] = time.time()
                        except Exception:
                            pass
                    continue

                if decision.wait_duration:
                    human_delay = get_human_delay(decision.wait_duration, "thinking")
                    log.debug(
                        "🔀 Command Sequence: Extra wait before '%s' (%.3fs humanized to %.3fs)",
                        decision.command.__class__.__name__,
                        decision.wait_duration,
                        human_delay,
                    )
                    time.sleep(human_delay)
                    # Track extra wait
                    try:
                        get_metrics_logger().record_extra_wait()
                        # Update routine stats
                        if hasattr(config, "routine") and config.routine:
                            config.routine.command_sequence_stats[
                                "total_extra_waits"
                            ] += 1
                            config.routine.command_sequence_stats[
                                "last_extra_wait_time"
                            ] = time.time()
                    except Exception:
                        pass

                decision.command.execute()
        self._increment_counter()

    @utils.run_if_enabled
    def _increment_counter(self):
        """Increments this Point's counter, wrapping back to 0 at the upper bound."""

        self.counter = (self.counter + 1) % self.frequency

    def _is_command_blacklisted(self, command_name, blacklist):
        """Check if a command name matches any entry in the blacklist (prefix matching, case-insensitive)."""
        if not blacklist:
            return False
        name_lower = command_name.lower()
        for blacklist_entry in blacklist:
            if name_lower.startswith(blacklist_entry.lower()):
                return True
        return False

    def get_command_order_preview(
        self, is_reverse_variant=False, is_floor_reverse=False
    ):
        """Get actual command order after shuffle (returns stored order from last execution).

        Args:
            is_reverse_variant: Unused, kept for compatibility
            is_floor_reverse: Unused, kept for compatibility
        """
        # If we have stored shuffled order, return it (this is the actual order that will be executed)
        if (
            self._shuffled_command_order is not None
            and self._shuffled_skip_flags is not None
        ):
            command_order = []
            for name, will_skip in zip(
                self._shuffled_command_order, self._shuffled_skip_flags
            ):
                if will_skip:
                    # Mark skipped commands with [SKIP]
                    command_order.append(f"{name}[SKIP]")
                else:
                    command_order.append(name)
            return command_order

        # Fallback: if no stored order, return original order (command_sequence not executed yet)
        rand_cfg = getattr(config.routine, "command_randomization", None) or {}
        enabled = rand_cfg.get("enabled", False)

        if not enabled:
            # Return original order if command_sequence is disabled
            return [cmd.__class__.__name__ for cmd in self.commands]

        # If enabled but not executed yet, return original order
        return [cmd.__class__.__name__ for cmd in self.commands]

    def _iter_commands(self, is_reverse_variant, is_floor_reverse):
        """Yield commands with randomization metadata applied."""
        commands = list(self.commands)
        rand_cfg = getattr(config.routine, "command_randomization", None) or {}
        enabled = rand_cfg.get("enabled", False)

        if enabled:
            commands = self._shuffle_commands(commands, rand_cfg)

        skip_blacklist = set(rand_cfg.get("skip_blacklist", []))
        extra_wait_probability = rand_cfg.get("extra_wait_probability", 0.0)
        skip_probability = rand_cfg.get("skip_probability", 0.0)
        wait_range = rand_cfg.get("extra_wait_range", (0.05, 0.12))

        # Store command order and skip flags for accurate display
        command_order = []
        skip_flags = []

        for command in commands:
            skip_reason = None
            wait_duration = None
            name = command.__class__.__name__

            if (is_reverse_variant or is_floor_reverse) and getattr(
                command, "direction", None
            ):
                if name.lower().startswith("teleport"):
                    skip_reason = "teleport disabled in reverse movement"

            if enabled and skip_reason is None:
                if (
                    not self._is_command_blacklisted(name, skip_blacklist)
                    and random.random() < skip_probability
                ):
                    skip_reason = "probabilistic skip"
                    log.debug(
                        "🔀 Command Sequence: Probabilistic skip triggered for '%s' (probability: %.1f%%)",
                        name,
                        skip_probability * 100,
                    )
                elif random.random() < extra_wait_probability:
                    low, high = wait_range
                    wait_duration = random.uniform(low, high)
                    log.debug(
                        "🔀 Command Sequence: Extra wait triggered for '%s' (probability: %.1f%%, duration: %.3fs)",
                        name,
                        extra_wait_probability * 100,
                        wait_duration,
                    )

            # Store command order and skip status
            command_order.append(name)
            skip_flags.append(skip_reason is not None)

            yield CommandDecision(command, skip_reason, wait_duration)

        # Save shuffled command order for display
        self._shuffled_command_order = command_order
        self._shuffled_skip_flags = skip_flags

    def _shuffle_commands(self, commands, settings):
        """Shuffle commands while respecting blacklist and probability."""
        commands = list(commands)
        if len(commands) < 2:
            return commands

        shuffle_probability = settings.get("shuffle_probability", 0.0)
        if random.random() >= shuffle_probability:
            return commands

        blacklist = set(settings.get("shuffle_blacklist", []))
        randomizable_indices = [
            idx
            for idx, cmd in enumerate(commands)
            if not self._is_command_blacklisted(cmd.__class__.__name__, blacklist)
        ]

        if len(randomizable_indices) < 2:
            return commands

        subset = [commands[idx] for idx in randomizable_indices]
        original_order = [cmd.__class__.__name__ for cmd in subset]
        random.shuffle(subset)
        shuffled_order = [cmd.__class__.__name__ for cmd in subset]

        for idx, command in zip(randomizable_indices, subset):
            commands[idx] = command

        # Log shuffle
        log.info(
            "🔀 Command Sequence: Shuffled %d commands (probability: %.1f%%) - %s → %s",
            len(subset),
            shuffle_probability * 100,
            " → ".join(original_order),
            " → ".join(shuffled_order),
        )

        # Track command shuffle
        try:
            get_metrics_logger().record_command_shuffle()
            # Update routine stats
            if hasattr(config, "routine") and config.routine:
                config.routine.command_sequence_stats["total_shuffles"] += 1
                config.routine.command_sequence_stats["last_shuffle_time"] = time.time()
        except Exception:
            pass

        return commands

    def info(self):
        curr = super().info()
        curr["vars"].pop("location", None)
        curr["vars"]["commands"] = ", ".join([c.id for c in self.commands])
        return curr

    def __str__(self):
        return f"  * {self.location}"


class Label(Component):
    id = "@"

    def __init__(self, label):
        super().__init__(locals())
        self.label = str(label)
        if self.label in config.routine.labels:
            raise ValueError
        self.links = set()
        self.index = None

    def set_index(self, i):
        self.index = i

    def encode(self):
        return "\n" + super().encode()

    def info(self):
        curr = super().info()
        curr["vars"]["index"] = self.index
        return curr

    def __delete__(self, instance):
        del self.links
        config.routine.labels.pop(self.label)

    def __str__(self):
        return f"{self.label}:"


class Jump(Component):
    """Jumps to the given Label."""

    id = ">"

    def __init__(self, label, frequency=1, skip="False"):
        super().__init__(locals())
        self.label = str(label)
        self.frequency = settings.validate_nonnegative_int(frequency)
        self.counter = int(settings.validate_boolean(skip))
        self.link = None

    def main(self):
        if self.link is None:
            log.error("Label '%s' does not exist", self.label)
        else:
            if self.counter == 0:
                config.routine.index = self.link.index
            self._increment_counter()

    @utils.run_if_enabled
    def _increment_counter(self):
        self.counter = (self.counter + 1) % self.frequency

    def bind(self):
        """
        Binds this Goto to its corresponding Label. If the Label's index changes, this Goto
        instance will automatically be able to access the updated value.
        :return:    Whether the binding was successful
        """

        if self.label in config.routine.labels:
            self.link = config.routine.labels[self.label]
            self.link.links.add(self)
            return True
        return False

    def __delete__(self, instance):
        if self.link is not None:
            self.link.links.remove(self)

    def __str__(self):
        return f"  > {self.label}"


class Setting(Component):
    """Changes the value of the given setting variable."""

    id = "$"

    def __init__(self, target, value):
        super().__init__(locals())
        self.key = str(target)
        if self.key not in settings.SETTING_VALIDATORS:
            raise ValueError(f"Setting '{target}' does not exist")
        self.value = settings.SETTING_VALIDATORS[self.key](value)

    def main(self):
        setattr(settings, self.key, self.value)

    def __str__(self):
        return f"  $ {self.key} = {self.value}"


SYMBOLS = {"*": Point, "@": Label, ">": Jump, "$": Setting}


#############################
#       Shared Commands     #
#############################
class Command(Component):
    id = "Command Superclass"

    def __init__(self, *args):
        super().__init__(*args)
        self.id = self.__class__.__name__

    def __str__(self):
        variables = self.__dict__
        result = "    " + self.id
        if len(variables) - 1 > 0:
            result += ":"
        for key, value in variables.items():
            if key != "id":
                result += f"\n        {key}={value}"
        return result


class Move(Command):
    """Moves to a given position using the shortest path based on the current Layout."""

    def __init__(self, x, y, max_steps=15):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)
        self.prev_direction = ""
        # Teleport configuration for skip context
        self.teleport_threshold = 0.05  # Distance threshold for teleport (when skipping or reverse) - reduced for better skip teleport
        self.teleport_probability = (
            1.0  # 100% chance to teleport if distance > threshold (normal and reverse)
        )

    def _new_direction(self, new):
        try:
            key_down(new)
            if self.prev_direction and self.prev_direction != new:
                key_up(self.prev_direction)
            self.prev_direction = new
        except Exception:
            # Ensure key is released if error occurs
            if self.prev_direction:
                key_up(self.prev_direction)
            raise

    def _teleport_to_target(self, reverse_direction=False):
        """Teleport to target using Luminous teleport command when distance is far.

        Args:
            reverse_direction: If True, reverse the calculated direction (for reverse movement).
        """
        try:
            # Get command book to access Teleport command
            # CommandBook uses dict and __getitem__, not get() method
            if "teleport" not in config.bot.command_book:
                action_log.warning(
                    "Move: Teleport command not found in command book, falling back to walk"
                )
                return False

            teleport_cmd_class = config.bot.command_book["teleport"]

            # Calculate direction based on target position
            d_x = self.target[0] - config.player_pos[0]
            d_y = self.target[1] - config.player_pos[1]

            # Determine primary direction (horizontal or vertical)
            if abs(d_x) > abs(d_y):
                # Horizontal movement
                direction = "right" if d_x > 0 else "left"
            else:
                # Vertical movement
                direction = "down" if d_y > 0 else "up"

            original_direction = direction  # Store original for logging

            # Reverse direction if needed (for reverse movement)
            if reverse_direction:
                if direction == "right":
                    direction = "left"
                elif direction == "left":
                    direction = "right"
                elif direction == "up":
                    direction = "down"
                elif direction == "down":
                    direction = "up"
                action_log.debug(
                    "Move: Reversed teleport direction from '%s' to '%s' (reverse_direction=True)",
                    original_direction,
                    direction,
                )

            # Calculate number of teleports needed (rough estimate)
            distance = utils.distance(config.player_pos, self.target)
            # Estimate: each teleport covers ~0.05-0.08 distance
            teleport_distance = 0.06
            num_teleports = max(1, int(distance / teleport_distance))
            # Limit max teleports to avoid overshooting
            num_teleports = min(num_teleports, 3)

            # Execute teleport command
            direction_label = (
                f"{direction} (reversed)"
                if reverse_direction and original_direction != direction
                else direction
            )
            action_log.info(
                "🚀 Move: Teleporting %s %d times (distance: %.3f, threshold: %.3f, reverse_direction=%s)",
                direction_label,
                num_teleports,
                distance,
                self.teleport_threshold,
                reverse_direction,
            )
            teleport_cmd_instance = teleport_cmd_class(direction, num_teleports)
            teleport_cmd_instance.execute()

            # Wait for teleport to complete (longer for vertical teleports / floor changes)
            is_vertical_direction = direction in ("up", "down")
            if is_vertical_direction:
                action_log.debug(
                    "Move: Vertical teleport start (player_y=%.3f → target_y=%.3f, distance=%.3f, reverse=%s)",
                    config.player_pos[1],
                    self.target[1],
                    distance,
                    reverse_direction,
                )
                settle_delay = random.uniform(0.4, 0.6)
                action_log.debug(
                    "Move: Vertical teleport settle delay %.3fs (direction=%s, num_teleports=%d)",
                    settle_delay,
                    direction,
                    num_teleports,
                )
                time.sleep(settle_delay)
                # Poll player position to ensure floor transition completed
                initial_position = tuple(config.player_pos)
                waited = 0.0
                max_wait = 1.0
                position_delta = 0.0
                while waited < max_wait:
                    time.sleep(0.1)
                    waited += 0.1
                    position_delta = utils.distance(
                        tuple(config.player_pos), initial_position
                    )
                    if position_delta > 0.05:
                        break
                if position_delta > 0.05:
                    action_log.debug(
                        "Move: Floor transition confirmed (delta=%.3f after %.2fs)",
                        position_delta,
                        waited,
                    )
                else:
                    action_log.debug(
                        "Move: Floor transition not confirmed after %.2fs (delta=%.3f) – continuing",
                        waited,
                        position_delta,
                    )
            else:
                time.sleep(0.2)

            # Check if we're close enough to target
            remaining_distance = utils.distance(config.player_pos, self.target)
            if remaining_distance > settings.move_tolerance:
                # Still need to adjust, but teleport got us closer
                action_log.debug(
                    "Move: Teleport completed, remaining distance: %.3f",
                    remaining_distance,
                )

            return True
        except Exception as e:
            action_log.warning(
                "Move: Error during teleport: %s, falling back to walk", e
            )
            return False

    def main(self):
        # Calculate distance to target
        distance = utils.distance(config.player_pos, self.target)

        # NOTE: Auto-jump for floor transitions is handled by:
        # 1. Adjust class (when adjust=True) - handles Y adjustment including floor transitions
        # 2. step() function (when direction is vertical) - handles large Y changes during movement
        # Move class does NOT auto-jump to avoid duplicate jumps

        # Check if we should teleport (when skipping, backwarding, or reverse and distance is far)
        is_skipping = getattr(config.routine, "is_skipping_context", False)
        is_backwarding = getattr(config.routine, "is_backwarding_context", False)

        # Check if we're in reverse variant or floor-only variant with reverse direction
        current_variant = getattr(config.routine, "current_variant", "normal")
        is_reverse = current_variant == "reverse"
        is_floor_only = current_variant in ["floor1_only", "floor2_only"]
        floor_direction = getattr(config.routine, "floor_direction", "forward")
        is_floor_reverse = is_floor_only and floor_direction == "reverse"

        # Use teleport in reverse variant, floor-only variant with reverse direction, skipping, or backwarding when distance is large
        should_use_teleport = (
            is_skipping
            or is_backwarding
            or (is_reverse and distance > self.teleport_threshold)
            or (is_floor_reverse and distance > self.teleport_threshold)
        )

        if should_use_teleport and distance > self.teleport_threshold:
            # Always teleport when distance > threshold (100% chance for both normal and reverse)
            # For floor-only reverse movement: Direction is already calculated correctly based on actual position
            # (e.g., moving from right to left = "left" direction). Do NOT reverse direction.
            # For normal reverse variant: Always reverse direction.
            reverse_teleport = False
            if is_reverse:
                # Normal reverse variant: always reverse direction
                reverse_teleport = True
            elif is_floor_reverse:
                # Floor reverse: Direction is already correct (calculated from actual position movement)
                # Do NOT reverse direction - the calculated direction (left/right) is already correct for reverse movement
                reverse_teleport = False
            if self._teleport_to_target(reverse_direction=reverse_teleport):
                # Teleport successful, check if we need to adjust
                remaining_distance = utils.distance(config.player_pos, self.target)
                if remaining_distance > settings.move_tolerance:
                    # Still need to walk a bit to reach exact target
                    # Continue with walk logic for fine adjustment
                    pass
                else:
                    # Close enough, no need to walk
                    return
            else:
                # Teleport failed, fall through to walk
                pass
        elif should_use_teleport:
            # Should teleport but distance is close, walk normally
            pass
        else:
            # Not skipping and not reverse, walk normally
            pass

        # Normal walk logic with human-like movement characteristics
        counter = self.max_steps
        path = config.layout.shortest_path(config.player_pos, self.target)
        total_distance = max(distance, settings.move_tolerance * 2)

        for i, waypoint in enumerate(path):
            is_last_waypoint = i == len(path) - 1
            target_stage = self._apply_waypoint_jitter(
                waypoint, allow_jitter=not is_last_waypoint
            )
            self.prev_direction = ""
            # Track if we've already jumped for this waypoint to prevent duplicate jumps
            waypoint_jumped = False

            local_error = utils.distance(config.player_pos, target_stage)
            global_error = utils.distance(config.player_pos, self.target)

            while (
                config.enabled
                and counter > 0
                and local_error > settings.move_tolerance
                and global_error > settings.move_tolerance
            ):
                d_x = target_stage[0] - config.player_pos[0]
                d_y = target_stage[1] - config.player_pos[1]

                if abs(d_x) >= abs(d_y):
                    key = "right" if d_x > 0 else "left"
                    base_delay = 0.12
                else:
                    key = "down" if d_y > 0 else "up"
                    base_delay = 0.06

                self._new_direction(key)
                self._maybe_apply_micro_gesture(key)
                # Pass distance to step() for distance-based movement (hold vs press)
                # Also pass waypoint_jumped flag to prevent duplicate jumps
                step(
                    key,
                    target_stage,
                    distance=local_error,
                    waypoint_jumped=waypoint_jumped,
                )
                # Mark as jumped if this was a vertical movement with large Y change
                if key in ("up", "down") and abs(d_y) > settings.move_tolerance * 1.5:
                    waypoint_jumped = True

                if settings.record_layout:
                    config.layout.add(*config.player_pos)

                counter -= 1
                progress = 1.0 - min(
                    1.0, utils.distance(config.player_pos, self.target) / total_distance
                )
                move_delay = self._compute_axis_delay(base_delay, progress)
                time.sleep(move_delay)

                if random.random() < 0.12:
                    self._maybe_apply_micro_pause(progress)

                # Small delay to allow position update from capture thread (prevent step-over)
                # This ensures config.player_pos is updated before next check
                time.sleep(
                    0.05
                )  # 50ms delay to sync with position update (0.05s interval when active)

                local_error = utils.distance(config.player_pos, target_stage)
                global_error = utils.distance(config.player_pos, self.target)

            if self.prev_direction:
                key_up(self.prev_direction)
                self.prev_direction = ""

            if (
                not config.enabled
                or utils.distance(config.player_pos, self.target)
                <= settings.move_tolerance
            ):
                break

    def _apply_waypoint_jitter(self, waypoint, allow_jitter=True):
        """Apply subtle jitter to the waypoint to avoid rigid straight lines."""
        if not allow_jitter:
            return waypoint

        jitter_range = 0.006
        jitter_x = random.uniform(-jitter_range, jitter_range)
        jitter_y = random.uniform(-jitter_range, jitter_range)
        return (waypoint[0] + jitter_x, waypoint[1] + jitter_y)

    def _compute_axis_delay(self, base_delay, progress):
        """Compute axis-specific delay with easing-based acceleration/deceleration."""
        progress = max(0.0, min(progress, 1.0))
        eased = 0.5 - 0.5 * math.cos(progress * math.pi)  # Smoothstep-like easing
        multiplier = 0.7 + 0.5 * eased
        return get_human_delay(base_delay * multiplier, "normal")

    def _maybe_apply_micro_pause(self, progress):
        """Occasionally apply a micro pause to simulate human adjustments."""
        progress = max(0.0, min(progress, 1.0))
        if random.random() >= 0.2:
            return
        pause_duration = 0.025 + 0.045 * progress
        time.sleep(get_human_delay(pause_duration, "thinking"))
        if hasattr(config, "routine") and hasattr(
            config.routine, "observability_metrics"
        ):
            config.routine.observability_metrics["micro_pauses"] += 1

    def _maybe_apply_micro_gesture(self, current_direction):
        """Inject a short counter-movement to mimic human adjustment."""
        routine = getattr(config, "routine", None)
        if not routine:
            return
        cfg = getattr(routine, "micro_gesture_config", {})
        if not cfg.get("enabled"):
            return
        chance = cfg.get("mirror_chance", 0.0)
        roll = random.random()
        if roll >= chance:
            return
        opposite = self._opposite_direction(current_direction)
        if not opposite:
            return
        duration_low, duration_high = cfg.get("duration_range", (0.02, 0.05))
        duration = random.uniform(
            min(duration_low, duration_high), max(duration_low, duration_high)
        )
        if getattr(routine, "movement_logging_enabled", False):
            log.info(
                "MicroGesture: roll=%.3f <= chance=%.3f ⇒ mirror '%s' for %.3fs (range %.3f–%.3f)",
                roll,
                chance,
                opposite,
                duration,
                min(duration_low, duration_high),
                max(duration_low, duration_high),
            )
        action_log.debug("Move: Micro gesture %s for %.3fs", opposite, duration)
        try:
            key_down(opposite)
            time.sleep(duration)
        finally:
            key_up(opposite)
        routine.observability_metrics["micro_gestures"] += 1
        # Track micro gesture in metrics
        try:
            get_metrics_logger().record_micro_gesture()
        except Exception:
            pass

    @staticmethod
    def _opposite_direction(direction):
        mapping = {"left": "right", "right": "left", "up": "down", "down": "up"}
        return mapping.get(direction)


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)


def step(direction, target, distance=None, waypoint_jumped=False):
    """
    The default 'step' function. If not overridden, immediately stops the bot.
    :param direction:   The direction in which to move.
    :param target:      The target location to step towards.
    :param distance:    Optional distance to target. Used for distance-based movement decisions.
    :param waypoint_jumped: If True, skip auto-jump to prevent duplicate jumps for same waypoint.
    :return:            None
    """

    log.error(
        "Function 'step' not implemented in current command book, aborting process."
    )
    config.enabled = False


class Wait(Command):
    """Waits for a set amount of time."""

    def __init__(self, duration):
        super().__init__(locals())
        self.duration = float(duration)

    def main(self):
        # Use human-like delay instead of fixed sleep
        human_delay = get_human_delay(self.duration, "normal")
        action_log.debug(
            "wait(duration=%.3f) -> human_delay=%.3f", self.duration, human_delay
        )
        time.sleep(human_delay)


class Wait_Random(Command):
    """Waits for a random amount of time within a specified range."""

    def __init__(self, min_duration, max_duration):
        super().__init__(locals())
        self.min_duration = float(min_duration)
        self.max_duration = float(max_duration)

        # Validate range
        if self.min_duration > self.max_duration:
            self.min_duration, self.max_duration = self.max_duration, self.min_duration

    def main(self):
        # Generate random duration within range
        random_duration = random.uniform(self.min_duration, self.max_duration)

        # Use human-like delay for the random duration
        human_delay = get_human_delay(random_duration, "normal")
        action_log.debug(
            "wait_random(%.3f, %.3f) -> sampled=%.3f, human_delay=%.3f",
            self.min_duration,
            self.max_duration,
            random_duration,
            human_delay,
        )
        time.sleep(human_delay)


class Walk(Command):
    """Walks in the given direction for a set amount of time."""

    def __init__(self, direction, duration):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.duration = float(duration)

    def main(self):
        key_down(self.direction)
        # Use human-like delay instead of fixed sleep
        human_delay = get_human_delay(self.duration, "normal")
        time.sleep(human_delay)
        key_up(self.direction)
        # Use human-like delay for post-walk pause
        post_delay = get_human_delay(0.05, "fast")
        time.sleep(post_delay)


class Fall(Command):
    """
    Performs a down-jump and then free-falls until the player exceeds a given distance
    from their starting position.
    """

    def __init__(self, distance=settings.move_tolerance / 2):
        super().__init__(locals())
        self.distance = float(distance)

    def main(self):
        start = config.player_pos
        key_down("down")
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.5):
            time.sleep(utils.rand_float(0.2, 0.4))
        counter = 6
        while (
            config.enabled
            and counter > 0
            and utils.distance(start, config.player_pos) < self.distance
        ):
            press("space", 1, down_time=0.1)
            counter -= 1
        key_up("down")
        time.sleep(0.05)


class Buff(Command):
    """Undefined 'buff' command for the default command book."""

    def main(self):
        log.error(
            "'Buff' command not implemented in current command book, aborting process."
        )
        config.enabled = False
