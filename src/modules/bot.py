"""An interpreter that reads and executes user-created routines."""

import threading
import time
import git
import cv2
from src.common import config, utils
from src.common.anti_detect import initialize_anti_detect, update_activity

# Routine randomization - DISABLED
# from src.common.routine_randomization import initialize_routine_randomization, get_variant_start_index
from src.common.process_stealth import enable_process_stealth
from src.detection import detection
from src.routine.routine import Routine
from src.command_book.command_book import CommandBook
from src.routine.components import Point
from src.common.vkeys import press, click
from src.common.interfaces import Configurable
from src.common.logger import get_logger
from src.common.metrics_logger import get_metrics_logger


# The rune's buff icon
RUNE_BUFF_TEMPLATE = cv2.imread(
    utils.get_asset_path("assets/rune_buff_template.jpg"), 0
)


log = get_logger(__name__)


class Bot(Configurable):
    """A class that interprets and executes user-defined routines."""

    DEFAULT_CONFIG = {"Interact": "y", "Feed pet": "9"}

    def __init__(self):
        """Loads a user-defined routine on start up and initializes this Bot's main thread."""

        super().__init__("keybindings")
        config.bot = self

        self.rune_active = False
        self.rune_pos = (0, 0)
        self.rune_closest_pos = (0, 0)  # Location of the Point closest to rune
        self.submodules = []
        self.command_book = None  # CommandBook instance
        # self.module_name = None
        # self.buff = components.Buff()

        # self.command_book = {}
        # for c in (components.Wait, components.Walk, components.Fall,
        #           components.Move, components.Adjust, components.Buff):
        #     self.command_book[c.__name__.lower()] = c

        config.routine = Routine()

        self.ready = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

    def start(self):
        """
        Starts this Bot object's thread.
        :return:    None
        """

        # Initialize anti-detect features
        initialize_anti_detect()

        # Routine randomization - DISABLED
        # initialize_routine_randomization()

        # Enable process stealth (optional)
        try:
            enable_process_stealth()
        except Exception as e:
            log.warning("Failed to enable process stealth: %s", e)

        # Enable screenshot blocking (recommended) - DISABLED TEMPORARILY
        # try:
        #     enable_screenshot_blocking()
        #     protect_maplestory_window()
        #     print("[Bot] Screenshot blocking enabled")
        # except Exception as e:
        #     print(f"[Bot] Failed to enable screenshot blocking: {e}")

        # tạm tắt cập nhật recoures

        # self.update_submodules()
        # print('\n[~] Started main bot loop')
        self.thread.start()

    def _main(self):
        """
        The main body of Bot that executes the user's routine.
        :return:    None
        """

        log.info("Initializing detection algorithm")
        # model = detection.load_model()  # Disabled: rune solving turned off
        log.info("Detection algorithm disabled (rune solving off)")

        self.ready = True
        if getattr(config, "listener", None) is not None:
            config.listener.enabled = True
        last_activity_update = time.time()

        # Variant switching - DISABLED
        # Routine starts from index 0 (normal behavior)

        consecutive_errors = 0
        max_consecutive_errors = 10
        metrics = get_metrics_logger()

        while True:
            try:
                # Check if we should log periodic summary
                if metrics.should_log_summary():
                    metrics.log_summary()

                if config.enabled and len(config.routine) > 0:
                    # Track loop start time
                    loop_start_time = time.time()

                    # Update activity for anti-detect
                    current_time = time.time()
                    if current_time - last_activity_update > 1.0:
                        update_activity()
                        last_activity_update = current_time

                        # Highlight the current Point in GUI (if available)
                        try:
                            config.gui.view.routine.select(config.routine.index)
                            config.gui.view.details.display_info(config.routine.index)
                        except Exception as gui_error:
                            log.debug("GUI update error (non-critical): %s", gui_error)

                    # Random Move Backward: Check if we should backward BEFORE any command execution
                    should_backward, backward_steps = config.routine.should_backward()
                    if should_backward:
                        config.routine.apply_backward(backward_steps)
                        metrics.record_backward_movement()
                        element = config.routine[config.routine.index]
                        element_type = element.__class__.__name__
                        log.info(
                            "Random Backward: Now at index %d, element type: %s",
                            config.routine.index,
                            element_type,
                        )

                    element = config.routine[config.routine.index]
                    element_type = element.__class__.__name__

                    # Log current routine state
                    log.debug(
                        "Routine Execution: Index %d/%d - %s",
                        config.routine.index,
                        len(config.routine.sequence) - 1,
                        element_type,
                    )

                    # Check if we should skip this point
                    should_skip = config.routine.should_skip_current_point()

                    if should_skip:
                        if isinstance(element, Point):
                            log.info(
                                "Skipping point at index %d due to randomization",
                                config.routine.index,
                            )
                            metrics.record_point_skip()
                        config.routine.is_skipping_context = True
                        config.routine.step()
                    else:
                        if isinstance(element, Point):
                            log.info(
                                "Executing point at index %d (location: %.3f, %.3f)",
                                config.routine.index,
                                element.location[0],
                                element.location[1],
                            )
                            metrics.record_point_execution()
                            metrics.update_position(element.location)

                        element.execute()
                        log.debug(
                            "Element executed, stepping routine from index %d",
                            config.routine.index,
                        )
                        config.routine.step()
                        log.debug(
                            "Routine stepped, new index: %d/%d",
                            config.routine.index,
                            len(config.routine.sequence) - 1,
                        )

                        config.routine.is_skipping_context = False
                        config.routine.is_backwarding_context = False

                        loop_duration = time.time() - loop_start_time
                        metrics.record_loop_completion(loop_duration)

                        consecutive_errors = 0

                    # CPU Optimization: Adaptive sleep - 20 Hz when active (sufficient responsiveness)
                    time.sleep(0.05)
                else:
                    # Log why bot is not executing to help debug
                    if not config.enabled:
                        log.debug(
                            "Bot loop: config.enabled = False, skipping execution"
                        )
                    elif len(config.routine) == 0:
                        log.debug(
                            "Bot loop: len(config.routine) = 0, skipping execution"
                        )
                    # CPU Optimization: Lower frequency when disabled - 5 Hz (enough to detect enable)
                    time.sleep(0.2)
            except KeyboardInterrupt:
                log.info("Bot loop interrupted by user")
                raise
            except Exception as e:
                consecutive_errors += 1
                metrics.record_error()
                log.error(
                    "Bot loop error (consecutive: %d/%d): %s",
                    consecutive_errors,
                    max_consecutive_errors,
                    e,
                    exc_info=True,
                )

                if consecutive_errors >= max_consecutive_errors:
                    log.critical(
                        "Too many consecutive errors (%d), disabling bot to prevent crash",
                        consecutive_errors,
                    )
                    config.enabled = False
                    consecutive_errors = 0
                    time.sleep(5)
                else:
                    try:
                        if len(config.routine) > 0 and config.routine.index < len(
                            config.routine.sequence
                        ):
                            log.warning(
                                "Recovering: Skipping current point and continuing"
                            )
                            metrics.record_recovery()
                            config.routine.step()
                            config.routine.is_skipping_context = False
                            config.routine.is_backwarding_context = False
                    except Exception as recovery_error:
                        log.error("Recovery failed: %s", recovery_error, exc_info=True)

                    time.sleep(0.5)

    @utils.run_if_enabled
    def _solve_rune(self, model):
        """
        Moves to the position of the rune and solves the arrow-key puzzle.
        :param model:   The TensorFlow model to classify with.
        :param sct:     The mss instance object with which to take screenshots.
        :return:        None
        """

        move = self.command_book["move"]
        move(*self.rune_pos).execute()
        adjust = self.command_book["adjust"]
        adjust(*self.rune_pos).execute()
        time.sleep(0.2)
        press(self.config["Interact"], 1, down_time=0.2)  # Inherited from Configurable

        log.info("Solving rune")
        inferences = []
        for _ in range(15):
            frame = config.capture.frame
            solution = detection.merge_detection(model, frame)
            if solution:
                log.info(", ".join(solution))
                if solution in inferences:
                    log.info("Solution found, entering result")
                    for arrow in solution:
                        press(arrow, 1, down_time=0.1)
                    time.sleep(1)
                    for _ in range(3):
                        time.sleep(0.3)
                        frame = config.capture.frame
                        # CPU Optimization: Pre-convert to grayscale once
                        frame_top_gray = cv2.cvtColor(
                            frame[: frame.shape[0] // 8, :], cv2.COLOR_BGR2GRAY
                        )
                        rune_buff = utils.multi_match(
                            frame_top_gray,
                            RUNE_BUFF_TEMPLATE,
                            threshold=0.9,
                            is_gray=True,
                        )
                        if rune_buff:
                            rune_buff_pos = min(rune_buff, key=lambda p: p[0])
                            target = (
                                round(rune_buff_pos[0] + config.capture.window["left"]),
                                round(rune_buff_pos[1] + config.capture.window["top"]),
                            )
                            click(target, button="right")
                    self.rune_active = False
                    break
                elif len(solution) == 4:
                    inferences.append(solution)

    def load_commands(self, file):
        try:
            self.command_book = CommandBook(file)
            config.gui.settings.update_class_bindings()
        except ValueError:
            pass  # TODO: UI warning popup, say check cmd for errors
        #
        # utils.print_separator()
        # print(f"[~] Loading command book '{basename(file)}':")
        #
        # ext = splitext(file)[1]
        # if ext != '.py':
        #     print(f" !  '{ext}' is not a supported file extension.")
        #     return False
        #
        # new_step = components.step
        # new_cb = {}
        # for c in (components.Wait, components.Walk, components.Fall):
        #     new_cb[c.__name__.lower()] = c
        #
        # # Import the desired command book file
        # module_name = splitext(basename(file))[0]
        # target = '.'.join(['resources', 'command_books', module_name])
        # try:
        #     module = importlib.import_module(target)
        #     module = importlib.reload(module)
        # except ImportError:     # Display errors in the target Command Book
        #     print(' !  Errors during compilation:\n')
        #     for line in traceback.format_exc().split('\n'):
        #         line = line.rstrip()
        #         if line:
        #             print(' ' * 4 + line)
        #     print(f"\n !  Command book '{module_name}' was not loaded")
        #     return
        #
        # # Check if the 'step' function has been implemented
        # step_found = False
        # for name, func in inspect.getmembers(module, inspect.isfunction):
        #     if name.lower() == 'step':
        #         step_found = True
        #         new_step = func
        #
        # # Populate the new command book
        # for name, command in inspect.getmembers(module, inspect.isclass):
        #     new_cb[name.lower()] = command
        #
        # # Check if required commands have been implemented and overridden
        # required_found = True
        # for command in [components.Buff]:
        #     name = command.__name__.lower()
        #     if name not in new_cb:
        #         required_found = False
        #         new_cb[name] = command
        #         print(f" !  Error: Must implement required command '{name}'.")
        #
        # # Look for overridden movement commands
        # movement_found = True
        # for command in (components.Move, components.Adjust):
        #     name = command.__name__.lower()
        #     if name not in new_cb:
        #         movement_found = False
        #         new_cb[name] = command
        #
        # if not step_found and not movement_found:
        #     print(f" !  Error: Must either implement both 'Move' and 'Adjust' commands, "
        #           f"or the function 'step'")
        # if required_found and (step_found or movement_found):
        #     self.module_name = module_name
        #     self.command_book = new_cb
        #     self.buff = new_cb['buff']()
        #     components.step = new_step
        #     config.gui.menu.file.enable_routine_state()
        #     config.gui.view.status.set_cb(basename(file))
        #     config.routine.clear()
        #     print(f" ~  Successfully loaded command book '{module_name}'")
        # else:
        #     print(f" !  Command book '{module_name}' was not loaded")

    def update_submodules(self, force=False):
        """
        Pulls updates from the submodule repositories. If FORCE is True,
        rebuilds submodules by overwriting all local changes.
        """

        utils.print_separator()
        log.info("Retrieving latest submodules")
        self.submodules = []
        repo = git.Repo.init()
        with open(".gitmodules", "r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith("[") and i < len(lines) - 2:
                    path = lines[i + 1].split("=")[1].strip()
                    url = lines[i + 2].split("=")[1].strip()
                    self.submodules.append(path)
                    try:
                        repo.git.clone(url, path)  # First time loading submodule
                        log.info("Initialized submodule '%s'", path)
                    except git.exc.GitCommandError:
                        sub_repo = git.Repo(path)
                        if not force:
                            sub_repo.git.stash()  # Save modified content
                        sub_repo.git.fetch("origin", "main")
                        sub_repo.git.reset("--hard", "FETCH_HEAD")
                        if not force:
                            try:  # Restore modified content
                                sub_repo.git.checkout("stash", "--", ".")
                                log.info(
                                    "Updated submodule '%s', restored local changes",
                                    path,
                                )
                            except git.exc.GitCommandError:
                                log.info("Updated submodule '%s'", path)
                        else:
                            log.info("Rebuilt submodule '%s'", path)
                        sub_repo.git.stash("clear")
                    i += 3
                else:
                    i += 1
