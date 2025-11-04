import cv2
import tkinter as tk
from PIL import ImageTk, Image
from src.gui.interfaces import LabelFrame
from src.common import config, utils
from src.routine.components import Point


class Minimap(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Minimap', **kwargs)

        # Optimized canvas for scale 1.2 minimap (~522x164, display at 2x)
        self.WIDTH = 1044   # 522 × 2 for clear visibility
        self.HEIGHT = 328   # 164 × 2, maintains aspect ratio
        self.canvas = tk.Canvas(self, bg='black',
                                width=self.WIDTH, height=self.HEIGHT,
                                borderwidth=0, highlightthickness=0)
        self.canvas.pack(expand=True, fill='both', padx=5, pady=5)
        self.container = None
        
        # CPU Optimization: Cache converted and resized minimap to avoid repeated conversions
        self.cached_minimap_hash = None
        self.cached_minimap = None
        self.cached_size = None
        # CPU Optimization: Cache PhotoImage when base minimap + overlays unchanged
        self.cached_photo_hash = None
        self.cached_photo_image = None

    def display_minimap(self):
        """Updates the Main page with the current minimap."""

        minimap = config.capture.minimap
        if minimap:
            rune_active = minimap['rune_active']
            rune_pos = minimap['rune_pos']
            path = minimap['path']
            player_pos = minimap['player_pos']

            # CPU Optimization: Cache converted and resized minimap
            # Only convert/resize if minimap data has changed
            minimap_hash = hash(minimap['minimap'].tobytes()) if minimap['minimap'] is not None else None
            
            if minimap_hash != self.cached_minimap_hash or self.cached_minimap is None:
                # Convert and resize only when minimap changes
                img = cv2.cvtColor(minimap['minimap'], cv2.COLOR_BGR2RGB)
                height, width, _ = img.shape

                # Resize minimap to fit the Canvas
                ratio = min(self.WIDTH / width, self.HEIGHT / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                if new_height * new_width > 0:
                    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
                
                # Cache the converted/resized image
                self.cached_minimap = img.copy()
                self.cached_minimap_hash = minimap_hash
                self.cached_size = (new_width, new_height)
            else:
                # Reuse cached image (still need to draw on it)
                img = self.cached_minimap.copy()

            # Mark the position of the active rune
            if rune_active:
                cv2.circle(img,
                           utils.convert_to_absolute(rune_pos, img),
                           3,
                           (128, 0, 128),
                           -1)

            # Draw the current path that the program is taking
            if config.enabled and len(path) > 1:
                for i in range(len(path) - 1):
                    start = utils.convert_to_absolute(path[i], img)
                    end = utils.convert_to_absolute(path[i + 1], img)
                    cv2.line(img, start, end, (0, 255, 255), 1)

            # Draw each Point in the routine as a circle
            for p in config.routine.sequence:
                if isinstance(p, Point):
                    utils.draw_location(img,
                                        p.location,
                                        (0, 255, 0) if config.enabled else (255, 0, 0))

            # Display the current Layout
            if config.layout:
                config.layout.draw(img)

            # Draw the player's position on top of everything
            cv2.circle(img,
                       utils.convert_to_absolute(player_pos, img),
                       3,
                       (0, 0, 255),
                       -1)

            # CPU Optimization: Cache PhotoImage when base minimap + overlays unchanged
            # Hash includes: minimap base, path, rune, player_pos, routine, enabled state
            path_str = str(path) if path else ""
            rune_tuple = (rune_active, rune_pos[0] if rune_pos else None, rune_pos[1] if rune_pos else None)
            player_tuple = (player_pos[0] if player_pos else None, player_pos[1] if player_pos else None)
            routine_str = str(config.routine.sequence) if config.routine else ""
            enabled_hash = config.enabled
            
            # Create combined hash for PhotoImage caching (using hashable types)
            combined_hash = (
                minimap_hash,
                hash(path_str),
                hash(rune_tuple),
                hash(player_tuple),
                hash(routine_str),
                enabled_hash
            )
            
            # Only create PhotoImage if something changed
            if combined_hash != self.cached_photo_hash or self.cached_photo_image is None:
                img_photo = ImageTk.PhotoImage(Image.fromarray(img))
                self.cached_photo_hash = combined_hash
                self.cached_photo_image = img_photo
            else:
                # Reuse cached PhotoImage
                img_photo = self.cached_photo_image

            # Display the minimap in the Canvas
            if self.container is None:
                self.container = self.canvas.create_image(self.WIDTH // 2,
                                                          self.HEIGHT // 2,
                                                          image=img_photo, anchor=tk.CENTER)
            else:
                self.canvas.itemconfig(self.container, image=img_photo)
            self._img = img_photo                 # Prevent garbage collection
