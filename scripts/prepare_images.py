#!/usr/bin/env python3
"""Recreate RadarMind image paths from officially downloaded upstream data."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from collections.abc import Iterator
from pathlib import Path


PAIRED_FILES = ("train.json", "test.json")
SARDET_FILES = ("sarvqa1_train.json", "sarvqa1_test.json")
RGB_FOLDER = {
    ("train", "oemsar"): "OEMSARtrain",
    ("test", "oemsar"): "OEMSARtest",
    ("train", "dfc2023"): "DFC2023train",
    ("test", "dfc2023"): "DFC2023test",
    ("train", "spacenet6"): "SpaceNet6train",
    ("test", "spacenet6"): "SpaceNet6test",
}
EXPECTED = {"paired": 13244, "sardet": 104985, "records": 118229}


def records(path: Path) -> Iterator[dict]:
    """Stream the release's one-record-per-line JSON array."""
    with path.open("r", encoding="utf-8") as stream:
        for number, raw in enumerate(stream, 1):
            line = raw.strip()
            if not line or line in ("[", "]"):
                continue
            if line.startswith("["):
                line = line[1:].lstrip()
            if line.endswith("]"):
                line = line[:-1].rstrip()
            if line.endswith(","):
                line = line[:-1].rstrip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Cannot parse {path}:{number}: {exc}") from exc


def place(source: Path, target: Path, mode: str, verify_only: bool = False) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Missing upstream image: {source}")
    if verify_only:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.stat().st_size != source.stat().st_size:
            raise ValueError(f"Existing target differs in size: {target}")
        return
    if mode == "copy":
        shutil.copy2(source, target)
    elif mode == "hardlink":
        try:
            os.link(source, target)
        except OSError as exc:
            raise OSError(
                f"Cannot hardlink {source} -> {target}; use --mode copy when filesystems differ"
            ) from exc
    elif mode == "symlink":
        target.symlink_to(source.resolve())
    else:
        raise ValueError(mode)


def safe_target(root: Path, relative: str) -> Path:
    target = (root / Path(relative)).resolve()
    root_resolved = root.resolve()
    if target != root_resolved and root_resolved not in target.parents:
        raise ValueError(f"Annotation path escapes output root: {relative}")
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations-root", type=Path, required=True)
    parser.add_argument("--sarlang-root", type=Path, required=True)
    parser.add_argument("--sardet-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--mode", choices=("hardlink", "copy", "symlink"), default="hardlink")
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Check every upstream filename and annotation mapping without creating image files.",
    )
    args = parser.parse_args()

    annotations = args.annotations_root.resolve()
    sarlang = args.sarlang_root.resolve()
    sardet = args.sardet_root.resolve()
    output = args.output_root.resolve()
    output.mkdir(parents=True, exist_ok=True)

    paired_count = 0
    sardet_count = 0
    seen_targets: set[Path] = set()

    for filename in PAIRED_FILES:
        annotation_file = annotations / filename
        for record in records(annotation_file):
            split = record["split"]
            source_name = record["source"]
            rgb_name = Path(record["images"]["rgb"]).name
            sar_name = Path(record["images"]["sar"]).name
            if Path(rgb_name).stem.casefold() != Path(sar_name).stem.casefold():
                raise ValueError(f"RGB/SAR stem mismatch in record {record['id']}")
            rgb_source = sarlang / "RGBimages" / split / RGB_FOLDER[(split, source_name)] / rgb_name
            sar_source = sarlang / "SARimages" / sar_name
            for key, upstream in (("rgb", rgb_source), ("sar", sar_source)):
                target = safe_target(output, record["images"][key])
                if target in seen_targets:
                    raise ValueError(f"Duplicate target path: {target}")
                seen_targets.add(target)
                place(upstream, target, args.mode, args.verify_only)
            paired_count += 1

    for filename in SARDET_FILES:
        annotation_file = annotations / filename
        for record in records(annotation_file):
            partition = record["source_partition"]
            image_name = Path(record["images"]["sar"]).name
            upstream = sardet / "Images" / partition / image_name
            target = safe_target(output, record["images"]["sar"])
            if target in seen_targets:
                raise ValueError(f"Duplicate target path: {target}")
            seen_targets.add(target)
            place(upstream, target, args.mode, args.verify_only)
            sardet_count += 1

    total = paired_count + sardet_count
    actual = {"paired": paired_count, "sardet": sardet_count, "records": total}
    if actual != EXPECTED:
        raise ValueError(f"Unexpected record counts: {actual}; expected {EXPECTED}")
    print(json.dumps({"status": "ok", **actual, "files_placed": len(seen_targets)}, indent=2))


if __name__ == "__main__":
    main()


