---
title: "zFISHer: Automated 3D Registration, Detection, and Colocalization with Interactive Curation for Sequential Multiplexed FISH"
title_zh: zFISHer：用于序列多重荧光原位杂交的自动化3D配准、检测与共定位及交互式策展系统
authors: "Staller, S. A., Valentine, V., Burden, S."
date: 2026-05-21
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.19.726314v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 为FISH提供自动化3D注册和检测，其定位技术可转移到图像取证
tldr: zFISHer是针对顺序多重荧光原位杂交（FISH）三维图像分析的开源工具，解决了共定位分析中的劳动密集型瓶颈。它自动化了核分割、斑点检测、多轮图像注册、坐标变换等步骤，并集成交互式编辑工具和批处理模式，实现高通量分析，提升了效率和准确性。
source: biorxiv
selection_source: fresh_fetch
motivation: 为了解决sequential multiplexed FISH中三维共定位分析效率和准确性不足的问题。
method: zFISHer是一个基于napari的开源应用，提供自动化图像处理、交互式策展工具和批处理功能，包括核分割、检测、注册和共定位分析。
result: 实现了端到端的自动化分析，支持高通量数据集的批处理，并提供了实时交互编辑等增强功能。
conclusion: zFISHer作为开源工具发布在GitHub上，促进了sequential multiplexed FISH研究的自动化和标准化。
---

## 摘要
摘要序列多重荧光原位杂交（FISH）能够实现细胞单层中空间分辨的分子谱分析，但跨三维数据集的斑点共定位分析仍是耗时耗力的瓶颈环节。zFISHer是一个基于napari查看器构建的开源应用程序，它结合交互式用户策展工具，实现了序列FISH图像处理的全流程自动化。zFISHer提供配对FISH数据集的端到端分析，涵盖细胞核分割、非对齐z轴堆栈上的自动斑点检测、基于平移约束RANSAC（可选B样条可变形配准）的多轮图像配准、斑点坐标到对齐空间的精确变换、共识细胞核生成、具有实时碰撞检测功能的交互编辑，以及配对与三通道共定位统计分析。其中包括一个“钓鱼钩”光线投射算法，该算法通过识别沿相机射线的强度最大值来定位斑点的真实三维质心，从而消除手动z层导航需求，并辅以亚体素体积优化。内置的批处理模式支持对多个实验数据集进行高通量无人值守分析。

可用性与实现zFISHer基于MIT许可证开源，可在GitHub免费获取：https://github.com/stjude/zFISHer。示例数据集（去卷积的ND2图像堆栈）归档于Zenodo：https://doi.org/10.5281/zenodo.20288536。zFISHer采用Python开发，利用napari查看器作为交互界面。文档和示例数据集的预期测试输出可在GitHub查阅：https://github.com/stjude/zFISHer。若需报告zFISHer使用问题或参与贡献，请在GitHub仓库提交issue：https://github.com/stjude/zFISHer/issues。

联系方式Seth.Staller@STJUDE.ORG

补充信息补充数据可在线获取。

## Abstract
SummarySequential multiplexed fluorescence in situ hybridization (FISH) enables spatially resolved molecular profiling in cell monolayers, but analyzing puncta colocalization across three-dimensional (3D) datasets remains a labor-intensive bottleneck. zFISHer is an open-source application built on the napari viewer that provides complete automation of sequential FISH image processing in conjunction with interactive user-curation tools. zFISHer provides end-to-end analysis of paired FISH datasets, encompassing nuclear segmentation, automated puncta detection on unaligned z-stacks, multi-round image registration via translation-constrained RANSAC with optional B-spline deformable warping, precise transformation of puncta coordinates into aligned space, consensus nuclei generation, interactive editing with real-time collision detection, and pairwise and tri-channel colocalization analysis with statistics. This includes a "Fishing Hook" raycasting algorithm that enables users to locate puncta at their true 3D centroids by identifying intensity maxima along the camera ray, eliminating manual z-slice navigation, complemented by a sub-voxel volume optimization. The included batch processing mode enables high-throughput unattended analysis of multiple experimental datasets.

Availability and ImplementationzFISHer is open source under the MIT license, freely available on GitHub: https://github.com/stjude/zFISHer. The example dataset (deconvolved ND2 image stacks) is archived on Zenodo at https://doi.org/10.5281/zenodo.20288536. zFISHer is developed in Python utilizing the napari viewer for the interface. Documentation and expected test outputs for the sample dataset are available on the GitHub: https://github.com/stjude/zFISHer. To report an issue using zFISHer or contributing to it, please file an issue in the GitHub repository: https://github.com/stjude/zFISHer/issues.

ContactSeth.Staller@STJUDE.ORG

Supplementary InformationSupplementary data are available online.