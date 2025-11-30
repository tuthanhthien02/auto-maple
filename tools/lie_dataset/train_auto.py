"""Auto-training script that checks dataset and trains models."""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def check_dataset_size(dataset_dir: str, puzzle_type: str) -> dict:
    """
    Check dataset size and return statistics.

    Returns:
        dict with stats: {'total_frames', 'labeled_frames', 'classes', etc.}
    """
    stats = {
        "total_frames": 0,
        "labeled_frames": 0,
        "classes": {},
        "ready": False,
    }

    if puzzle_type == "puzzle":
        images_dir = os.path.join(dataset_dir, "images")
        labels_dir = os.path.join(dataset_dir, "labels")

        if not os.path.exists(images_dir):
            return stats

        # Count images and labels
        image_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg"]:
            for subdir in Path(images_dir).rglob(ext):
                image_files.append(subdir)

        stats["total_frames"] = len(image_files)

        # Count labeled
        for image_file in image_files:
            label_file = (
                Path(labels_dir)
                / image_file.relative_to(Path(images_dir)).parent
                / f"{image_file.stem}.txt"
            )
            if label_file.exists():
                stats["labeled_frames"] += 1

        # Ready if at least 50 labeled frames
        stats["ready"] = stats["labeled_frames"] >= 50

    elif puzzle_type == "violetta":
        # Check for YOLO format labels (preferred)
        raw_frames_dir = os.path.join(dataset_dir, "raw_frames")
        labels_dir = os.path.join(dataset_dir, "labels")

        if os.path.exists(raw_frames_dir) and os.path.exists(labels_dir):
            # YOLO format: count labeled frames
            for video_dir in Path(raw_frames_dir).iterdir():
                if not video_dir.is_dir():
                    continue

                video_name = video_dir.name
                for ext in ["*.png", "*.jpg", "*.jpeg"]:
                    for image_file in video_dir.glob(ext):
                        label_file = (
                            Path(labels_dir) / video_name / f"{image_file.stem}.txt"
                        )
                        if label_file.exists():
                            stats["labeled_frames"] += 1
                        stats["total_frames"] += 1

            # Ready if at least 50 labeled frames
            stats["ready"] = stats["labeled_frames"] >= 50

        # Fallback: check classification format
        else:
            train_dir = os.path.join(dataset_dir, "train")

            if not os.path.exists(train_dir):
                return stats

            # Count by class
            for class_dir in Path(train_dir).iterdir():
                if not class_dir.is_dir():
                    continue

                class_name = class_dir.name
                image_files = []
                for ext in ["*.png", "*.jpg", "*.jpeg"]:
                    image_files.extend(class_dir.glob(ext))

                count = len(image_files)
                stats["classes"][class_name] = count
                stats["total_frames"] += count

            # Ready if at least 20 frames per class (minimum 3 classes)
            min_per_class = 20
            ready_classes = sum(
                1 for count in stats["classes"].values() if count >= min_per_class
            )
            stats["ready"] = ready_classes >= 3 and stats["total_frames"] >= 100

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Auto-train lie detector models when dataset is ready"
    )
    parser.add_argument(
        "--type", required=True, choices=["puzzle", "violetta"], help="Puzzle type"
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="Dataset directory (default: ai/lie_detector/{type}/dataset)",
    )
    parser.add_argument(
        "--min_frames",
        type=int,
        default=50,
        help="Minimum frames required for puzzle (default: 50)",
    )
    parser.add_argument(
        "--min_per_class",
        type=int,
        default=20,
        help="Minimum frames per class for violetta (default: 20)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force training even if dataset is small",
    )

    args = parser.parse_args()

    # Determine dataset directory
    if args.dataset:
        dataset_dir = args.dataset
    else:
        dataset_dir = os.path.join(
            project_root, "ai", "lie_detector", args.type, "dataset"
        )

    if not os.path.exists(dataset_dir):
        print(f"Error: Dataset directory not found: {dataset_dir}")
        print("Please run process_all.py first to create dataset")
        return

    print(f"Checking dataset: {dataset_dir}")
    print(f"Type: {args.type}")
    print()

    # Check dataset
    stats = check_dataset_size(dataset_dir, args.type)

    print("Dataset Statistics:")
    print(f"  Total frames: {stats['total_frames']}")

    if args.type == "puzzle":
        print(f"  Labeled frames: {stats['labeled_frames']}")
        print(f"  Ready: {stats['ready']}")

        if not stats["ready"] and not args.force:
            print()
            print(f"Dataset not ready. Need at least {args.min_frames} labeled frames.")
            print(f"Current: {stats['labeled_frames']}")
            print()
            print("Next steps:")
            print("1. Record more videos")
            print("2. Run: python tools/lie_dataset/process_all.py --type puzzle")
            print(
                "3. Review labels if needed: python tools/lie_dataset/review_labels.py --type puzzle"
            )
            return

    elif args.type == "violetta":
        if stats.get("labeled_frames", 0) > 0:
            # YOLO format
            print(f"  Labeled frames: {stats['labeled_frames']}")
            print(f"  Total frames: {stats['total_frames']}")
            print(f"  Ready: {stats['ready']}")

            if not stats["ready"] and not args.force:
                print()
                print("Dataset not ready. Need at least 50 labeled frames.")
                print(f"Current: {stats['labeled_frames']}")
                print()
                print("Next steps:")
                print("1. Record more videos")
                print("2. Run: python tools/lie_dataset/process_all.py --type violetta")
                print(
                    "3. Label bounding boxes: python tools/lie_dataset/label_violetta_yolo.py"
                )
                return
        else:
            # Classification format (fallback)
            print(f"  Classes: {len(stats['classes'])}")
            for class_name, count in stats["classes"].items():
                print(f"    {class_name}: {count}")
            print(f"  Ready: {stats['ready']}")

            if not stats["ready"] and not args.force:
                print()
                print(
                    f"Dataset not ready. Need at least {args.min_per_class} frames per class (minimum 3 classes)."
                )
                print()
                print("Next steps:")
                print("1. Record more videos")
                print("2. Run: python tools/lie_dataset/process_all.py --type violetta")
                print("3. Label frames: python tools/lie_dataset/label_violetta_gui.py")
                return

    # Dataset is ready, start training
    print()
    print("Dataset is ready! Starting training...")
    print()

    if args.type == "puzzle":
        train_script = os.path.join(
            project_root, "ai", "lie_detector", "puzzle", "train_puzzle_yolo.py"
        )
    else:
        # Check if YOLO format (preferred) or classification format
        raw_frames_dir = os.path.join(dataset_dir, "raw_frames")
        labels_dir = os.path.join(dataset_dir, "labels")

        if os.path.exists(raw_frames_dir) and os.path.exists(labels_dir):
            # Use YOLO training
            train_script = os.path.join(
                project_root, "ai", "lie_detector", "violetta", "train_violetta_yolo.py"
            )
        else:
            # Fallback to classification
            train_script = os.path.join(
                project_root,
                "ai",
                "lie_detector",
                "violetta",
                "train_violetta_classifier.py",
            )

    if not os.path.exists(train_script):
        print(f"Error: Training script not found: {train_script}")
        print("Please create training script first")
        return

    # Run training script
    import subprocess

    print(f"Running: python {train_script}")
    print()

    try:
        subprocess.run(
            ["python", train_script, "--dataset", dataset_dir],
            check=True,
        )
        print()
        print("Training completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Training failed with error: {e}")
        return
    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
        return


if __name__ == "__main__":
    main()
