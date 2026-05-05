---
title: "Information Bottleneck Dominates Adversarial Training for Ancestry-Invariant Polygenic Risk Prediction: Dimensionality, Not Gradient Reversal, Controls the Fairness-Accuracy Tradeoff"
authors: "Tran, P. P., Do, A. T."
date: 2026-04-29
pdf: "https://www.biorxiv.org/content/10.64898/2026.04.24.720752v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 用于公平预测的对抗训练技术，可转移到图像取证中的对抗鲁棒性
tldr: 本研究挑战了对抗性表示学习中梯度反转系数是控制敏感属性不变性的主要因素的假设。通过双流架构进行跨祖先多基因风险评分预测，我们发现潜在维度（信息瓶颈）比对抗强度更能控制祖先泄漏。实验表明，维度变化对泄漏的影响远大于λ变化，且在无对抗训练时，低维度也能实现近似不变性。这建议实践者应优先选择潜在维度来管理公平-准确性权衡。
source: biorxiv
selection_source: fresh_fetch
motivation: 挑战对抗性公平学习中梯度反转系数作为主要控制因素的传统观点。
method: 采用双流架构，结合DCT-II频率域特征和PCA编码，进行跨祖先多基因风险评分预测。
result: 潜在维度比对抗强度更能解释祖先泄漏的方差，维度变化导致泄漏变化46.6个百分点，而λ变化仅2.2个百分点。
conclusion: 对抗性公平社区应优先控制潜在维度来设置公平-准确性权衡的信息预算，而非过度投资于对手工程。
---

## Abstract
In adversarial representation learning for fair prediction, the gradient reversal coefficient ({lambda}) is widely treated as the primary control for sensitive-attribute invariance. We show this assumption is wrong. Using a dual-stream architecture for cross-ancestry polygenic risk score (PRS) prediction, we demonstrate that latent dimensionality -- the information bottleneck -- accounts for 8-27 x more variance in ancestry leakage than adversarial strength. Varying{lambda} across a 20 x range changes leakage by only 2.2 percentage points; varying dimensionality across a 16 x range changes it by 46.6 pp. At dimension 8 with no adversarial training ({lambda} = 0), ancestry leakage is 32.9% (chance = 20%): the bottleneck alone achieves near-invariance. The adversary architecture (linear vs deep MLP) is equally irrelevant (0.6 pp range). We validate this finding across two unrelated domains -- genomic ancestry invariance (6 clinical traits, 1000 Genomes, n = 2,504) and EEG subject invariance (pretrained HFTP + Braindecode dual-domain model, 20 subjects) -- observing consistent dimensionality dominance (12.7:1 ratio in EEG).

For the genomic application, Stream 1 encodes population structure via DCT-II frequencydomain features (136 coefficients); Stream 2 encodes phenotype signal from top PRS SNPs (PCA to 128 dimensions). The architecture works equally well with standard genomic PCA as the ancestry stream (R2 = 0.217 vs 0.222), confirming the contribution is architectural, not encoding-specific. African-ancestry PRS reconstruction R2 improves on all six traits (e.g., +5.1 pp for coronary artery disease). Linear models achieve higher aggregate R2 but fail catastrophically on cross-ancestry transfer (R2 = - 12.45 for African-ancestry CAD). We emphasize that we predict PRS (a computed score), not disease phenotypes; validation on biobank-scale phenotype data is ongoing.

These results suggest the adversarial fairness community has been over-investing in adversary engineering relative to simple capacity control. Practitioners should select latent dimensionality first to set the information budget for the fairness-accuracy tradeoff, then optionally use adversarial training for marginal refinement.