import numpy as np
import matplotlib.pyplot as plt

# Configuración general
plt.style.use('default')

# Función sigmoide
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 1. Simple Perceptron
def generate_simple_perceptron():
    # Generar datos
    np.random.seed(42)
    X = np.random.randn(100, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    # Entrenar perceptrón simple
    weights = np.random.randn(2)
    bias = np.random.randn(1)
    learning_rate = 0.1
    
    for _ in range(100):
        output = sigmoid(np.dot(X, weights) + bias)
        error = y - output
        weights += learning_rate * np.dot(X.T, error)
        bias += learning_rate * np.sum(error)
    
    # Visualizar
    plt.figure(figsize=(10, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', alpha=0.6)
    
    # Dibujar línea de decisión
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                        np.arange(y_min, y_max, 0.1))
    Z = sigmoid(np.dot(np.c_[xx.ravel(), yy.ravel()], weights) + bias)
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, [0.5], colors='black')
    
    plt.title('Simple Perceptron Decision Boundary')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.savefig('../../assets/images/simple_perceptron.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. AND Operator
def generate_and_operator():
    # Datos AND
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])
    
    # Entrenar perceptrón AND
    weights = np.random.randn(2, 1)
    bias = np.random.randn(1)
    learning_rate = 0.1
    
    for _ in range(100):
        output = sigmoid(np.dot(X, weights) + bias)
        error = y.reshape(-1, 1) - output
        weights += learning_rate * np.dot(X.T, error)
        bias += learning_rate * np.sum(error)
    
    # Visualizar
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', s=200)
    
    # Dibujar línea de decisión
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                        np.arange(y_min, y_max, 0.1))
    Z = sigmoid(np.dot(np.c_[xx.ravel(), yy.ravel()], weights) + bias)
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, [0.5], colors='black')
    
    plt.title('AND Operator Perceptron')
    plt.xlabel('Input 1')
    plt.ylabel('Input 2')
    plt.xticks([0, 1])
    plt.yticks([0, 1])
    plt.grid(True)
    plt.savefig('../../assets/images/and_perceptron.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. Multi-layer Perceptron (XOR)
def generate_xor_perceptron():
    # Datos XOR
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 1, 1, 0])
    
    # Inicializar pesos
    np.random.seed(42)
    weights_0 = np.random.randn(2, 3)
    weights_1 = np.random.randn(3, 1)
    bias_0 = np.random.randn(1, 3)
    bias_1 = np.random.randn(1, 1)
    learning_rate = 0.1
    
    # Entrenar MLP
    for _ in range(1000):
        # Forward pass
        hidden = sigmoid(np.dot(X, weights_0) + bias_0)
        output = sigmoid(np.dot(hidden, weights_1) + bias_1)
        
        # Backward pass
        error = y.reshape(-1, 1) - output
        delta_1 = error * output * (1 - output)
        delta_0 = np.dot(delta_1, weights_1.T) * hidden * (1 - hidden)
        
        weights_1 += learning_rate * np.dot(hidden.T, delta_1)
        weights_0 += learning_rate * np.dot(X.T, delta_0)
        bias_1 += learning_rate * np.sum(delta_1, axis=0)
        bias_0 += learning_rate * np.sum(delta_0, axis=0)
    
    # Visualizar
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', s=200)
    
    # Dibujar región de decisión
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                        np.arange(y_min, y_max, 0.1))
    
    hidden = sigmoid(np.dot(np.c_[xx.ravel(), yy.ravel()], weights_0) + bias_0)
    Z = sigmoid(np.dot(hidden, weights_1) + bias_1)
    Z = Z.reshape(xx.shape)
    
    plt.contourf(xx, yy, Z, alpha=0.4, cmap='coolwarm')
    plt.contour(xx, yy, Z, [0.5], colors='black')
    
    plt.title('Multi-layer Perceptron (XOR)')
    plt.xlabel('Input 1')
    plt.ylabel('Input 2')
    plt.xticks([0, 1])
    plt.yticks([0, 1])
    plt.grid(True)
    plt.savefig('../../assets/images/xor_perceptron.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    generate_simple_perceptron()
    generate_and_operator()
    generate_xor_perceptron() 