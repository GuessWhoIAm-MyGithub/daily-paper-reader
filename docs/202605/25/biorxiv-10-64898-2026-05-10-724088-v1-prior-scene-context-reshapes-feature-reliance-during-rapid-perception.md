---
title: Prior scene context reshapes feature reliance during rapid perception
title_zh: 先前场景情境重塑快速感知中的特征依赖性
authors: "Tasliyurt-Celebi, S., de Haas, B., L.-H. Vo, M., Dobs, K."
date: 2026-05-18
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.10.724088v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 利用先验上下文改进自然场景中的人脸检测。
tldr: 本研究探讨先验场景上下文如何影响快速视觉感知，特别是人脸检测。通过结合眼动追踪和特征编码模型的两个实验，操纵场景预览和周边视觉输入。结果表明，先验上下文促进检测，尤其对挑战性图像，并在首次眼动中显现，表明上下文从一开始就塑造感知策略。建模显示感官信息和空间先验均影响延迟，但上下文增加空间先验依赖，减少感官驱动特征使用，揭示了信息平衡的转变。
source: biorxiv
selection_source: fresh_fetch
motivation: 探索先验场景上下文对快速视觉感知的影响机制。
method: 结合眼动追踪和基于特征的编码模型，通过实验操纵场景预览和视觉输入来测试快速人脸检测。
result: 先验上下文促进人脸检测，改变信息依赖，增加空间先验的贡献并减少感官驱动特征的使用。
conclusion: 先前场景上下文将快速感知中的特征依赖从感官驱动转向基于期望的空间指导。
---

## 摘要
人类感知由感觉输入和先前知识或期望共同塑造。但先前的背景信息如何影响快速视觉处理？本研究在两项实验中结合眼动追踪与基于特征的编码模型，预测核心视觉任务中的检测潜伏期：自然场景中的快速人脸检测（每项实验N=38）。第一项实验操控了无人脸场景预览的存在性。第二项实验通过移动窗口范式进一步限制外周视觉输入，从而增强对先前信息的依赖。两项实验均表明，先前情境促进了人脸检测，尤其对于具有挑战性的图像。这种促进效应在首次眼动中就已显现，表明预览从一开始就塑造了感知策略。为量化引导行为的信息，我们使用一组基于图像的预测因子建模检测潜伏期，这些因子捕获了（i）感觉信息和（ii）场景衍生的空间先验：预期的人脸位置。两类预测因子均解释了图像间的潜伏期变化。在感觉预测因子中，人脸存在引发的深度神经网络反应差异对检测潜伏期的样本外预测力最强。关键的是，当场景预览可用时，空间先验的贡献增加，而对感觉驱动特征的依赖普遍降低。这些发现共同表明，先前场景情境将快速人脸检测所用信息的平衡从感觉驱动转向了基于期望的空间引导。

## Abstract
Human perception is shaped by both sensory input and prior knowledge or expectations. But how does prior contextual information influence rapid visual processing? Here, we combined eye tracking with feature-based encoding models across two experiments to predict detection latencies in a core visual task: rapid face detection in natural scenes (N = 38 per experiment). In the first experiment, we manipulated the presence of faceless scene previews. In the second experiment, we additionally restricted peripheral visual input using a moving-window paradigm, thereby increasing reliance on prior information. Across both experiments, prior context facilitated face detection, particularly for challenging images. This facilitation was already evident in the very first eye movement, suggesting that previews shape perceptual strategies from the outset. To quantify what information guided behavior, we modeled detection latencies using a set of image-based predictors capturing (i) sensory information and (ii) a scene-derived spatial prior: the expected face location. Both predictor classes explained latency variation across images. Among sensory predictors, the difference in deep neural network responses induced by the presence of the face provided the strongest out-of-sample prediction of detection latency. Critically, when scene previews were available, the contribution of the spatial prior increased, while reliance on sensory-driven features was generally reduced. Together, these findings indicate that prior scene context shifts the balance of information used for rapid face detection from sensory-driven to expectation-based spatial guidance.