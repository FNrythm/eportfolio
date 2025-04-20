# Reflection on Gradient Descent Experiment

## Key Observations

- The cost dropped significantly during the early iterations, showing that the model was learning efficiently.
- No oscillation or divergence was observed at 0.15, which means the learning rate was aggressive but still stable.
- After ~50–60 iterations, improvements in cost became marginal—indicating diminishing returns with additional iterations.

## Dataset Analysis

The experiment used a simple dataset [1,2,3,4,5] with outputs [5,7,9,11,13], which represents a perfect linear relation y = 2x + 3. This clean dataset allowed for clear observation of the gradient descent behavior.

## Personal Reflection

1. This experiment reinforced the importance of tuning the learning rate. A smaller value would have required more iterations to reach the same result, while a larger one could have risked overshooting the optimal point.

2. It also showed how the nature of the dataset matters. This one is small and perfectly linear, so convergence was smooth. On messier, real-world datasets, careful tuning becomes even more critical. 