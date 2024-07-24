from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt

# Datensatz laden
iris = datasets.load_iris()
# Verwende nur die ersten zwei Features für die Visualisierung
X = iris.data[:, :2]
y = iris.target
print(X)

# Nur zwei Klassen verwenden: Klasse 0 und Klasse 1
binary_class_mask = y != 2
X_binary = X[binary_class_mask]
y_binary = y[binary_class_mask]


# Daten visualisieren ohne Entscheidungsgrenzen
plt.figure(figsize=(8, 6))
plt.scatter(X_binary[:, 0], X_binary[:, 1], c=y_binary,
            edgecolors='k', cmap=plt.cm.coolwarm)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Daten ohne Entscheidungsgrenzen')
plt.show()


# Trainings- und Testdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(
    X_binary, y_binary, test_size=0.2, random_state=42)

# SVM-Modell trainieren
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# Entscheidungsgrenzen und Margin plotten


def plot_decision_boundaries_with_margins(X, y, model, title, new_points=None, new_labels=None):
    h = .02  # Mesh-Gitterweite
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.coolwarm)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k',
                marker='o', cmap=plt.cm.coolwarm)

    # Support Vectors und Entscheidungsgrenzen
    plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[
                :, 1], s=100, facecolors='none', edgecolors='k', marker='o')
    w = model.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(x_min, x_max)
    yy = a * xx - (model.intercept_[0]) / w[1]
    plt.plot(xx, yy, 'k-')

    # Margin-Linien
    margin = 1 / np.sqrt(np.sum(model.coef_ ** 2))
    yy_down = yy + a * margin
    yy_up = yy - a * margin
    plt.plot(xx, yy_down, 'k--')
    plt.plot(xx, yy_up, 'k--')

    # Neue Punkte hinzufügen (falls vorhanden)
    if new_points is not None:
        plt.scatter(new_points[:, 0], new_points[:, 1], c=new_labels,
                    edgecolors='k', marker='x', cmap=plt.cm.coolwarm, s=100)
        for i, txt in enumerate(new_labels):
            plt.annotate(txt, (new_points[i, 0], new_points[i, 1]),
                         textcoords="offset points", xytext=(0, 10), ha='center')

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.show()


# Plot mit Entscheidungsgrenzen und Margin für den gesamten Datensatz
plot_decision_boundaries_with_margins(
    X_binary, y_binary, svm, 'SVM Entscheidungsgrenzen und Margins (Linear Kernel)')


# Neue Punkte zum Klassifizieren
new_points = np.array([[5.0, 4], [6.5, 3.0], [4.5, 2.5]])
new_labels = svm.predict(new_points)

# Punkte und neue Klassifizierungen visualisieren
plot_decision_boundaries_with_margins(
    X_binary, y_binary, svm, 'SVM Entscheidungsgrenzen und Margins mit neuen Punkten', new_points, new_labels)
