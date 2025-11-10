"""A collection of classes used to execute a Routine."""

import math
import time
import random
from src.common import config, settings, utils
from src.common.vkeys import key_down, key_up, press, press_with_behavioral_pause
from src.common.anti_detect import get_human_delay, update_activity
from src.common.logger import get_logger, get_action_logger
log = get_logger(__name__)
action_log = get_action_logger()


#################################
#       Routine Components      #
#################################
class Component:
    id = 'Routine Component'
    PRIMITIVES = {int, str, bool, float}

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError('Component superclass __init__ only accepts 1 (optional) argument: LOCALS')
        if len(kwargs) != 0:
            raise TypeError('Component superclass __init__ does not accept any keyword arguments')
        if len(args) == 0:
            self.kwargs = {}
        elif type(args[0]) != dict:
            raise TypeError("Component superclass __init__ only accepts arguments of type 'dict'.")
        else:
            self.kwargs = args[0].copy()
            self.kwargs.pop('__class__')
            self.kwargs.pop('self')

    @utils.run_if_enabled
    def execute(self):
        self.main()

    def main(self):
        pass

    def update(self, *args, **kwargs):
        """Updates this Component's constructor arguments with new arguments."""

        self.__class__(*args, **kwargs)     # Validate arguments before actually updating values
        self.__init__(*args, **kwargs)

    def info(self):
        """Returns a dictionary of useful information about this Component."""

        return {
            'name': self.__class__.__name__,
            'vars': self.kwargs.copy()
        }

    def encode(self):
        """Encodes an object using its ID and its __init__ arguments."""

        arr = [self.id]
        for key, value in self.kwargs.items():
            if key != 'id' and type(self.kwargs[key]) in Component.PRIMITIVES:
                arr.append(f'{key}={value}')
        return ', '.join(arr)


class Point(Component):
    """Represents a location in a user-defined routine."""

    id = '*'

    def __init__(self, x, y, frequency=1, skip='False', adjust='False'):
        super().__init__(locals())
        self.x = float(x)
        self.y = float(y)
        self.location = (self.x, self.y)
        self.frequency = settings.validate_nonnegative_int(frequency)
        self.counter = int(settings.validate_boolean(skip))
        self.adjust = settings.validate_boolean(adjust)
        if not hasattr(self, 'commands'):       # Updating Point should not clear commands
            self.commands = []

    def main(self):
        """Executes the set of actions associated with this Point."""

        if self.counter == 0:
            # Update activity for anti-detect
            update_activity()
            
            move = config.bot.command_book['move']
            move(*self.location).execute()
            if self.adjust:
                adjust = config.bot.command_book['adjust']      # TODO: adjust using step('up')?
                adjust(*self.location).execute()
            
            # Check if we're in reverse variant - skip teleport commands in routine
            # because they're designed for normal direction and will conflict with reverse movement
            is_reverse = getattr(config.routine, 'current_variant', 'normal') == 'reverse'
            
            for command in self.commands:
                # Skip teleport commands in reverse variant (they're designed for normal direction)
                if is_reverse and hasattr(command, 'direction'):
                    # Check if it's a Teleport command
                    if command.__class__.__name__ == 'Teleport':
                        log.debug("Point: Skipping teleport command '%s' in reverse variant (designed for normal direction)", 
                                 command.direction)
                        continue
                command.execute()
        self._increment_counter()

    @utils.run_if_enabled
    def _increment_counter(self):
        """Increments this Point's counter, wrapping back to 0 at the upper bound."""

        self.counter = (self.counter + 1) % self.frequency

    def info(self):
        curr = super().info()
        curr['vars'].pop('location', None)
        curr['vars']['commands'] = ', '.join([c.id for c in self.commands])
        return curr

    def __str__(self):
        return f'  * {self.location}'


class Label(Component):
    id = '@'

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
        return '\n' + super().encode()

    def info(self):
        curr = super().info()
        curr['vars']['index'] = self.index
        return curr

    def __delete__(self, instance):
        del self.links
        config.routine.labels.pop(self.label)

    def __str__(self):
        return f'{self.label}:'


class Jump(Component):
    """Jumps to the given Label."""

    id = '>'

    def __init__(self, label, frequency=1, skip='False'):
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
        return f'  > {self.label}'


