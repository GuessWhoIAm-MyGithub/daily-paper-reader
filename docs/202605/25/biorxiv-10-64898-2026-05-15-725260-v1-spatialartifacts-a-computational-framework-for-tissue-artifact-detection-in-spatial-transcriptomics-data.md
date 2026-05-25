---
title: "SpatialArtifacts: a computational framework for tissue artifact detection in spatial transcriptomics data"
title_zh: "SpatialArtifacts: 用于空间转录组学数据中组织伪影检测的计算框架"
authors: "He, J. H., Thompson, J. R., Totty, M. S., Hicks, S. C."
date: 2026-05-18
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.15.725260v1.full.pdf"
tags: ["query:imgfor"]
score: 7.0
evidence: 用于定位图像中空间伪影的计算框架
tldr: 空间转录组数据常受干燥斑块、组织脱落等技术伪影影响，导致UMI计数低，尤其在组织边界。现有质量控制方法难以识别这些区域。本文提出SpatialArtifacts框架，结合中位数绝对偏差（MAD）异常检测和数学形态学操作，识别和分类空间连续的组织伪影。在人类海马体、背外侧前额叶皮层和结直肠癌组织中使用10x Genomics Visium和VisiumHD平台验证了其性能，并免费提供软件包。
source: biorxiv
selection_source: fresh_fetch
motivation: 空间转录组数据常受技术伪影影响，现有方法难以识别低质量区域。
method: 提出SpatialArtifacts框架，结合MAD异常检测和数学形态学操作来识别和分类组织伪影。
result: 在人类海马体、背外侧前额叶皮层和结直肠癌组织中验证了方法的有效性。
conclusion: SpatialArtifacts包在Bioconductor和PyPI上免费提供，可进行下游分析。
---

## 摘要
空间转录组学数据常受到技术伪影的影响，如干燥斑块、组织剥离和不均匀的试剂覆盖，这些伪影表现为 UMI 计数较低的区域，尤其是在组织边界处。使用现有的质量控制方法识别这些区域往往具有挑战性。在此，我们介绍 SpatialArtifacts，这是一个结合了基于中位数绝对偏差（MAD）的异常值检测和数学形态学操作的框架，用于识别和分类空间连续的组织伪影。包括 3x3 填充、5x5 轮廓和星形模式连通性在内的局部操作在保留真实生物域的同时连接低质量点。我们使用一个分层分类系统来区分边缘与内部伪影以及大区域与小区域，从而实现下游移除或有针对性的手动审查。我们使用 10x Genomics Visium 和 VisiumHD 平台，在人类海马体、背外侧前额叶皮层和结直肠癌组织中演示了我们方法的性能。我们的 SpatialArtifacts 包在 Bioconductor（https://bioconductor.org/packages/SpatialArtifacts）和 PyPI（https://pypi.org/project/spatial-artifacts/）上免费提供。

## Abstract
Spatial transcriptomics data are frequently compromised by technical artifacts, such as dry patches, tissue lifting, and uneven reagent coverage, which manifests as regions with low UMI counts, in particular at tissue borders. It can often be challenging to identify these regions using existing quality control methods. Here, we present SpatialArtifacts, a framework that combines median absolute deviation (MAD)-based outlier detection with mathematical morphology operations to identify and classify spatially contiguous tissue artifacts. Focal operations including 3x3 fill, 5x5 outline, and star-pattern connectivity link low-quality spots while preserving true biological domains. We use a hierarchical classification system to distinguish edge versus interior artifacts and large versus small regions, enabling downstream removal or targeted manual review. We demonstrate the performance of our method in human hippocampus, dorsolateral prefrontal cortex, and colorectal cancer tissues using 10x Genomics Visium and VisiumHD platforms. Our SpatialArtifacts package is freely available on Bioconductor at https://bioconductor.org/packages/SpatialArtifacts and on PyPI at https://pypi.org/project/spatial-artifacts/.