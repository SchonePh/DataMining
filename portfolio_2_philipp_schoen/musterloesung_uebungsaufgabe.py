import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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

# Vorhersagen treffen
y_pred = svm.predict(X_test)

# Genauigkeit berechnen
accuracy = accuracy_score(y_test, y_pred)
print(f'Genauigkeit: {accuracy:.2f}')

# Ergebnisse ausgeben
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Einige Vorhersagen visualisieren

_, axes = plt.subplots(2, 5)
images_and_predictions = list(zip(X_test, y_pred))
for ax, (image, prediction) in zip(axes.flatten(), images_and_predictions):
    ax.set_axis_off()
    image = image.reshape(8, 8)
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    ax.set_title(f'Pred: {prediction}')
plt.show()
