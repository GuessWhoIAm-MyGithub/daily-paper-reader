---
title: "ATI_Box: A Simple tool for convolutional neural network-based image semantic segmentation"
title_zh: ATI_Box：一种基于卷积神经网络的简单图像语义分割工具
authors: "Przygodzki, T."
date: 2026-06-02
pdf: "https://www.biorxiv.org/content/10.64898/2026.05.29.728143v1.full.pdf"
tags: ["query:imgfor"]
score: 6.0
evidence: CNN图像分割工具用于区域定位
tldr: 在生物医学研究中，CNNs用于图像语义分割很有用，但训练过程复杂，非编码研究人员难以采用。作者提出ATI_Box平台，整合标注、存储、训练、评估和分析功能，基于U-Net和MinIO，提供端到端用户友好解决方案，可用于实验室实践和教育场景。
source: biorxiv
selection_source: fresh_fetch
motivation: 为了帮助非编码研究人员克服CNNs应用的困难，提供一个简化且易用的图像语义分割工具。
method: 开发ATI_Box平台，集成Label Studio标注、MinIO存储、U-Net模型训练和评估，实现端到端工作流。
result: 平台在实验室实践中展示了可用性，提供像素级和对象级评估指标，支持批量分析。
conclusion: ATI_Box作为非编码工具，既可用于基本生物医学图像分析，也可作为教育平台介绍语义分割基础。
---

## 摘要
显微图像的定量分析已成为基础生物和生物医学研究的标准。深度机器学习为此过程提供了强大的工具。然而，对于缺乏基本编码技能的研究人员来说，将深度机器学习实际应用于图像分析可能很困难。这是由于非编码解决方案有限，特别是在卷积神经网络（CNN）领域。这种稀缺性可以用以下悖论来解释：CNN的训练是一个相对复杂的过程；熟悉此过程的研究人员也足够熟练，能够编码CNN实现的完整流程，从注释、模型训练和评估到其在实验室实践中的使用。任何更广泛研究人员可接受的替代方案，如果他们不熟悉CNN概念，都不可避免地会导致整个过程的简化，特别是训练步骤。这种简化反过来可能导致此类工具解决特定问题的局限性。然而，作者认为，在复杂性和简单性之间可以找到一些妥协，足以解决基础生物和生物医学研究领域的一些基本问题。为应对这一挑战，作者提出了ATI_Box（注释、训练、推理一体化），这是一个统一的、用户导向的端到端图像语义分割平台。该系统将数据注释、存储、模型训练、评估和定量分析集成到一个单一工作流程中，显著简化了模型开发过程。图像和注释数据通过S3兼容的对象存储系统（MinIO）管理，实现可扩展和透明的数据处理。注释过程通过Label Studio实现。模型训练基于卷积神经网络U-Net架构，使用ResNet作为编码器。模型评估在训练期间留出的地面真值数据集上进行，并提供像素级和对象级评估指标。批量分析模式使模型预测的自动化量化成为可能，如对象计数和覆盖区域。平台的可用性通过实验室实践中的示例展示。该平台故意缺乏模型调优功能，因为它针对不熟悉深层机器学习概念的用户。同时，访问模型训练的基本功能，如定义轮数或保存和实施训练好的模型版本，使人们能够进行一些基本的分析实验。因此，该平台不仅可以作为分析工具，还可以作为教育解决方案，解释语义分割过程的实际基础。

## Abstract
Quantitative analysis of microscopic images has become a standard in basic biological and biomedical research. Deep machine learning provided a powerful tool facilitating this process. However, practical adoption of deep machine learning to image analysis may be difficult for a researcher who lacks basic coding skills. This is caused by a limited number of non-coding solutions, specifically in the domain of convolutional neural networks (CNNs). This scarcity may be explained by the following paradox. Training of CNNs is a relatively complex process. Researchers who are familiar with this process are also skilled enough to code the full pipeline of CNN implementation from annotation, through model training and evaluation to its usage in laboratory practice. Any kind of an alternative solution, acceptable by a broader group of researchers who are unfamiliar with CNN concepts, must inevitably result in simplification of the entire process, specifically the training step. Such simplification in turn may lead to limitation to solve specific problems by such a tool. Author believes however, that some compromise may be found between complexity and simplicity that would be sufficient to solve some basic problems in the field of basic biological and biomedical research.

To address this challenge, author proposes ATI_Box (Annotation, Training, Inference in One Box), a unified, user-oriented platform for end-to-end image semantic segmentation. The system integrates data annotation, storage, model training, evaluation, and quantitative analysis into a single workflow, significantly simplifying the model development process. Image and annotation data are managed through an S3-compatible object storage system (MinIO), enabling scalable and transparent data handling. Annotation process is implemented through Label Studio. Model training is based on convolutional neural network U-Net architecture with ResNet as an encoder. Model evaluation is performed on ground-truth dataset held-out during training and provides pixel-level and object-level evaluation metrics. Batch analysis mode enables automated quantification of model predictions such as object counts and coverage areas. The usability of the platform was presented on examples from laboratory practice.

The platform is intentionally devoid of model-tuning capabilities as it is addressed to users unfamiliar with profound machine learning concepts. At the same time, accessibility of such basic features of model training as definition of epochs number or saving and implementing of trained model versions enables one to perform some basic analytical experiments. As such, the platform may serve not only as an analytical tool but also as an educational solution to explain practical basics of semantic segmentation process.