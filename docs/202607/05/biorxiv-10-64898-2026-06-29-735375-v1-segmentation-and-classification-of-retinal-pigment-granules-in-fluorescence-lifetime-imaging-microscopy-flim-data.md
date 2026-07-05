---
title: Segmentation and classification of retinal pigment granules in fluorescence lifetime imaging microscopy (FLIM) data
title_zh: 荧光寿命成像显微镜（FLIM）数据中视网膜色素颗粒的分割与分类
authors: "Ali, M., Ahmad, H. A., Alderzy, H., Hammer, M., Heintzmann, R., Stranik, O."
date: 2026-07-03
pdf: "https://www.biorxiv.org/content/10.64898/2026.06.29.735375v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: 用于定位图像区域的分割算法
tldr: 本研究针对年龄相关性黄斑变性等疾病导致的视网膜色素上皮颗粒荧光变化，提出 Classi4RPE 算法。该方法基于荧光寿命成像数据，采用带种子的分水岭分割颗粒，并依据寿命分布特征将其分类为脂褐质、黑素脂褐质和黑素三类，实现高准确度分割与分类，为定量分析提供高效工具。
source: biorxiv
selection_source: fresh_fetch
motivation: 疾病如年龄相关性黄斑变性引起视网膜色素上皮细胞荧光性质改变，需要精细分析单个荧光颗粒以支持诊断。
method: 提出 Classi4RPE 算法，使用带种子的分水岭分割和基于荧光寿命特征的分类方法。
result: 算法在脂褐质颗粒上达到敏感性和特异性分别为 0.99 和 0.93，在黑素脂褐质颗粒上分别为 0.90 和 0.98，优于手动注释。
conclusion: Classi4RPE 能够超越人类视觉限制，为视网膜色素上皮的定量分析提供稳健工具。
---

## 摘要
年龄相关性黄斑变性（AMD）等疾病引起的视网膜色素上皮（RPE）细胞荧光特性的改变，强调了对单个水平荧光RPE颗粒进行详细分析的必要性。由于这些颗粒的视觉可分离性有限，精确分割和分类它们仍然具有挑战性。在这项研究中，我们提出了Classi4RPE，一种计算算法，旨在基于荧光寿命成像数据准确分割RPE颗粒并将其分类为三个类别——脂褐素（L）、黑色素脂褐素（ML）和黑色素（M），这些数据提供独特的对比度。该方法在一个自定义的Python框架中实现，并采用种子分水岭分割来隔离单个颗粒。脂褐素颗粒被识别为具有较长寿命的高荧光结构，而寿命较短的颗粒则根据它们从中心到边缘的空间寿命分布进一步分析，从而能够区分ML与其他富含黑色素的颗粒。我们的方法实现了高性能，与人工标注的真实值相比，L颗粒的平均灵敏度为0.99，ML颗粒的平均灵敏度为0.90，对应的特异性分别为0.93和0.98。这些结果展示了Classi4RPE超越人类视觉限制的潜力，并为定量RPE分析提供了一个强大的工具。

## Abstract
Alterations of fluorescence properties in retinal pigment epithelium (RPE) cells caused by diseases such as age-related macular degeneration (AMD) highlight the need for detailed analysis of the fluorescent RPE granules at the individual level. Precise segmentation and classification of these granules remain challenging due to their limited visual separability. In this study, we present Classi4RPE, a computational algorithm designed to accurately segment RPE granules and classify them into three categories -- lipofuscin (L), melanolipofuscin (ML), and melanin (M) -- based on fluorescence lifetime imaging data, which provide distinctive contrast. The method is implemented in a custom Python framework and employs seeded watershed segmentation to isolate individual granules. Lipofuscin granules are identified as hyperfluorescent structures with longer lifetimes, while granules with shorter lifetimes are further analyzed based on their spatial lifetime distribution from the center to edge, enabling discrimination of ML from other melanin-rich granules. Our approach achieves high performance, with mean sensitivities of 0.99 for L granules and 0.90 for ML granules, and corresponding specificities of 0.93 and 0.98, respectively, compared to manually annotated ground truth. These results demonstrate the potential of Classi4RPE to surpass human visual limitations and provide a robust tool for quantitative RPE analysis.