class Setting(Component):
    """Changes the value of the given setting variable."""

    id = '$'

    def __init__(self, target, value):
        super().__init__(locals())
        self.key = str(target)
        if self.key not in settings.SETTING_VALIDATORS:
            raise ValueError(f"Setting '{target}' does not exist")
        self.value = settings.SETTING_VALIDATORS[self.key](value)

    def main(self):
        setattr(settings, self.key, self.value)

    def __str__(self):
        return f'  $ {self.key} = {self.value}'


SYMBOLS = {
    '*': Point,
    '@': Label,
    '>': Jump,
    '$': Setting
}


#############################
#       Shared Commands     #
#############################
class Command(Component):
    id = 'Command Superclass'

    def __init__(self, *args):
        super().__init__(*args)
        self.id = self.__class__.__name__

    def __str__(self):
        variables = self.__dict__
        result = '    ' + self.id
        if len(variables) - 1 > 0:
            result += ':'
        for key, value in variables.items():
            if key != 'id':
                result += f'\n        {key}={value}'
        return result


class Move(Command):
    """Moves to a given position using the shortest path based on the current Layout."""

    def __init__(self, x, y, max_steps=15):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)
        self.prev_direction = ''
        # Teleport configuration for skip context
        self.teleport_threshold = 0.05  # Distance threshold for teleport (when skipping or reverse) - reduced for better skip teleport
        self.teleport_probability = 1.0  # 100% chance to teleport if distance > threshold (normal and reverse)

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

    def _teleport_to_target(self):
        """Teleport to target using Luminous teleport command when distance is far."""
        try:
            # Get command book to access Teleport command
            # CommandBook uses dict and __getitem__, not get() method
            if 'teleport' not in config.bot.command_book:
                action_log.warning("Move: Teleport command not found in command book, falling back to walk")
                return False
            
            teleport_cmd_class = config.bot.command_book['teleport']
            
            # Calculate direction based on target position
            d_x = self.target[0] - config.player_pos[0]
            d_y = self.target[1] - config.player_pos[1]
            
            # Determine primary direction (horizontal or vertical)
            if abs(d_x) > abs(d_y):
                # Horizontal movement
                direction = 'right' if d_x > 0 else 'left'
            else:
                # Vertical movement
                direction = 'down' if d_y > 0 else 'up'
            
            # Calculate number of teleports needed (rough estimate)
            distance = utils.distance(config.player_pos, self.target)
            # Estimate: each teleport covers ~0.05-0.08 distance
            teleport_distance = 0.06
            num_teleports = max(1, int(distance / teleport_distance))
            # Limit max teleports to avoid overshooting
            num_teleports = min(num_teleports, 3)
            
            # Execute teleport command
            action_log.info("🚀 Move: Teleporting %s %d times (distance: %.3f, threshold: %.3f)", 
                           direction, num_teleports, distance, self.teleport_threshold)
            teleport_cmd_instance = teleport_cmd_class(direction, num_teleports)
            teleport_cmd_instance.execute()
            
            # Wait for teleport to complete
            time.sleep(0.2)
            
            # Check if we're close enough to target
            remaining_distance = utils.distance(config.player_pos, self.target)
            if remaining_distance > settings.move_tolerance:
                # Still need to adjust, but teleport got us closer
                action_log.debug("Move: Teleport completed, remaining distance: %.3f", remaining_distance)
            
            return True
        except Exception as e:
            action_log.warning("Move: Error during teleport: %s, falling back to walk", e)
            return False

    def main(self):
        # Calculate distance to target
        distance = utils.distance(config.player_pos, self.target)
        
        # Check if we should teleport (when skipping and distance is far)
        is_skipping = getattr(config.routine, 'is_skipping_context', False)
        
        # Check if we're in reverse variant (for better movement in reverse)
        is_reverse = getattr(config.routine, 'current_variant', 'normal') == 'reverse'
        # Use teleport in reverse variant when distance is large (similar to skipping)
        should_use_teleport = is_skipping or (is_reverse and distance > self.teleport_threshold)
        
        # Log move decision (always log for observation)
        action_log.info("📍 Move: Target (%.3f, %.3f), Distance: %.3f, Threshold: %.3f, Skipping: %s, Reverse: %s", 
                       self.target[0], self.target[1], distance, self.teleport_threshold, is_skipping, is_reverse)
        
        if should_use_teleport and distance > self.teleport_threshold:
            # Always teleport when distance > threshold (100% chance for both normal and reverse)
            reason = "reverse variant" if is_reverse else "skipping"
            action_log.info("🚀 Move: Attempting teleport (distance: %.3f > threshold: %.3f, reason: %s, chance: 100%%)", 
                           distance, self.teleport_threshold, reason)
            if self._teleport_to_target():
                # Teleport successful, check if we need to adjust
                remaining_distance = utils.distance(config.player_pos, self.target)
                if remaining_distance > settings.move_tolerance:
                    # Still need to walk a bit to reach exact target
                    action_log.info("🚶 Move: Adjusting position after teleport (remaining: %.3f)", 
                                   remaining_distance)
                    # Continue with walk logic for fine adjustment
                else:
                    # Close enough, no need to walk
                    action_log.info("✅ Move: Teleport successful, reached target")
                    return
            else:
                # Teleport failed, fall through to walk
                action_log.warning("⚠️ Move: Teleport failed, falling back to walk")
        elif should_use_teleport:
            # Should teleport but distance is close, walk normally
            reason = "reverse variant" if is_reverse else "skipping"
            action_log.info("🚶 Move: %s but distance is close (%.3f <= %.3f), walking", 
                           reason, distance, self.teleport_threshold)
        else:
            # Not skipping and not reverse, walk normally
            action_log.info("🚶 Move: Normal walk (distance: %.3f, skipping: %s, reverse: %s)", 
                           distance, is_skipping, is_reverse)
        
        # Normal walk logic (pathfinding + press key direction)
        counter = self.max_steps
        path = config.layout.shortest_path(config.player_pos, self.target)
        for i, point in enumerate(path):
            toggle = True
            self.prev_direction = ''
            local_error = utils.distance(config.player_pos, point)
            global_error = utils.distance(config.player_pos, self.target)
            while config.enabled and counter > 0 and \
                    local_error > settings.move_tolerance and \
                    global_error > settings.move_tolerance:
                if toggle:
                    d_x = point[0] - config.player_pos[0]
                    if abs(d_x) > settings.move_tolerance / math.sqrt(2):
                        if d_x < 0:
                            key = 'left'
                        else:
                            key = 'right'
                        self._new_direction(key)
                        step(key, point)
                        if settings.record_layout:
                            config.layout.add(*config.player_pos)
                        counter -= 1
                        if i < len(path) - 1:
                            # Use human-like delay instead of fixed delay
                            delay = get_human_delay(0.15, 'normal')
                            time.sleep(delay)
                else:
                    d_y = point[1] - config.player_pos[1]
                    if abs(d_y) > settings.move_tolerance / math.sqrt(2):
                        if d_y < 0:
                            key = 'up'
                        else:
                            key = 'down'
                        self._new_direction(key)
                        step(key, point)
                        if settings.record_layout:
                            config.layout.add(*config.player_pos)
                        counter -= 1
                        if i < len(path) - 1:
                            # Use human-like delay instead of fixed delay
                            delay = get_human_delay(0.05, 'fast')
                            time.sleep(delay)
                local_error = utils.distance(config.player_pos, point)
                global_error = utils.distance(config.player_pos, self.target)
                toggle = not toggle
            if self.prev_direction:
                key_up(self.prev_direction)


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)


