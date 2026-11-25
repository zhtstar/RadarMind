# SARLingu

SARLingu is a text-only release. It does not include SAR or RGB image files.

## Statistics

| Item | Count |
| --- | ---: |
| Image records | 118,229 |
| Paired RGB/SAR records | 13,244 |
| SARDet-100K SAR-only records | 104,985 |
| VQA families | 1,080,076 |
| VQA question formulations | 4,459,880 |
| Caption QA families | 45,650 |
| Caption question formulations | 182,600 |
| Caption answer formulations | 182,600 |
| Generated RGB captions | 13,244 |
| Generated SAR captions | 13,244 |

The paired records consist of 5,174 DFC2023 pairs, 4,813 OpenEarthMap-SAR pairs, and 3,257 SpaceNet6 pairs.

## Annotation files

- `annotations/train.json`: paired RGB/SAR training records;
- `annotations/test.json`: paired RGB/SAR test records;
- `annotations/sarvqa1_train.json`: SARDet-100K training records;
- `annotations/sarvqa1_test.json`: SARDet-100K validation images used as the RadarMind test split.

The public files contain VQA and caption annotations. Training and evaluation eligibility is represented directly in the relevant annotation entries.

## Upstream downloads

For the 13,244 paired records, download `RGBimages.zip` and `SARimages_preprocessed.zip` from:

https://huggingface.co/datasets/YiminJimmy/SARLANG-1M/tree/main

For the 104,985 SAR-only records, download the SARDet-100K `train` and `val` image archives from:

https://github.com/zcablii/SARDet_100K

Downloading the raw SpaceNet6, DFC2023, or OpenEarthMap-SAR projects directly is not recommended for this release, because SARLANG-1M applies its own selection and preprocessing. The official SARLANG-1M image archives provide the filenames used by the annotations.

## Filename verification

Release validation confirmed:

- all 13,244 paired RGB filenames in the official SARLANG-1M RGB archive;
- all 13,244 paired SAR filenames in the official SARLANG-1M preprocessed SAR archive;
- all RGB/SAR filename stems identical within each pair;
- all 104,985 SARDet filenames and extensions unchanged from the official `train` and `val` folders;
- zero missing or renamed image basenames.

Directory prefixes were normalized in SARLingu, so users must run `scripts/prepare_images.py` or implement the mappings below.

| RadarMind path | Upstream path |
| --- | --- |
| `images/rgb/train/oemsar/<file>` | `RGBimages/train/OEMSARtrain/<file>` |
| `images/rgb/test/oemsar/<file>` | `RGBimages/test/OEMSARtest/<file>` |
| `images/rgb/train/dfc2023/<file>` | `RGBimages/train/DFC2023train/<file>` |
| `images/rgb/test/dfc2023/<file>` | `RGBimages/test/DFC2023test/<file>` |
| `images/rgb/train/spacenet6/<file>` | `RGBimages/train/SpaceNet6train/<file>` |
| `images/rgb/test/spacenet6/<file>` | `RGBimages/test/SpaceNet6test/<file>` |
| `images/sar/<split>/<source>/<file>` | `SARimages/<file>` |
| `images/sar_only/train/<file>` | `SARDet-100K/Images/train/<file>` |
| `images/sar_only/test/<file>` | `SARDet-100K/Images/val/<file>` |

The SpaceNet6 RGB files use `.tif`, while their paired preprocessed SAR files use `.png`. Pairing is based on the filename stem, not the extension.


