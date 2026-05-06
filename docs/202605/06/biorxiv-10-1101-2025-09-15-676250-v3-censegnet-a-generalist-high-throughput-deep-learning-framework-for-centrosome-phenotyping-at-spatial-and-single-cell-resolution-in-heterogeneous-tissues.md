---
title: "CenSegNet: a generalist high-throughput deep learning framework for centrosome phenotyping at spatial and single-cell resolution in heterogeneous tissues"
title_zh: CenSegNet：用于异质组织中空间和单细胞分辨率中心体表型分析的通用型高通量深度学习框架
authors: "Cheng, J., Fan, K., Bailey, M., Du, X., Jena, R., Savva, C., Reed, E., Gou, M., Zuo, P., Beers, S., Cutress, R., Cai, X., Elias, S."
date: 2026-05-04
pdf: "https://www.biorxiv.org/content/10.1101/2025.09.15.676250v3.full.pdf"
tags: ["query:imgfor"]
score: 7.0
evidence: 用于图像分割和区域定位的深度学习框架
tldr: 本研究针对中心体异常在癌症中的空间复杂性和表型异质性问题，提出了CenSegNet深度学习框架，用于高分辨率分割中心体和上皮结构。该框架在多种组织类型和成像模态上表现优异，首次实现了大规模、单细胞分辨率的中心体异常量化，揭示了其与临床特征的关联，并支持了中心体表型分析的临床相关性。
source: biorxiv
selection_source: fresh_fetch
motivation: 中心体异常是上皮癌症的关键标志，但传统图像分析无法解析其空间复杂性和表型异质性，限制了研究进展。
method: CenSegNet采用模块化深度学习框架，集成双分支架构和不确定性引导的细化，实现高分辨率、上下文感知的中心体分割。
result: CenSegNet在多种成像模态上达到最先进性能，应用于乳腺癌组织微阵列，首次大规模量化中心体异常，并发现其与肿瘤分级、生存率等临床特征相关。
conclusion: CenSegNet为组织中的中心体表型分析提供了可扩展、通用的平台，有助于系统解析中心体生物学及其在癌症中的失调。
---

## 摘要
中心体异常（CA）是上皮癌的标志，但由于传统图像分析的限制，其空间复杂性和表型异质性仍未得到充分解析。我们提出了CenSegNet（中心体分割网络），这是一个模块化深度学习框架，用于跨多种组织类型的高分辨率、上下文感知的中心体和上皮结构分割。通过整合双分支架构和不确定性引导的细化，CenSegNet在免疫荧光和免疫组化两种模态中实现了最先进的性能和泛化能力，在准确性和形态保真度上优于现有模型。应用于包含127名患者911个乳腺癌样本核心的组织微阵列（TMAs），CenSegNet首次实现了在单细胞分辨率下对数值和结构CA的大规模、空间分辨量化。这些CA亚型在机制上是解耦的，表现出不同的空间分布、年龄依赖性动态，并与组织学肿瘤分级、激素受体状态、基因组改变和淋巴结受累相关。结构CA水平还与总生存率相关，支持空间分辨CA模式的临床相关性。肿瘤边缘的不一致CA谱与局部侵袭性和基质重塑相关。为了支持广泛采用和可重复性，CenSegNet作为开源Python库发布。总之，我们的研究将CenSegNet确立为一个可扩展、可泛化的平台，用于完整组织中空间分辨的中心体表型分析，能够系统解析该细胞器的生物学及其在癌症和其他上皮疾病中的失调。

## Abstract
Centrosome abnormalities (CA) are a hallmark of epithelial cancers, yet their spatial complexity and phenotypic heterogeneity remain poorly resolved due to limitations in conventional image analysis. We present CenSegNet (Centrosome Segmentation Network), a modular deep learning framework for high-resolution, context-aware segmentation of centrosomes and epithelial architecture across diverse tissue types. Integrating a dual-branch architecture with uncertainty-guided refinement, CenSegNet achieves state-of-the-art performance and generalisability across both immunofluorescence and immunohistochemistry modalities, outperforming existing models in accuracy and morphological fidelity. Applied to tissue microarrays (TMAs) containing 911 breast cancer sample cores from 127 patients, CenSegNet enables the first large-scale, spatially resolved quantification of numerical and structural CA at single-cell resolution. These CA subtypes are mechanistically uncoupled, exhibiting distinct spatial distributions, age-dependent dynamics, and associations with histological tumour grade, hormone receptor status, genomic alterations, and nodal involvement. Structural CA levels are additionally associated with overall survival, supporting the clinical relevance of spatially resolved CA patterns. Discordant CA profiles at tumour margins are linked to local aggressiveness and stromal remodelling. To support broad adoption and reproducibility, CenSegNet is released as an open-source Python library. Together, our findings establish CenSegNet as a scalable, generalisable platform for spatially resolved centrosome phenotyping in intact tissues, enabling systematic dissection of the biology of this organelle and its dysregulation in cancer and other epithelial diseases.