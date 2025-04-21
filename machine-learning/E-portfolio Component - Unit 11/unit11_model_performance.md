# Model Performance Measurement – AUC and R² Exploration

This notebook explores how changing model parameters impacts the **Area Under the Curve (AUC)** and the **R² score**, two widely used evaluation metrics in classification and regression tasks respectively.

## CNN Model Review Summary

The provided notebook walks through model performance metrics such as:
- Accuracy
- Precision
- Recall
- F1-score
- ROC AUC
- Mean Squared Error (MSE)
- Mean Absolute Error (MAE)
- R² Score

Below are two key experiments and code blocks used to explore how parameter changes impact AUC and R².

## 1. AUC with Varying Regularization (Logistic Regression)

We used the breast cancer dataset to train a Logistic Regression model with different regularization strengths (parameter `C`). A lower `C` implies stronger regularization, which can lead to underfitting, while a very high `C` may overfit.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import numpy as np

X, y = load_breast_cancer(return_X_y=True)

# Try different regularization strengths
for C in [0.01, 0.1, 1, 10, 100]:
    clf = LogisticRegression(solver="liblinear", C=C, random_state=42)
    clf.fit(X, y)
    auc_score = roc_auc_score(y, clf.predict_proba(X)[:, 1])
    print(f"AUC with C={C}: {auc_score:.4f}")
```

## 2. R² Score with Different Prediction Quality

We compared R² scores for predictions of varying quality to observe how it reacts to error levels.

```python
from sklearn.metrics import r2_score

# Original values
y_true = [3, -0.5, 2, 7]

# Perfect prediction
y_pred_1 = [3, -0.5, 2, 7]
print("Perfect prediction R²:", r2_score(y_true, y_pred_1))

# Slightly off
y_pred_2 = [2.5, 0.0, 2, 8]
print("Slightly off prediction R²:", r2_score(y_true, y_pred_2))

# Bad prediction
y_pred_3 = [0, 0, 0, 0]
print("Bad prediction R²:", r2_score(y_true, y_pred_3))
```

## Ethical and Professional Considerations

These metrics are more than numbers. For instance:
- **A high AUC** may look good but can hide poor recall on minority classes, leading to unfair treatment in healthcare or finance.
- **R²** can be misleading if not interpreted with residual patterns, particularly if models are deployed in policy-sensitive areas like energy forecasting or housing.

As machine learning professionals, we must:
- Choose metrics aligned with the real-world use case
- Clearly document parameter choices and their impact
- Avoid metric over-optimization without considering fairness, explainability, and real-world impact

Metrics are tools, not truths. Responsible model evaluation requires a critical mindset.
