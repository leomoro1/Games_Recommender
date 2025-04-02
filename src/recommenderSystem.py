import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import pearsonr

# Funzione per ottenere input dell'utente
def get_info():
    print("Inserisci i dati con la lettera maiuscola iniziale\n")

    title = input("Inserisci il titolo del gioco: \n")
    genre = input("Inserisci il genere (es. Action): \n")
    release_date = input("Inserisci l'anno di uscita (YYYY): \n")

    user_data = pd.DataFrame({
        'title': [title],
        'genre': [genre],
        'release_date': [release_date],
        'avg_playtime': [0],
        'game_price': [0.0],
        'positive_ratings': [0],
        'negative_ratings': [0]
    })
    return user_data

# Funzione per costruire la raccomandazione
def construct_recommendation(filename, user_data):
    df = pd.read_csv(filename)

    df = df[['title', 'release_date', 'genre', 'positive_ratings', 'negative_ratings', 'avg_playtime', 'game_price']].copy()
    df = df.dropna(subset=['title', 'genre'])

    # Aggiunta del gioco inserito dall'utente se non presente
    if user_data['title'][0] not in df['title'].values:
        df = pd.concat([user_data, df], ignore_index=True)
        user_index = 0
    else:
        user_index = df.index[df['title'] == user_data['title'][0]].tolist()[0]

    # Costruzione della colonna combinata per la vettorizzazione
    df['combined'] = (
        df['title'].astype(str) + ' ' +
        df['release_date'].astype(str) + ' ' +
        df['genre'].astype(str) + ' ' +
        df['avg_playtime'].astype(str) + ' ' +
        df['game_price'].astype(str) + ' ' +
        df['positive_ratings'].astype(str) + ' ' +
        df['negative_ratings'].astype(str)
    )

    tfidf_matrix = vectorize_data(df)
    tfidf_array = tfidf_matrix.toarray()

    print("\nInizio ricerca dei giochi simili...")

    # Calcolo correlazione tra gioco utente e tutti gli altri
    correlation = []
    for i in range(len(tfidf_array)):
        corr, _ = pearsonr(tfidf_array[user_index], tfidf_array[i])
        correlation.append((i, corr))

    sorted_corr = sorted(correlation, key=lambda x: x[1], reverse=True)[1:6]
    game_indexes = [i[0] for i in sorted_corr]

    print("\n[5 giochi più simili trovati]")
    return df.iloc[game_indexes][['title', 'genre', 'release_date']]

# Funzione di vettorizzazione
def vectorize_data(df):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['combined'])
    return tfidf

# Funzione principale
def get_recommendation():
    print("\nBENVENUTO NEL GAME RECOMMENDER SYSTEM\n")
    user_data = get_info()

    while True:
        print("\nDati inseriti:")
        print(user_data.head())

        answer = input("\nConfermi i dati? (y/n): ")
        if answer.lower() == 'n':
            user_data = get_info()
        else:
            break

    recommendations = construct_recommendation('../dataset/pre-processato/steam_renamed_dataset.csv', user_data)
    print("\nEcco i giochi consigliati:\n")
    print(recommendations)
    return recommendations