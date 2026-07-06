---
title: "dSTORMQuant: A Python Package for Post-Processing and Quantitative Analysis of SMLM datasets"
title_zh: dSTORMQuant：一个用于SMLM数据集后处理与定量分析的Python包
authors: "Karki, S., Nemeita, B., Hammann, A. S., Thoms, S."
date: 2026-07-03
pdf: "https://www.biorxiv.org/content/10.64898/2026.06.30.735216v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 提供用于定位数据分析的Python包；涉及图像区域定位。
tldr: 单分子定位显微镜（SMLM）技术如(d)STORM和PALM能突破衍射极限，可视化亚细胞分子组织，但数据采集慢且下游分析复杂耗时，限制了实验规模和统计能力。为此，我们开发了dSTORMQuant，一个开源Python包，用于自动化、高通量地处理和分析SMLM定位数据，实现高效数据处理，减少手动干预，提升研究可靠性和效率。
source: biorxiv
selection_source: fresh_fetch
motivation: 数据处理复杂耗时限制了SMLM研究的统计能力和生物可靠性。
method: 开发了开源Python包dSTORMQuant，用于自动化高通量后处理和定量分析SMLM数据。
result: 该包能高效处理大量数据集，最小化手动干预，提高研究效率。
conclusion: dSTORMQuant在GitHub上免费可用，采用GPL v3许可证。
---

## 摘要
摘要：单分子定位显微技术，如（直接）随机光学重建显微镜（(d)STORM）和光激活定位显微镜（PALM），使得在超越传统光学显微镜衍射极限的条件下可视化亚细胞分子组织成为可能。不仅数据采集相当缓慢，而且定位数据集的下游分析通常计算上具有挑战性且耗时。因此，数据处理的复杂性和持续时间常常限制实验仅能采集和分析少量细胞或感兴趣区域，从而限制了SMLM研究的统计功效和生物学可靠性。为了解决这一限制，我们开发了一个开源的基于Python的包，用于自动化、高通量的SMLM定位数据后处理和定量分析，使得能够高效且直接地处理大量数据集，且仅需最少的人工干预。可用性和实现：dSTORMQuant（源代码和文档）在GitHub上免费提供，地址为https://github.com/BCMM-Bielefeld-University/dSTORMQuant，采用GPL v3许可证。

## Abstract
Summary: Single-molecule localization microscopy techniques, such as (direct) stochastic optical reconstruction microscopy ((d)STORM) and photo-activated localization microscopy (PALM) enable the visualization of subcellular molecular organization beyond the diffraction limit of conventional light microscopy. Not only is data acquisition rather slow, but the downstream analysis of localization datasets often remains computationally challenging and time-consuming. Consequently, the complexity and duration of data processing often limit experiments to the acquisition and analysis of only small numbers of cells or regions of interest, thereby restricting the statistical power and biological reliability of SMLM studies. To address this limitation, we developed an open-source Python-based package for automated, high-throughput post-processing and quantitative analysis of SMLM localization data, enabling efficient and straightforward handling of extensive datasets with minimal manual intervention. Availability and implementation: dSTORMQuant (source code and documentation) are freely available on GitHub at https://github.com/BCMM-Bielefeld-University/dSTORMQuant under GPL v3 license.