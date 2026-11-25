<div align="center">

# RadarMind

### Explainable Chain-of-Thought Reasoning for SAR Image Interpretation with Large Vision-Language Models

<p>
  <a href="https://doi.org/10.1109/TAES.2026.3719218"><img src="https://img.shields.io/badge/Paper-IEEE-00629B?logo=ieee&logoColor=white" alt="IEEE paper" /></a>
  <a href="https://openreview.net/forum?id=StGQ99KD78"><img src="https://img.shields.io/badge/OpenReview-Paper-8C1B13" alt="OpenReview" /></a>
  <a href="https://huggingface.co/datasets/zhtstar/SARLingu"><img src="https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black" alt="Hugging Face dataset" /></a>
  <a href="https://modelscope.cn/datasets/zhtstar/SARLingu"><img src="https://img.shields.io/badge/ModelScope-Dataset-624AFF" alt="ModelScope dataset" /></a>
  <a href="https://huggingface.co/zhtstar/RadarMind-3B"><img src="https://img.shields.io/badge/Hugging%20Face-3B-FFD21E?logo=huggingface&logoColor=black" alt="RadarMind-3B on Hugging Face" /></a>
  <a href="https://huggingface.co/zhtstar/RadarMind-7B"><img src="https://img.shields.io/badge/Hugging%20Face-7B-FFD21E?logo=huggingface&logoColor=black" alt="RadarMind-7B on Hugging Face" /></a>
</p>

</div>

This repository hosts the official implementation of the paper **“RadarMind: Explainable Chain-of-Thought Reasoning for SAR Image Interpretation with Large Vision-Language Models.”**

Haitao Zhang, Haote Xu, Hongyang Zhang, Yuzhi Huang, Hailiang Huang, Yue Huang, Xinghao Ding, and Huangxing Lin

## Overview

RadarMind is a vision-language model for synthetic aperture radar (SAR) image understanding. The project provides two model scales and SARLingu, a large-scale text annotation resource covering visual question answering and image captioning.

## Release links

| Resource | Hugging Face | ModelScope |
| --- | --- | --- |
| SARLingu | [Dataset](https://huggingface.co/datasets/zhtstar/SARLingu) | [Dataset](https://modelscope.cn/datasets/zhtstar/SARLingu) |
| RadarMind-3B | [Model](https://huggingface.co/zhtstar/RadarMind-3B) | [Model](https://modelscope.cn/models/zhtstar/RadarMind-3B) |
| RadarMind-7B | [Model](https://huggingface.co/zhtstar/RadarMind-7B) | [Model](https://modelscope.cn/models/zhtstar/RadarMind-7B) |

The repository pages are being populated progressively. A link may remain unavailable until its corresponding upload finishes.

## SARLingu

SARLingu is released as text annotations only. It contains:

- 118,229 image records;
- 1,080,076 VQA families and 4,459,880 question formulations;
- 45,650 caption-QA families and 182,600 question-answer formulations;
- 13,244 SAR image captions and 13,244 paired RGB image captions.

Image files are not redistributed. The annotation files retain the original image filenames so users can obtain the pixels from the upstream datasets and reconstruct the referenced paths.

### Upstream images

- Paired SAR/RGB images: download `SARimages_preprocessed.zip` and `RGBimages.zip` from [SARLANG-1M](https://huggingface.co/datasets/YiminJimmy/SARLANG-1M/tree/main).
- SARDet images: download the train and validation images from [SARDet-100K](https://github.com/zcablii/SARDet_100K). RadarMind uses SARDet `train` for training and SARDet `val` for evaluation.

The image preparation utility checks every referenced filename and creates the directory layout expected by the annotations:

```bash
python scripts/prepare_images.py \
  --annotations-root /path/to/SARLingu/annotations \
  --sarlang-root /path/to/SARLANG-1M \
  --sardet-root /path/to/SARDet-100K \
  --output-root /path/to/SARLingu \
  --mode copy
```

See [docs/DATASET.md](docs/DATASET.md) for the complete mapping rules and dataset structure.

## Models

- **RadarMind-3B** is derived from Qwen2.5-VL-3B-Instruct and distributed as fully merged weights.
- **RadarMind-7B** is derived from Qwen2.5-VL-7B-Instruct and distributed as fully merged weights.

Please follow each model repository for its base-model license, usage conditions, and loading instructions.

## Citation

```bibtex
@article{zhang2026radarmind,
  title   = {RadarMind: Explainable Chain-of-Thought Reasoning for SAR Image Interpretation with Large Vision-Language Models},
  author  = {Zhang, Haitao and Xu, Haote and Zhang, Hongyang and Huang, Yuzhi and Huang, Hailiang and Huang, Yue and Ding, Xinghao and Lin, Huangxing},
  journal = {IEEE Transactions on Aerospace and Electronic Systems},
  year    = {2026},
  publisher = {IEEE}
}
```

## License and acknowledgements

- Repository code is released under the Apache License 2.0.
- SARLingu text annotations are released under CC BY-NC 4.0.
- Model use remains subject to the license of the corresponding base model.
- Images are not included and remain governed by their original licenses and terms of use.

RadarMind builds on [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL), [SARLANG-1M](https://huggingface.co/datasets/YiminJimmy/SARLANG-1M), and [SARDet-100K](https://github.com/zcablii/SARDet_100K). We thank the authors and maintainers of these projects.


