from owlready2 import *

def main_ontology():
    print("\nBENVENUTO NELL'ONTOLOGIA DEI VIDEOGIOCHI")

    ontology_path = 'Ontologia.owx'
    ontology = get_ontology(ontology_path).load()

    def stampa_individui(nome_classe):
        classe = ontology.search_one(iri=f"*{nome_classe}")
        if classe:
            individui = list(classe.instances())
            if individui:
                print(f"\nIndividui della classe '{classe}':")
                for i in individui:
                    print(f"- {i}")
            else:
                print(f"Nessun individuo per la classe '{classe}'")
        else:
            print(f"Classe '{nome_classe}' non trovata.")

    while True:
        print("\nSeleziona un'operazione:\n1) Visualizzazione Classi\n2) Visualizzazione proprietà d'oggetto"
              "\n3) Visualizzazione proprietà dei dati\n4) Esegui query\n5) Esci dall'Ontologia\n")
        menu_answer = input("Inserisci un valore: ")

        if menu_answer == '1':
            print("\nCLASSI PRESENTI NELL'ONTOLOGIA: ")
            for cls in ontology.classes():
                print(f"- {cls}")  # Nome completo con prefisso

            while True:
                print("\nVorresti esplorare meglio una delle seguenti classi?\n"
                      "1) Videogioco\n2) Genere\n3) Prezzo\n4) Data di Rilascio\n5) Valutazione\n6) No\n")
                class_answer = input("Inserisci un valore: ")

                if class_answer == '1':
                    stampa_individui("Videogioco")
                elif class_answer == '2':
                    stampa_individui("Genere")
                elif class_answer == '3':
                    stampa_individui("Prezzo")
                elif class_answer == '4':
                    stampa_individui("DataRilascio")
                elif class_answer == '5':
                    stampa_individui("Valutazione")
                elif class_answer == '6':
                    break
                else:
                    print("Scelta non valida.")

        elif menu_answer == '2':
            print("\nPROPRIETÁ D'OGGETTO PRESENTI NELL'ONTOLOGIA:")
            for prop in ontology.object_properties():
                print(f"- {prop}")  # Nome completo

        elif menu_answer == '3':
            print("\nPROPRIETÁ DEI DATI PRESENTI NELL'ONTOLOGIA:")
            for prop in ontology.data_properties():
                print(f"- {prop}")  # Nome completo

        elif menu_answer == '4':
            while True:
                print("\n1) Videogiochi di genere 'Simulation'\n2) Videogiochi rilasciati nel 2013"
                      "\n3) Videogiochi con più di 50 valutazioni positive\n4) Indietro\n")
                choice = input("Scelta: ")

                videogioco_cls = ontology.search_one(iri="*Videogioco")

                if choice == '1':
                    print("\nVIDEOGIOCHI DI GENERE SIMULATION")
                    genere = ontology.search_one(iri="*Simulation")
                    if genere:
                        for vg in videogioco_cls.instances():
                            if hasattr(vg, "haGenere") and genere in vg.haGenere:
                                print(f"- {vg.name}")
                elif choice == '2':
                    print("\nVIDEOGIOCHI RILASCIATI NEL 2013")
                    anno = ontology.search_one(iri="*2013")
                    if anno:
                        for vg in videogioco_cls.instances():
                            if hasattr(vg, "haDataRilascio") and anno in vg.haDataRilascio:
                                print(f"- {vg.name}")
                elif choice == '3':
                    print("\nVIDEOGIOCHI CON PIU' DI 50 VALUTAZIONI POSITIVE")
                    for vg in videogioco_cls.instances():
                        if hasattr(vg, "valutazioniPositive"):
                            try:
                                if vg.valutazioniPositive[0] > 50:
                                    print(f"- {vg.name}")
                            except:
                                pass
                elif choice == '4':
                    break
                else:
                    print("Valore non valido.")

        elif menu_answer == '5':
            print("Uscita dall'ontologia.")
            break

if __name__ == "__main__":
    main_ontology()
