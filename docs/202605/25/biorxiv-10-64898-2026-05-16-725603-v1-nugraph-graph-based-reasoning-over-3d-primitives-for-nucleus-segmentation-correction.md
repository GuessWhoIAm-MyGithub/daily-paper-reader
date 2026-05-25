---
title: "NuGraph: Graph-Based Reasoning over 3D Primitives for Nucleus Segmentation Correction"
title_zh: NuGraph：基于3D原语的图推理用于核分割校正
authors: "Wang, M., Liu, P., Zhao, Y., Wang, B., Wan, J., Nie, L., Wei, D."
date: 2026-05-19
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.16.725603v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 基于图的方法用于定位分割片段，适用于图像区域定位
tldr: 为修正大规模3D细胞核重建中的分割错误，现有方法如局部成对匹配不足。提出NuGraph图推理框架，基于原子3D原语，使用点云骨干和图注意力进行全局推理，结合对比损失和形状细化。开发自监督数据引擎和NucEMFix基准。NuGraph在基准上F1分数高，显著优于现有方法，减少校对工作量。
source: biorxiv
selection_source: fresh_fetch
motivation: 现有分割错误修正方法依赖局部成对匹配，无法处理全局拓扑，难以恢复缺失形态。
method: 提出NuGraph，基于图推理框架，分解错误掩码为3D原语，使用点云编码和图注意力进行全局关系推理，并通过对比损失和形状细化优化。
result: "NuGraph在NucEMFix基准上F1分数达87.99%和86.20%，优于重新分割和成对修正方法，并减少100倍以上校对努力。"
conclusion: NuGraph为全脑尺度细胞核分割错误修正提供了高效解决方案，结合图推理和自监督训练提升准确性和效率。
---

## 摘要
在大规模3D核重建中校正分割错误需要推理哪些碎片属于同一核，跨越密集区域。现有校正方法依赖于局部成对碎片匹配，无法解决核簇的全局拓扑，并无法恢复缺失的形态。我们提出NuGraph，一个基于图推理的框架，操作于通过分解错误掩模获得的原子3D原语。NuGraph通过3D点云主干编码原语几何，并通过图注意力执行全局关系推理，捕获整个簇中的原语间依赖关系，而不是孤立的对。一个原语提议对比损失将局部原语特征与核级语义对齐，提高密集区域的分组准确性。然后，一个形状精炼网络通过预测符号距离场来精炼这些提议，以恢复平滑的形态。为了在无需手动错误标注的情况下训练，我们开发了一个自监督数据引擎，从干净的核标签合成逼真的分割错误。为了在脑规模上基准校正，我们整理了NucEMFix，这是首个脑范围的EM基准，包含FAFB和MICrONS中的核错误案例（超过8,000个标注错误核）。NuGraph在NucEMFix-F (FAFB) 上达到87.99% F1，在NucEMFix-M (MICrONS) 上达到86.20% F1，超越了重新分割基线（例如，比nnU-Net高8.6%）和成对校正方法，同时将整理工作量相对于手动校对减少了100倍以上。代码和数据可在 https://mingzhiwang618.github.io/NucEMFix 获取。

## Abstract
Correcting segmentation errors in large-scale 3D nuclei reconstructions requires reasoning about which fragments belong to the same nucleus across densely packed regions. Existing correction methods rely on local pairwise fragment matching, which cannot resolve the global topology of nuclear clusters and fails to recover missing morphology. We propose NO_SCPLOWUC_SCPLOWGO_SCPLOWRAPHC_SCPLOW, a graph-based reasoning framework that operates over atomic 3D primitives obtained by decomposing erroneous masks. NO_SCPLOWUC_SCPLOWGO_SCPLOWRAPHC_SCPLOW encodes primitive geometry via a 3D point-cloud backbone and performs global relational reasoning through graph attention, capturing inter-primitive dependencies across entire clusters rather than isolated pairs. A primitive-proposal contrastive loss aligns local primitive features with nucleuslevel semantics, improving grouping accuracy in dense regions. The resulting proposals are then refined by a shaperefinement network that predicts signed distance fields to restore smooth morphology. To train without manual error annotations, we develop a self-supervised data engine that synthesizes realistic segmentation errors from clean nuclei labels. To benchmark correction at brain scale, we curate NucEMFix, the first brain-wide EM benchmark of nuclei error cases across FAFB and MICrONS (8,000+ annotated error nuclei). NO_SCPLOWUC_SCPLOWGO_SCPLOWRAPHC_SCPLOW attains 87.99% F1 on NucEMFix-F (FAFB) and 86.20% on NucEMFix-M (MICrONS), outperforming both re-segmentation baselines (e.g., +8.6% over nnU-Net) and pairwise correction methods, while reducing curation effort by over 100x relative to manual proofreading. Code and data are available at https://mingzhiwang618.github.io/NucEMFix.