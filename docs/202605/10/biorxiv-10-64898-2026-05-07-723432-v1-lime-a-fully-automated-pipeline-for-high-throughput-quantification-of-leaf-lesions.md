---
title: "LIME: a fully automated pipeline for high-throughput quantification of leaf lesions"
title_zh: LIME：一个用于高通量量化叶片病变的全自动流水线
authors: "Tan, D."
date: 2026-05-10
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.07.723432v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 用于病斑量化的图像分割和区域定位
tldr: "叶片病斑的准确量化对植物疾病研究至关重要，但传统方法依赖主观视觉评分和手动分析，效率低且不精确。本文提出了LIME，一个全自动开源管道，通过集成零样本叶片分割和卷积神经网络来高通量量化病斑。应用于拟南芥感染实验，LIME实现了12.9%的平均绝对百分比误差，与人工评分变异相当，处理速度比手动标注快13倍，为标准化病理测定提供了客观、可重复的解决方案。"
source: biorxiv
selection_source: fresh_fetch
motivation: 现有叶片病斑量化方法依赖主观评分和手动分析，限制了研究效率和准确性。
method: LIME集成零样本叶片分割模型和卷积神经网络，构建全自动图像分析管道进行病斑面积估计。
result: "实验表明LIME误差为12.9%，处理200叶片仅需15分钟，比手动标注快13倍，且深度学习模型优于传统方法。"
conclusion: LIME作为开源工具，支持植物病理学中叶片病斑的客观、可重复和可扩展量化。
---

## 摘要
精确量化叶片病变的严重程度对于植物病害研究和表型分析至关重要，但常常受限于主观的视觉评分和耗时的手动图像分析。我们提出了LIME，一个全自动、开源的图像分析流水线，用于从病害测定图像中高通量量化叶片病变。LIME整合了使用Segment Anything Model的零样本叶片分割与卷积神经网络，用于病变面积估计。应用于感染核盘菌的拟南芥叶片，所提出的方法达到了12.9%的平均绝对百分比误差，与手动评分中观察到的评分者内变异性相当。跨病变大小组的分层评估显示，对于小、中、大病变，预测准确性一致，并且比较分析表明，基于深度学习的模型显著优于基于颜色的基线方法。在GPU加速执行下，LIME在15分钟内处理了包含约200片叶子的完整测定，与手动标注相比，处理时间减少了约13倍。综上所述，这些结果表明，LIME能够实现标准化植物病理学测定中叶片病变严重程度的客观、可重现和可扩展的量化。该流水线作为开源工具发布，以支持定量表型研究。

## Abstract
Accurate quantification of leaf lesion severity is essential for plant disease research and phenotyping but is often limited by subjective visual scoring and time-intensive manual image analysis. We present LIME, a fully automated, open-source image analysis pipeline for high-throughput quantification of leaf lesions from disease assay images. LIME integrates zero-shot leaf segmentation using the Segment Anything Model with a convolutional neural network for lesion area estimation. Applied to Arabidopsis thaliana leaves infected with Sclerotinia sclerotiorum, the proposed approach achieved a mean absolute percentage error of 12.9%, comparable to observed intrarater variability in manual scoring. Stratified evaluation across lesion-size groups demonstrated consistent prediction accuracy for small, intermediate, and large lesions, and comparative analysis showed that the deep learning-based model substantially outperformed color-based baseline methods. Under GPU-accelerated execution, LIME processed complete assays containing approximately 200 leaves in 15 minutes, representing an approximate 13-fold reduction in processing time relative to manual annotation. Together, these results indicate that LIME enables objective, reproducible, and scalable quantification of leaf lesion severity in standardized plant pathology assays. The pipeline is released as an open-source tool to support quantitative phenotyping studies.