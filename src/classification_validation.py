import sklearn
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import RepeatedKFold

from recommenderSystem import get_recommendation

def RandomizedSearch(hyperparameters, X_train, y_train):
    knn = KNeighborsClassifier()
    cvFold = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    randomSearch = RandomizedSearchCV(estimator=knn, cv=cvFold, param_distributions=hyperparameters)
    best_model = randomSearch.fit(X_train, y_train)
    return best_model

def ModelEvaluation(y_test, y_pred, pred_prob):
    print("Classification Report: \n", classification_report(y_test, y_pred))
    roc_score = roc_auc_score(y_test, pred_prob, multi_class='ovr')
    print("ROC Score: ", roc_score)
    return roc_score

def HyperparametersSearch(X_train, X_test, y_train, y_test):
    result = {}
    n_neighbors = list(range(1, 30))
    weights = ['uniform', 'distance']
    metric = ['euclidean', 'manhattan', 'hamming']
    hyperparameters = dict(metric=metric, weights=weights, n_neighbors=n_neighbors)

    i = 0
    while i < 15:
        best_model = RandomizedSearch(hyperparameters, X_train, y_train)
        bestweights = best_model.best_estimator_.get_params()['weights']
        bestMetric = best_model.best_estimator_.get_params()['metric']
        bestNeighbours = best_model.best_estimator_.get_params()['n_neighbors']

        knn = KNeighborsClassifier(n_neighbors=bestNeighbours, weights=bestweights, algorithm='auto', metric=bestMetric)
        knn.fit(X_train, y_train)

        pred_prob = knn.predict_proba(X_test)
        roc_score = roc_auc_score(y_test, pred_prob, multi_class='ovr')

        result[i] = {'n_neighbors': bestNeighbours, 'metric': bestMetric, 'weights': bestweights, 'roc_score': roc_score}
        i += 1

    result = dict(sorted(result.items(), key=lambda x: x[1]['roc_score'], reverse=True))
    first_e1 = list(result.keys())[0]
    result = list(result[first_e1].values())
    return result

def SearchingBestModelStats(X_train, X_test, y_train, y_test):
    print("\n\nComposizione iniziale del modello con iper-parametri di base...")
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', p=2, metric='minkowski')
    knn.fit(X_train, y_train)

    print("\nPredizioni dei primi 5 elementi: ", knn.predict(X_test)[0:5], 'Valori effettivi: ', y_test[0:5])
    y_pred = knn.predict(X_test)
    pred_prob = knn.predict_proba(X_test)

    print("\nValutazione del modello...\n")
    ModelEvaluation(y_test, y_pred, pred_prob)

    print("\nProviamo a migliorare il nostro modello determinando gli iper-parametri ottimali con 'Grid Search':\n")
    result = HyperparametersSearch(X_train, X_test, y_train, y_test)

    print("\nGRID SEARCH:\n")
    bestweights = result[2]
    print("Best Weights: ", bestweights)
    bestmetric = result[1]
    print("Best Metric: ", bestmetric)
    bestNeighbours = result[0]
    print("Best n_eighbours: ", bestNeighbours)

    print("\nRicomponiamo il modello utilizzando i nuovi iper-parametri: ")
    knn = KNeighborsClassifier(n_neighbors=bestNeighbours, weights=bestweights, algorithm='auto', metric=bestmetric)
    knn.fit(X_train, y_train)

    print("\nPredizione dei primi 5 elementi: ", knn.predict(X_test)[0:5], "Valori effettivi: ", y_test[0:5])
    y_pred = knn.predict(X_test)
    pred_prob = knn.predict_proba(X_test)

    ModelEvaluation(y_test, y_pred, pred_prob)
    print("\nOra possiamo procede alla fase di recommandation...")

    return knn

def main_recommender():
    # Carichiamo il dataset Steam pre-processato
    game_data = pd.read_csv('../dataset/pre-processato/steam_renamed_dataset.csv')

    # Creiamo la colonna "star" come media di valutazioni (ipotetiche) o basata su metriche reali
    game_data['star'] = ((game_data['positive_ratings'] /
                          (game_data['positive_ratings'] + game_data['negative_ratings'] + 1)) * 5)

    # Classifichiamo i giochi in fasce di qualità
    game_data.loc[(game_data['star'] >= 4.0), 'star'] = 5
    game_data.loc[(game_data['star'] < 4.0) & (game_data['star'] >= 3), 'star'] = 4
    game_data.loc[(game_data['star'] < 3) & (game_data['star'] >= 2), 'star'] = 3
    game_data.loc[(game_data['star'] < 2) & (game_data['star'] >= 1), 'star'] = 2
    game_data.loc[(game_data['star'] < 1), 'star'] = 1

    # Features per il KNN
    knn_data = game_data[['game_price', 'avg_playtime', 'positive_ratings', 'negative_ratings', 'star']].copy()

    x = knn_data.drop(columns=['star'])
    y = knn_data['star'].values

    # Otteniamo i dati raccomandati
    recommend_data = get_recommendation()

    # Creiamo la matrice per predizione
    predict_data = game_data[['game_price', 'avg_playtime', 'positive_ratings', 'negative_ratings']].iloc[recommend_data.index]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1, stratify=y)

    # Standardizzazione
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    predict_data = scaler.transform(predict_data)

    knn = SearchingBestModelStats(X_train, X_test, y_train, y_test)
    knn.fit(X_train, y_train)

    # Predizione
    star_prediction = knn.predict(predict_data)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    recommend_data['star_prediction'] = star_prediction

    print("\nEcco una lista di giochi simili con predizione sulla qualità (star):\n")
    print(recommend_data, "\n")
