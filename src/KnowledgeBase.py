import pandas as pd

def clean_string(s):
    """Pulisce e normalizza una stringa per l'uso in Prolog."""
    return str(s).replace("'", "").encode('ascii', 'ignore').decode()

class KnowledgeBase:
    def createKnowledgeBase(self):
        df = pd.read_csv('steam_renamed_dataset.csv')

        # Pulizia delle stringhe
        columns_to_string = ['name', 'genre']
        df[columns_to_string] = df[columns_to_string].apply(lambda x: x.apply(clean_string))

        with open('game_kb.pl', 'w', encoding='utf-8') as f:
            f.write(":- discontiguous name/2.\n")
            f.write(":- discontiguous genre/2.\n")
            f.write(":- discontiguous release_year/2.\n")
            f.write(":- discontiguous average_playtime/2.\n")
            f.write(":- discontiguous game_price/2.\n\n")

            for _, row in df.iterrows():
                f.write(f"name({row['id']}, '{row['name']}').\n")
                f.write(f"genre({row['id']}, '{row['genre']}').\n")
                f.write(f"release_year({row['id']}, {int(row['release_year'])}).\n")
                f.write(f"average_playtime({row['id']}, {int(row['average_playtime'])}).\n")
                f.write(f"game_price({row['id']}, {float(row['game_price'])}).\n")

            # Regole anno
            f.write("\n% Classificazione per anno\n")
            f.write("recente(ID) :- release_year(ID, Y), Y > 2010.\n")
            f.write("tra_2000_2010(ID) :- release_year(ID, Y), Y >= 2000, Y =< 2010.\n")
            f.write("pre_2000(ID) :- release_year(ID, Y), Y < 2000.\n")

            # Regole durata gioco
            f.write("\n% Classificazione per durata media\n")
            f.write("breve(ID) :- average_playtime(ID, T), T =< 60.\n")
            f.write("medio(ID) :- average_playtime(ID, T), T > 60, T =< 300.\n")
            f.write("lungo(ID) :- average_playtime(ID, T), T > 300.\n")

            # Regole genere
            f.write("\n% Genere principale\n")
            f.write("game_genre(ID, G) :- genre(ID, G).\n")

            # Regole combinate anno + genere + durata
            genres = ["action", "indie", "rpg", "strategy", "simulation", "sports", "casual"]
            for genre in genres:
                for periodo in ["recente", "tra_2000_2010", "pre_2000"]:
                    for durata in ["breve", "medio", "lungo"]:
                        rule_name = f"{periodo}_{genre}_{durata}"
                        f.write(f"{rule_name}(ID) :- {periodo}(ID), game_genre(ID, '{genre}'), {durata}(ID).\n")

# Crea la KB
if __name__ == '__main__':
    kb = KnowledgeBase()
    kb.createKnowledgeBase()
