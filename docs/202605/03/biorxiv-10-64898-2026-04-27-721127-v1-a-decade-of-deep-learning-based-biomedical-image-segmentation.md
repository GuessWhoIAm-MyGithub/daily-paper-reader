---
title: A Decade of Deep Learning-based Biomedical Image Segmentation
title_zh: 基于深度学习的生物医学图像分割的十年
authors: "Yu, S., Wang, H., Wang, N., Chen, S., Wu, J., Yuan, Z., Qi, T., Zhou, Z., Xia, F., Ma, J., Zhou, Y."
date: 2026-04-30
pdf: "https://www.biorxiv.org/content/10.64898/2026.04.27.721127v1.full.pdf"
tags: ["query:imgfor"]
score: 8.0
evidence: 综述深度学习在生物医学图像分割中的应用，一种区域定位技术。
tldr: 本文综述了过去十年基于深度学习的生物医学图像分割的演变，从任务特定模型转向通用基础模型。分析了局部判别学习的局限性如何推动transformer和生成预训练的发展。主要贡献是引入了首个系统性的可提示分割分类法，将方法分为六类，便于用户选择提示策略，并讨论了数据集、评估和应用适应的进展。
source: biorxiv
selection_source: fresh_fetch
motivation: 动机是分析生物医学图像分割领域从专家模型到基础模型的演变，并提供系统分类以指导实践。
method: 方法是通过深入综述，提出首个可提示生物医学图像分割的系统分类法。
result: 结果是建立了六类可提示分割方法的分类，并概述了相关技术进展。
conclusion: 结论是基础模型在生物医学分割中潜力巨大，但需解决信任和临床集成问题。
---

## 摘要
生物医学图像分割是计算生物医学中的一个基本问题，旨在精确描绘生物医学图像中的解剖和生物结构、组织类型或病理区域。准确的分割对于广泛的生物和医学应用中的解释、决策和定量分析至关重要。在过去十年中，该领域经历了深刻的范式转变，从任务特定的专业模型演变为通用基础模型。本综述深入分析了这一演变过程，追溯了局部判别学习的局限性如何推动了向基于Transformer的全局建模和大规模生成式预训练的转变。为了帮助导航交互范式的多样化景观，我们引入了首个可提示生物医学图像分割的系统分类法，将现有方法分为六种不同类型，使用户能够基于视觉演示直观地选择适当的提示策略，并快速定位相关文献（\href{https://suhaoyu1020.github.io/MedicalSegmentation-PromptType-Website/}{提示类型可视化}）。除了模型架构，我们还讨论了数据集开发、评估协议以及跨放射学、病理学和生物学的应用特定适应方面的并行进展。将这些强大的基础模型与严格的领域特定适应相结合，具有改善患者结果和医疗效率的巨大潜力。最后，我们强调了在可信度和临床整合方面必须克服的关键挑战，以实现下一代生物和医学通才的潜力。

## Abstract
Biomedical image segmentation is a fundamental problem in computational biomedicine that aims to precisely delineate anatomical and biological structures, tissue types, or pathological regions in biomedical images. Accurate segmentation is essential for interpretation, decision-making, and quantitative analysis across a wide range of biological and medical applications. Over the past decade, the field has undergone a profound paradigm shift, evolving from task-specific specialist models to universal foundation models. This review provides an in-depth analysis of the evolution, tracing how the limitations of local discriminative learning drove the transition toward transformer-based global modeling, and large-scale generative pre-training. To help navigate the diverse landscape of interaction paradigms, we introduce the first systematic taxonomy of promptable biomedical image segmentation, categorizing existing methods into six distinct types, enabling users to intuitively select appropriate prompting strategies based on visual demonstrations and quickly pinpoint relevant literature (\href{https://suhaoyu1020.github.io/MedicalSegmentation-PromptType-Website/}{Prompt Type Visualization}). Beyond model architectures, we discuss parallel advancements in dataset development, evaluation protocols, and application-specific adaptations across radiology, pathology, and biology. Integrating these powerful foundation models with rigorous domain-specific adaptation has great potential to improve patient outcomes and healthcare efficiency. Finally, we highlight key challenges in trustworthiness and clinical integration that must be overcome to realize the potential of the next generation of biological and medical generalists.