def step(direction, target):
    """
    The default 'step' function. If not overridden, immediately stops the bot.
    :param direction:   The direction in which to move.
    :param target:      The target location to step towards.
    :return:            None
    """

    log.error("Function 'step' not implemented in current command book, aborting process.")
    config.enabled = False


class Wait(Command):
    """Waits for a set amount of time."""

    def __init__(self, duration):
        super().__init__(locals())
        self.duration = float(duration)

    def main(self):
        # Use human-like delay instead of fixed sleep
        human_delay = get_human_delay(self.duration, 'normal')
        action_log.debug("wait(duration=%.3f) -> human_delay=%.3f", self.duration, human_delay)
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
        import random
        random_duration = random.uniform(self.min_duration, self.max_duration)
        
        # Use human-like delay for the random duration
        human_delay = get_human_delay(random_duration, 'normal')
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
        human_delay = get_human_delay(self.duration, 'normal')
        time.sleep(human_delay)
        key_up(self.direction)
        # Use human-like delay for post-walk pause
        post_delay = get_human_delay(0.05, 'fast')
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
        key_down('down')
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.5):
            time.sleep(utils.rand_float(0.2, 0.4))
        counter = 6
        while config.enabled and \
                counter > 0 and \
                utils.distance(start, config.player_pos) < self.distance:
            press('space', 1, down_time=0.1)
            counter -= 1
        key_up('down')
        time.sleep(0.05)


class Buff(Command):
    """Undefined 'buff' command for the default command book."""

    def main(self):
        log.error("'Buff' command not implemented in current command book, aborting process.")
        config.enabled = False
