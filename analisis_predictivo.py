# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix');
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

#Cargamos el dataset
URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
data = pd.read_csv(URL1)

URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
X = pd.read_csv(URL2)
#TAREA 1: Creamos una matriz NumPy con la variable "class"
Y = data["Class"].to_numpy()
Y = pd.Series(Y)

#TAREA 2: Estandarizamos los datos en X y los asignamos a la variable X
transform = preprocessing.StandardScaler().fit(X).transform(X)
transform[0:5]

#TAREA 3: Usamos la funcion train_test_split para dividir los datos en entrenamiento y prueba
X_train, X_test, Y_train, Y_test = train_test_split( X, Y, test_size=0.2, random_state=2)
print ('Train set:', X_train.shape,  Y_train.shape)
print ('Test set:', X_test.shape,  Y_test.shape)

#Vemos que solo hay 18 muestras de prueba
print(Y_test.shape)

#TAREA 4: Creamos un objeto de regresion logistica y un objeto GridSearchCV
parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']}

parameters ={"C":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}# l1 lasso l2 ridge
lr=LogisticRegression(max_iter=400)
logreg_cv = GridSearchCV(estimator=lr, param_grid=parameters, scoring='accuracy', cv=5, n_jobs=-1, verbose=2)
logreg_cv.fit(X_train, Y_train)

print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)

#TAREA 5: Calculamos la precision de los datos de prueba
accuracy = logreg_cv.score(X_test, Y_test)  # Calcula la precisión en el conjunto de prueba
print(f"Precisión (usando score()): {accuracy}")

#Vemos la matriz de confusion
yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#TAREA 6: Creamos un objeto de maquina de vectores de soporte (SVM) y un objeto GridSearchCV
parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()

svm_cv = GridSearchCV(estimator=svm, param_grid=parameters, scoring='accuracy', cv=5, n_jobs=-1, verbose=2)
svm_cv.fit(X_train, Y_train)

print("tuned hpyerparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)

#TAREA 7: Calculamos la precision de los datos de prueba
accuracy = svm_cv.score(X_test, Y_test)  # Calcula la precisión en el conjunto de prueba
print(f"Precisión (usando score()): {accuracy}")

#Vemos la matriz de confusion
yhat=svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#TAREA 8: Creamos un objeto clasificador de arbol de decision y un objeto GridSearchCV
parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()

tree_cv = GridSearchCV(estimator=tree, param_grid=parameters, scoring='accuracy', cv=5, n_jobs=-1, verbose=2)
tree_cv.fit(X_train, Y_train)

print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)

#TAREA 9: Calculamos la precision de tree_cv en los datos de prueba
accuracy = tree_cv.score(X_test, Y_test)  # Calcula la precisión en el conjunto de prueba
print(f"Precisión (usando score()): {accuracy}")

#Vemos la matriz de confusion
yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#TAREA 10: Creamos un objeto k vecinos y un objeto GridSearchCV
parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}
KNN = KNeighborsClassifier()

knn_cv = GridSearchCV(estimator=KNN, param_grid=parameters, scoring='accuracy', cv=5, n_jobs=-1, verbose=2)
knn_cv.fit(X_train, Y_train)

print("tuned hpyerparameters :(best parameters) ",knn_cv.best_params_)
print("accuracy :",knn_cv.best_score_)

#TAREA 11: Calculamos la precision de knn_cv en los datos de prueba
accuracy = knn_cv.score(X_test, Y_test)  # Calcula la precisión en el conjunto de prueba
print(f"Precisión (usando score()): {accuracy}")

#Vemos la matriz de confusion
yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#TAREA 12: Encontramos el metodo que mejor funciona
#Vemos que tanto el modelo de Regresion Lineal, como el de Maquina de Vectores de Soporte y el k-vecinos
#arroja la misma presicion del 83.33%, superior al modelo de Arboles de Desicion, lo que sugiere que
#un limite de desicion lineal o basado en la proximidad es igual de efectivo para la clasificacion de los
#lanzamientos exitosos