# Project
State shortly what you did during each week. Just a table with the main results is enough. Remind to upload a brief presentation (pptx?) at virtual campus. Do not modify the previous weeks code. If you want to reuse it, just copy it on the corespondig week folder.

#### Team 7
* Marco Cordón
* Iñaki Lacunza
* Cristian Gutiérrez

## Bag of Visual Words (BoVW) classification
Our tuned model with the optimized parameters is **Dense SIFT with PCA and SVM clf** which obtained a maximum Test Accuracy score of 83.02 during an Optuna optimization run.

```
Step size = 18
Number of Features = 185
Octave Layers = 2
k_codebook = 198
Classifier = SVM (with RBF Kernel)
PCA (with 109 components)
```

We cross-validated every experiment and decided to use it as our metric of choice to decide for an improvement:
|    | Test Accuracy | Cross-validation Score |
| -- | ------------- | ---------------------- |
| SIFT | 59.11 | 57.99 |
| SIFT (w/ LDA) | 62.95 | 66.26 |
| Dense SIFT | 76.95 | 76.53 |
| Dense SIFT & Scale x2 |63.44| 62.72 |
| Dense SIFT & Scale x4 |36.68| 36.76 |
| Dense SIFT (w/ PCA) |77.08| 76.01 |
| Dense SIFT (w/ LDA) |78.44| 81.69 |
| Dense SIFT (w/ LDA + StandardScaler) |78.07| 81.03 |
| Dense SIFT (w/ LDA + MinMax) |78.93| 82.10 |
| Dense SIFT (w/ LDA + Normalizer) |79.43| 81.58 |
| Dense SIFT (K = 198) |78.81| 77.20 |
| Dense SIFT (w/ PCA) & (K = 198) |76.33| 76.56 |
| Dense SIFT (w/ LDA) & (K = 198) |80.17| 84.71 |
| Dense SIFT (KNN Dist = Euclidean) |78.81| 77.2 |
| Dense SIFT (KNN Dist = Cosine) |75.96| 75.74 |
| Dense SIFT (KNN Dist = Jaccard) |73.98| 73.4 |
| Dense SIFT + SVM (Kernel = Linear) |78.56| 77.53 |
| Dense SIFT + SVM (Kernel = RBF) |82.90| 82.78 |
| Dense SIFT + SVM (Kernel = Hist Inters) |81.41| 80.06 |
| Dense SIFT (w/ PCA) + SVM (Kernel = Linear) |78.93| 77.42 |
| Dense SIFT (w/ PCA) + SVM (Kernel = RBF) |83.02| 81.32 |
| Dense SIFT (w/ PCA) + SVM (Kernel = Hist Inters) |79.93| 78.57 |
| Dense SIFT (w/ LDA) + SVM (Kernel = Linear) |81.66| 86.27 |
| Dense SIFT (w/ LDA) + SVM (Kernel = RBF) |80.67| 86.42 |
| Dense SIFT (w/ LDA) + SVM (Kernel = Hist Inters) |80.55| 85.34|
| Dense SIFT + SVM (Spatial Pyramids Level = 2) | 81.29 | - |
| Dense SIFT (w/ PCA) + SVM (Spatial Pyramids Level = 2) | 81.91| - |
| Fisher Vectors (GMM n_components = 64) | 78.93 | - |
| Fisher Vectors + PCA n_components = 69 (GMM n_components = 64) | 79.43 | - |
| Fisher Vectors + LDA n_components = 7 (GMM n_components = 64) |  58.24| - |



## Task2 work

## Task3 work

## Task4 work
