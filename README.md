# Benchmarking Diffusion Models for Monomeric Protein Structure Prediction
This repository contains the code and datasets used in our study on systematically benchmarking state-of-the-art AI-powered diffusion models for monomeric protein structure prediction. Our analysis focuses on three leading models—AlphaFold 3, Protenix, and Chai-1—evaluating their accuracy, robustness, and ability to detect subtle 3D structural variations in unseen protein structures.

# Benchmarking Diffusion Models for Monomeric Protein Structure Prediction

This repository contains the code and datasets used in our study on systematically benchmarking state-of-the-art AI-powered diffusion models for monomeric protein structure prediction. Our analysis focuses on three leading models—**AlphaFold 3**, **Protenix**, and **Chai-1**—evaluating their accuracy, robustness, and ability to detect subtle 3D structural variations in unseen protein structures.

## Overview

Protein structure prediction is crucial for advancing computational biology, with applications ranging from drug design to understanding biological mechanisms. Recent advancements in diffusion models have revolutionized the field, enabling faster and more accurate predictions. This project explores:

- The predictive performance of AlphaFold 3, Protenix, and Chai-1 on test sets of unseen proteins.
- Sensitivity to single amino acid mutations, analyzing local structural deformation.
- Comparative performance across difficulty levels using metrics like **pLDDT**, **PAE**, **RMSD**, and **pTM**.

## Key Features

- **Dataset**: Includes newly released protein structures from CAMEO (2024) and experimental datasets with mutation-specific comparisons.
- **Metrics**: Comprehensive evaluation using confidence scores, alignment errors, and structural deviations.
- **Code**: Modular implementation for benchmarking diffusion-based prediction models.

## Goals

This repository aims to provide a transparent and reproducible framework for evaluating current AI-driven structural prediction methods, emphasizing their strengths, limitations, and potential for future applications.
Protein structure prediction is crucial for advancing computational biology, with applications ranging from drug design to understanding biological mechanisms. Recent advancements in diffusion models have revolutionized the field, enabling faster and more accurate predictions. This project explores:

The predictive performance of AlphaFold 3, Protenix, and Chai-1 on test sets of unseen proteins.
Sensitivity to single amino acid mutations, analyzing local structural deformation.
Comparative performance across difficulty levels using metrics like pLDDT, PAE, RMSD, and pTM.
Key Features
Dataset: Includes newly released protein structures from CAMEO (2024) and experimental datasets with mutation-specific comparisons.
Metrics: Comprehensive evaluation using confidence scores, alignment errors, and structural deviations.
Code: Modular implementation for benchmarking diffusion-based prediction models.
Goals
This repository aims to provide a transparent and reproducible framework for evaluating current AI-driven structural prediction methods, emphasizing their strengths, limitations, and potential for future applications.
