"""Data augmentation for lie detector datasets."""

import os
import cv2
import numpy as np
from pathlib import Path
import random
import argparse


def augment_image(image: np.ndarray, augment_type: str) -> np.ndarray:
    """
    Apply augmentation to image.

    Args:
        image: Input image (BGR format)
        augment_type: Type of augmentation

    Returns:
        Augmented image
    """
    if augment_type == "rotation":
        angle = random.uniform(-10, 10)
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

    elif augment_type == "brightness":
        factor = random.uniform(0.7, 1.3)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * factor, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    elif augment_type == "contrast":
        factor = random.uniform(0.8, 1.2)
        return cv2.convertScaleAbs(image, alpha=factor, beta=0)

    elif augment_type == "blur":
        kernel_size = random.choice([3, 5])
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    elif augment_type == "scale":
        scale = random.uniform(0.9, 1.1)
        h, w = image.shape[:2]
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(image, (new_w, new_h))
        # Crop or pad to original size
        if scale > 1.0:
            # Crop center
            start_x = (new_w - w) // 2
            start_y = (new_h - h) // 2
            return resized[start_y : start_y + h, start_x : start_x + w]
        else:
            # Pad
            pad_x = (w - new_w) // 2
            pad_y = (h - new_h) // 2
            return cv2.copyMakeBorder(
                resized,
                pad_y,
                h - new_h - pad_y,
                pad_x,
                w - new_w - pad_x,
                cv2.BORDER_REPLICATE,
            )

    elif augment_type == "flip_horizontal":
        return cv2.flip(image, 1)

    elif augment_type == "flip_vertical":
        return cv2.flip(image, 0)

    else:
        return image


def augment_yolo_label(label_path: str, augment_type: str, output_path: str) -> bool:
    """
    Augment YOLO label (adjust bbox for augmentations that affect geometry).

    Args:
        label_path: Path to input label file
        augment_type: Type of augmentation
        output_path: Path to save augmented label

    Returns:
        True if successful
    """
    try:
        with open(label_path, "r") as f:
            line = f.readline().strip()
            if not line:
                return False

        # For most augmentations, label stays the same
        # Only geometric transforms need adjustment
        if augment_type in ["flip_horizontal", "flip_vertical"]:
            parts = line.split()
            if len(parts) < 5:
                return False

            class_id = parts[0]
            center_x = float(parts[1])
            center_y = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])

            if augment_type == "flip_horizontal":
                center_x = 1.0 - center_x
            elif augment_type == "flip_vertical":
                center_y = 1.0 - center_y

            new_line = (
                f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}"
            )
        else:
            new_line = line

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(new_line)

        return True
    except Exception as e:
        print(f"Error augmenting label {label_path}: {e}")
        return False


def augment_puzzle_dataset(
    dataset_dir: str, output_dir: str, num_augmentations: int = 5
):
    """
    Augment puzzle dataset (YOLO format).

    Args:
        dataset_dir: Input dataset directory
        output_dir: Output directory for augmented data
        num_augmentations: Number of augmentations per image
    """
    images_dir = os.path.join(dataset_dir, "raw_frames")
    labels_dir = os.path.join(dataset_dir, "labels")

    if not os.path.exists(images_dir):
        print(f"Error: Images directory not found: {images_dir}")
        return

    # Find all images
    image_files = []
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        for subdir in Path(images_dir).rglob(ext):
            image_files.append(subdir)

    print(f"Found {len(image_files)} images to augment")

    augmentations = [
        "rotation",
        "brightness",
        "contrast",
        "blur",
        "scale",
    ]

    output_images_dir = os.path.join(output_dir, "images")
    output_labels_dir = os.path.join(output_dir, "labels")
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)

    augmented_count = 0

    for image_file in image_files:
        # Load original
        image = cv2.imread(str(image_file))
        if image is None:
            continue

        # Find corresponding label
        rel_path = image_file.relative_to(Path(images_dir))
        label_file = Path(labels_dir) / rel_path.parent / f"{image_file.stem}.txt"

        # Copy original
        output_image_path = os.path.join(output_images_dir, image_file.name)
        output_label_path = os.path.join(output_labels_dir, f"{image_file.stem}.txt")

        cv2.imwrite(output_image_path, image)
        if label_file.exists():
            import shutil

            shutil.copy2(label_file, output_label_path)

        # Create augmentations
        for i in range(num_augmentations):
            aug_type = random.choice(augmentations)
            aug_image = augment_image(image, aug_type)

            aug_name = f"{image_file.stem}_aug{i}_{aug_type}.png"
            aug_image_path = os.path.join(output_images_dir, aug_name)
            aug_label_path = os.path.join(
                output_labels_dir, f"{image_file.stem}_aug{i}_{aug_type}.txt"
            )

            cv2.imwrite(aug_image_path, aug_image)

            if label_file.exists():
                augment_yolo_label(str(label_file), aug_type, aug_label_path)

            augmented_count += 1

    print(f"Created {augmented_count} augmented images")
    print(f"Output: {output_dir}")


def augment_violetta_dataset(
    dataset_dir: str, output_dir: str, num_augmentations: int = 5
):
    """
    Augment violetta dataset (classification format).

    Args:
        dataset_dir: Input dataset directory (with class subdirectories)
        output_dir: Output directory for augmented data
        num_augmentations: Number of augmentations per image
    """
    train_dir = os.path.join(dataset_dir, "train")

    if not os.path.exists(train_dir):
        print(f"Error: Train directory not found: {train_dir}")
        return

    augmentations = [
        "rotation",
        "brightness",
        "contrast",
        "blur",
        "scale",
        "flip_horizontal",
    ]

    output_train_dir = os.path.join(output_dir, "train")
    os.makedirs(output_train_dir, exist_ok=True)

    augmented_count = 0

    # Process each class directory
    for class_dir in Path(train_dir).iterdir():
        if not class_dir.is_dir():
            continue

        class_name = class_dir.name
        output_class_dir = os.path.join(output_train_dir, class_name)
        os.makedirs(output_class_dir, exist_ok=True)

        # Find all images in class
        image_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg"]:
            image_files.extend(class_dir.glob(ext))

        print(f"Processing class '{class_name}': {len(image_files)} images")

        for image_file in image_files:
            # Load original
            image = cv2.imread(str(image_file))
            if image is None:
                continue

            # Copy original
            output_image_path = os.path.join(output_class_dir, image_file.name)
            cv2.imwrite(output_image_path, image)

            # Create augmentations
            for i in range(num_augmentations):
                aug_type = random.choice(augmentations)
                aug_image = augment_image(image, aug_type)

                aug_name = f"{image_file.stem}_aug{i}_{aug_type}.png"
                aug_image_path = os.path.join(output_class_dir, aug_name)
                cv2.imwrite(aug_image_path, aug_image)
                augmented_count += 1

    print(f"Created {augmented_count} augmented images")
    print(f"Output: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Augment lie detector datasets")
    parser.add_argument(
        "--type", required=True, choices=["puzzle", "violetta"], help="Dataset type"
    )
    parser.add_argument("--input", required=True, help="Input dataset directory")
    parser.add_argument(
        "--output", required=True, help="Output directory for augmented data"
    )
    parser.add_argument(
        "--num_aug", type=int, default=5, help="Number of augmentations per image"
    )

    args = parser.parse_args()

    if args.type == "puzzle":
        augment_puzzle_dataset(args.input, args.output, args.num_aug)
    else:
        augment_violetta_dataset(args.input, args.output, args.num_aug)


if __name__ == "__main__":
    main()
