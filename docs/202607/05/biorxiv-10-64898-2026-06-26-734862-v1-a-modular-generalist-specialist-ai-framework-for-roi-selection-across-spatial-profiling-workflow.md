---
title: A modular generalist-specialist AI framework for ROI selection across spatial profiling workflow
title_zh: 一种用于空间分析工作流程中ROI选择的模块化通才-专家AI框架
authors: "Castillo, S. P., Gautam, T., Pinao Gonzales, K. B., Salvatierra, M. E., Serrano, A., Ercan, C., Rodriguez, B. L., Acosta, P., Chen, P., Shokrollahi, Y., Lau, A., Kwong, L. N., Huse, J. T., Pan, X., Patient Mosaic Team,, Solis Soto, L. M., Yuan, Y."
date: 2026-07-01
pdf: "https://www.biorxiv.org/content/10.64898/2026.06.26.734862v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: AI引导的图像感兴趣区域选择
tldr: 本研究针对空间分子分析中ROI选择面临的可重复性和效率挑战，开发了一个模块化通才-专才AI框架。通过构建蛋白质分析参考图谱和ASTROS模型，在55种肿瘤类型数据上验证，混合策略在信号保留、一致性及计算效率间取得平衡，支持虚拟染色等应用，以减少评分者间差异并提升实验可重复性。
source: biorxiv
selection_source: fresh_fetch
motivation: ROI选择对空间分子分析的可重复性和生物可解释性至关重要，但现有方法存在评分者间差异和效率问题。
method: 我们开发了ASTROS模型和模块化通才-专才AI框架，基于蛋白质参考图谱进行跨平台ROI选择。
result: 混合通才-专才策略在幻灯片信号保留、病理学家参考一致性和计算效率上表现最优，并验证了虚拟染色和多种空间组学技术的可行性。
conclusion: 该框架为ROI选择提供了高效、可重复的解决方案，有助于减少评分者间差异并增强空间分析实验的多功能性。
---

## 摘要
感兴趣区域（ROIs）的选择通常是空间分子分析和许多病理学任务中的关键步骤，对研究可重复性和生物可解释性有重要影响。为了提供一个可重复且自适应的AI指导ROI选择框架，我们开发了一个跨空间分析平台的模块化通才-专家解决方案。在一个包含160名组织供体的55种肿瘤类型队列中，使用NanoString数字空间分析和多重免疫荧光进行分析，我们首先建立了一个蛋白质分析参考图谱，捕获了特定区室的免疫、检查点、基质和增殖模式。然后，我们开发了一个用于ROI选择的AI专家任务导向模型（ASTROS），并测试了综合基准，考虑了仅专家（ASTROS）、仅通才（PLIP/GFM）和混合通才-专家策略，显示后者在幻灯片水平信号保留、病理学家参考一致性、幻灯片内放置一致性和大幻灯片计算效率方面提供了平衡的权衡。我们进一步证明了虚拟染色用于ROI预览以及模块化ROI放置用于其他空间组学技术（Visium和Visium HD工作流程）的可行性。这些结果共同支持我们提出的框架，以实现ROI选择，满足减少评分者间变异性、可重复性和空间分析实验多功能性的未满足需求。

## Abstract
Selection of regions of interest (ROIs) is often a crucial step in spatial molecular profiling and many pathology tasks, with substantial implications for research reproducibility and biological interpretability. To provide a reproducible and adaptive framework for AI-guided ROI selection, we developed a modular generalist-specialist solution across spatial profiling platforms. In a cohort comprising 55 tumor types from 160 tissue donors profiled using NanoString Digital Spatial Profiling and multiplex immunofluorescence, we first established a protein-profiling reference atlas capturing compartment-specific immune, checkpoint, stromal, and proliferation patterns. We then developed an AI Specialist Task-Oriented Model for ROI Selection (ASTROS) and tested comprehensive benchmarks considering specialist-only (ASTROS), generalist-only (PLIP/GFM), and hybrid generalist-specialist strategies, showing that the latter provides a balanced tradeoff across slide-level signal preservation, pathologist-reference concordance, within-slide placement consistency, and large-slide computational efficiency. We further demonstrated the feasibility of virtual staining for ROI preview and modular ROI placement for other spatial omics technologies, Visium and Visium HD workflows. Together, these results support our proposed framework to enable ROI selection responding to unmet needs for reducing inter-rater variability, reproducibility, and versatility in spatial profiling experiments.