
from sklearn.metrics import plot_confusion_matrix
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Digits Datensatz laden
digits = datasets.load_digits()
X = digits.data
y = digits.target

# Trainings- und Testdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# SVM-Modell trainieren
svm = SVC(kernel='rbf', gamma=0.001)
svm.fit(X_train, y_train)

# Einige Vorhersagen visualisieren
_, axes = plt.subplots(2, 5, figsize=(10, 5))
images_and_predictions = list(zip(X_test, svm.predict(X_test)))
for ax, (image, prediction) in zip(axes.flatten(), images_and_predictions):
    ax.set_axis_off()
    image = image.reshape(8, 8)
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    ax.set_title(f'Pred: {prediction}')
plt.suptitle('SVM Predictions on Digits Dataset')
plt.show()


# Vorhersagen treffen
y_pred = svm.predict(X_test)

# Verwirrungsmatrix plotten
fig, ax = plt.subplots(figsize=(10, 10))
plot_confusion_matrix(svm, X_test, y_test, ax=ax, cmap=plt.cm.Blues)
plt.title('Confusion Matrix for SVM (RBF Kernel)')
plt.show()


kernels = ['linear', 'poly', 'rbf', 'sigmoid']
accuracies = []

for kernel in kernels:
    svm = SVC(kernel=kernel)
    svm.fit(X_train, y_train)
    accuracies.append(svm.score(X_test, y_test))

plt.figure(figsize=(10, 6))
plt.bar(kernels, accuracies, color=['blue', 'green', 'red', 'purple'])
plt.xlabel('Kernel')
plt.ylabel('Accuracy')
plt.title('SVM Accuracy for Different Kernels')
plt.show()
