---
title: Easy to use and low cost leaf disease quantification workflow using Ilastik
title_zh: 使用 Ilastik 的易用低成本叶片病害量化工作流
authors: "Prouvost, A., Connesson, L., Le Gourrierec, T., Freville, H., David, J., Plessis, C., Magnier, B."
date: 2026-05-16
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.14.719059v1.full.pdf"
tags: ["query:imgfor"]
score: 7.0
evidence: 使用机器学习分割定位图像中的疾病症状区域。
tldr: 传统叶片病害评估方法主观性强、精度有限且难以规模化应用，本研究提出一种基于Ilastik的半自动化图像分析工作流，用于同时量化小麦旗叶的白粉病和黄锈病症状。该工作流结合标准化采样成像、随机森林分割及用户界面，并系统比较四种颜色空间的影响。田间实验验证显示高分割准确性，颜色空间性能差异微小，提供了一种成本低、易用且可重复的深度学习替代方案，支持客观、可扩展的病害表型分析。
source: biorxiv
selection_source: fresh_fetch
motivation: 传统视觉评分方法主观、精度有限且难以规模化，亟需客观可重复的病害评估技术。
method: 开发了半自动化工作流，整合标准化成像、Ilastik中的随机森林分割多症状及用户界面，并比较了四种颜色空间的影响。
result: 在田间实验中，该工作流实现高分割准确性，且不同颜色空间性能差异不大。
conclusion: 该工作流是深度学习方法的低成本、易用替代，能实现可重复、可扩展的病害量化分析。
---

## 摘要
叶片病害严重度的准确和可重复评估对于评估异质植物群落的性能和理解宿主-病原体相互作用至关重要。然而，传统视觉评分方法仍然主观，精度有限，且在大规模表型实验中难以扩展。在此，我们提出一种半自动图像分析工作流，旨在同时量化从小麦品种混合物中采样的旗叶上的多种叶片病害症状。该工作流结合了三个方法组件：(i) 叶片采样和成像的标准化协议，(ii) 使用在 Ilastik 中实现的随机森林进行监督机器学习分割以分类多种症状（白粉病和条锈病），(iii) 一个图形用户界面，便于非专业操作员部署管线。为了评估图像表示对分类性能的影响，系统比较了四种颜色空间（RGB、HSV、HLS、LAB）。该方法使用从田间实验收集的硬粒小麦旗叶图像进行了验证，该实验评估了八种品种混合物在自然真菌压力下的情况。与手动标注图像的交叉验证显示，在所有症状上都有较高的分割准确性。颜色空间之间的比较显示性能差异很小。总体而言，该工作流提供了一种成本效益高、标注效率高且可重复的深度学习方法替代方案，利用开源和积极维护的工具，同时需要有限的训练数据，并实现客观、可重复和可扩展的疾病表型分析。

## Abstract
Accurate and reproducible assessment of foliar disease severity is essential for evaluating the performance of heterogeneous plant communities and understanding host-pathogen interactions. However, traditional visual scoring methods remain subjective, with limited precision, and difficult to scale in large phenotyping experiments. Here, we present a semi-automated image analysis workflow designed to quantify multiple foliar disease symptoms simultaneously on wheat flag leaves sampled from varietal mixtures. The workflow combines three methodological components: (i) a standardized protocol for leaf sampling and imaging, (ii) supervised machine learning segmentation using Random Forest implemented in Ilastik to classify multiple symptoms (powdery mildew and yellow rust), and (iii) a graphical user interface facilitating pipeline deployment by non-specialist operators. To evaluate the influence of image representation on classification performance, four color spaces (RGB, HSV, HLS, LAB) were systematically compared. The approach was validated using images of durum wheat flag leaves collected from a field experiment assessing eight-way varietal mixtures under natural fungal pressure. Cross-validation against manually annotated images demonstrated high segmentation accuracy across all symptom. Comparison among color spaces revealed only minor differences in performance. Overall, this workflow offers a cost-effective, annotation-efficient and reproducible alternative to deep learning approaches, leveraging open-source and actively maintained tools while requiring limited training data and enabling objective, reproducible and scalable disease phenotyping.