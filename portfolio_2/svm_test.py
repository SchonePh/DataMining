import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

# Datensatz laden
iris = datasets.load_iris()
# Verwende nur die ersten zwei Features für die Visualisierung
X = iris.data[:, :2]
y = iris.target

# Trainings- und Testdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# SVM-Modell trainieren
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# Vorhersagen treffen
y_pred = svm.predict(X_test)

# Ergebnisse ausgeben
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Daten visualisieren


def plot_decision_boundaries(X, y, model):
    h = .02  # Mesh-Gitterweite
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', marker='o')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('SVM Decision Boundaries')
    plt.show()


plot_decision_boundaries(X_test, y_test, svm)
