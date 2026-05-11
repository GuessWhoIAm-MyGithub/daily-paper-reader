---
title: Uncertainty-aware localization microscopy by variational diffusion
title_zh: 基于变分扩散的不确定性感知定位显微镜
authors: "Seitz, C., Liu, J."
date: 2026-05-05
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.01.722206v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 使用扩散模型在图像中进行定位
tldr: 在单分子定位显微镜中，深度神经网络用于核密度估计以加速超分辨率成像，但密集图像定位是具有多个可能解的逆问题。本文提出基于条件变分扩散模型（CVDM）的生成建模框架，用于建模高分辨率核密度估计的概率分布，从而能够估计不确定性并实现高保真超分辨率成像。
source: biorxiv
selection_source: fresh_fetch
motivation: 为了在单分子定位显微镜中建模不确定性并解决定位问题中多个可能解的挑战。
method: 采用条件变分扩散模型（CVDM）进行生成建模，以建模高分辨率核密度估计的概率分布。
result: 模型实现了高保真超分辨率成像并能够估计回归核密度估计的不确定性。
conclusion: 该方法对单分子和超分辨率显微镜的图像恢复具有重要应用意义。
---

## 摘要
利用深度神经网络从图像中快速提取物理相关信息，已导致荧光显微镜及其在生物系统研究中的应用取得显著进展。例如，在单分子定位显微镜（SMLM）中应用深度网络进行核密度（KD）估计，已加速了细胞中密集标记结构的超分辨率成像。然而，在密集图像中定位荧光分子是一个困难的逆问题，可能存在多个解决方案。为了对该问题的解决方案进行概率分布建模，我们提出了一种基于条件变分扩散模型（CVDM）的生成建模框架，用于SMLM中的KD估计。在这个框架中，CVDM通过建模高分辨率KD估计的分布，在低分辨率测量上执行定位任务。这种方法使我们能够探测KD估计分布的结构并表达不确定性，这是现有定位显微镜深度模型目前所不具备的。我们证明，该模型允许高保真超分辨率，能够对回归的KD估计进行不确定性估计，并对单分子和超分辨率显微镜中的图像恢复具有重要意义。

## Abstract
Fast extraction of physically relevant information from images using deep neural networks has led to significant advances in fluorescence microscopy and its application to the study of biological systems. For example, the application of deep networks for kernel density (KD) estimation in single-molecule localization microscopy (SMLM) has accelerated super-resolution imaging of densely labeled structures in the cell. However, localization of fluorescent molecules in dense images is a difficult inverse problem with potentially multiple solutions. To model a probability distribution of solutions to this problem, we propose a generative modeling framework for KD estimation in SMLM based on a conditional variational diffusion model (CVDM). In this framework, CVDM is trained to perform localization tasks on low-resolution measurements by modeling a distribution of high-resolution KD estimates. This approach allows us to probe the structure of the distribution on KD estimates and express uncertainty, which is not currently offered by existing deep models for localization microscopy. We demonstrate that this model permits high-fidelity super-resolution, enables the uncertainty estimation of regressed KD estimates, and has important implications for image restoration in single-molecule and super resolution microscopy.