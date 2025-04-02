from pyswip import Prolog

def main():
    prolog = Prolog()
    prolog.consult('game_kb.pl')
    game_ids = []

    while True:
        try:
            choice = int(input("\nScegliere quale funzione eseguire:\n"
                               "1) Trova un gioco in base a determinate caratteristiche\n"
                               "2) Trova la fascia di prezzo migliore per i giochi selezionati\n"
                               "3) Esci\n"
                               "\nInserisci un valore: "))
            if choice == 1:
                game_ids = query_game(prolog)
            elif choice == 2:
                if game_ids:
                    find_most_common_price_range(prolog, game_ids)
                else:
                    print("Esegui prima una ricerca di giochi (opzione 1).")
            elif choice == 3:
                print("Uscita dal programma.")
                break
            else:
                print("Input non valido. Utilizzare solo 1, 2 o 3.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

def query_game(prolog):
    periodo = None
    genere = None
    tempo = None
    game_ids = []

    while periodo is None:
        try:
            print("\nInserisci il periodo di rilascio del gioco:")
            print("1) recente\n2) tra 2000 e 2010\n3) pre 2000")
            scelta = int(input())
            if scelta == 1:
                periodo = "recente"
            elif scelta == 2:
                periodo = "tra_2000_2010"
            elif scelta == 3:
                periodo = "pre_2000"
            else:
                print("Valore non valido.")
        except ValueError:
            print("Inserisci un numero valido.")

    while genere is None:
        generi = ["action", "indie", "rpg", "strategy", "simulation", "sports", "casual"]
        print("\nScegli un genere tra:", ", ".join(generi))
        genere_input = input("Genere: ").lower()
        if genere_input in generi:
            genere = genere_input
        else:
            print("Genere non valido.")

    while tempo is None:
        print("\nQuanto tempo medio di gioco?\n1) breve\n2) medio\n3) lungo")
        try:
            t = int(input())
            if t == 1:
                tempo = "breve"
            elif t == 2:
                tempo = "medio"
            elif t == 3:
                tempo = "lungo"
            else:
                print("Valore non valido.")
        except ValueError:
            print("Inserisci un numero valido.")

    query = f"gioco(ID, {periodo}, {genere}, {tempo})."

    try:
        results = list(prolog.query(query))
        if not results:
            print("Nessun gioco trovato con questi filtri.")
        else:
            print("\nGiochi trovati:")
            for res in results:
                print(res["ID"])
                game_ids.append(res["ID"])
    except Exception as e:
        print(f"Errore durante la query: {e}")

    return game_ids

def find_most_common_price_range(prolog, game_ids):
    fascia_count = {}

    for game_id in game_ids:
        query = f"prezzo('{game_id}', Fascia)."
        try:
            results = list(prolog.query(query))
            for res in results:
                fascia = res["Fascia"]
                if fascia in fascia_count:
                    fascia_count[fascia] += 1
                else:
                    fascia_count[fascia] = 1
        except Exception as e:
            print(f"Errore nella query per {game_id}: {e}")

    if fascia_count:
        best_fascia = max(fascia_count, key=fascia_count.get)
        print(f"\n La fascia di prezzo più comune tra i giochi trovati è: {best_fascia}")
    else:
        print("Nessuna informazione sui prezzi disponibile per i giochi trovati.")


if __name__ == "__main__":
    main()