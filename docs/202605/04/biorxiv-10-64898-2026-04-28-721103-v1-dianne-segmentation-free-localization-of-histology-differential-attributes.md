---
title: "DIANNE: Segmentation-Free Localization of Histology Differential Attributes"
title_zh: DIANNE：组织学差异属性的无分割定位
authors: "Domanskyi, S., Rubinstein, J. C., Sheridan, T. B., Thiesen, A., Noorbakhsh, J., Alcoforado Diniz, J., Ramasamy, R., Baker, D. S., Sheldon, R., Wu, Q., Kuchel, G., Robson, P., Chuang, J. H."
date: 2026-05-01
pdf: "https://www.biorxiv.org/content/10.64898/2026.04.28.721103v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 组织学图像中的无分割定位
tldr: "在数字病理学中，手动标注耗时且限制新空间行为探索。DIANNE提出基于训练时正类混合增强的方法，利用基础模型实现无分割的快速定位。它能在秒级处理全切片H&E图像，支持实时训练和多种图像类型，用于肿瘤检测等任务，提供实用系统理解空间表型。"
source: biorxiv
selection_source: fresh_fetch
motivation: 当前数字病理学方法依赖手动标注，耗时且不适合探索新的空间行为，需要快速、无需分割的定位方法。
method: DIANNE采用训练时正类混合增强和基础模型，实现无分割的快速定位和实时训练。
result: DIANNE能在秒级处理全切片图像，用于肿瘤检测、伪影识别等，并支持多种图像类型如IHC和空间转录组。
conclusion: DIANNE提供了一个实用系统，用于定量理解已知和新的空间表型。
---

## 摘要
病理学家指导的组织学和空间组学图像中的区分为健康和疾病提供了见解，数字病理学利用人工智能来自动化此类评估。为了训练计算模型，当前的数字病理学方法依赖于预先的手动注释，这些注释生成起来耗时。预注释不适合研究新的空间行为——这是空间分析进展驱动的主要需求——对于这些行为，注释标准和数据需求将是不确定的。为了应对这些挑战，我们提出了DIANNE，一种基于训练时正类混合增强的数字病理学方法，用于快速训练和推断空间差异属性。DIANNE可以在工作站上几秒钟内计算基础模型衍生的无分割定位差异分类器，覆盖整个切片H&E图像，从而实现空间生态位的交互式研究。预测模型可以实时重新训练，以响应补丁或区域注释的变化，仅从几十个注释补丁中澄清跨切片的决定性生物属性。我们展示了DIANNE在肿瘤检测、伪影识别以及胰腺、胎膜和肾脏组织结构探索方面的有效性。DIANNE还为免疫组化（IHC）、多重免疫荧光和注册的空间转录组学+H&E图像提供了类似的能力。DIANNE在Jupyter工具包中实现，能够从弱监督训练中快速开发高分辨率分类器。DIANNE提供了一个实用的系统，用于定量理解已知和新的空间表型。

## Abstract
Pathologist-guided distinctions within histology and spatial omic images provide insights into health and disease, with digital pathology leveraging artificial intelligence to automate such assessments. To train computational models, current digital pathology methods rely on upfront manual annotations, which are time-consuming to generate. Pre-annotation is poorly suited to investigating novel spatial behaviors - a major need driven by advances in spatial profiling - for which annotation criteria and data needs will be uncertain. To address these challenges, we present DIANNE, a digital pathology approach for rapid training and inference of spatial differential attributes based on train-time Positive Class Mixup Augmentation. DIANNE can compute foundation model-derived segmentation-free localization of differential classifiers across whole slide H&E images within seconds on a workstation, enabling interactive investigation of spatial niches. Predictive models can be re-trained in real-time in response to patch or regional annotation changes, clarifying determinative biological attributes across slides from only a few dozen annotated patches. We demonstrate the effectiveness of DIANNE for tumor detection, artifact identification, and exploration of pancreatic, fetal membranes and kidney tissue structures. DIANNE also provides analogous capabilities for IHC, multiplex immunofluorescence, and registered spatial transcriptomic+H&E images. DIANNE is implemented in a Jupyter toolkit, enabling rapid development of high-resolution classifiers from weakly-supervised training. DIANNE provides a practical system to quantitatively understand known and novel spatial phenotypes.