import os
import xlsxwriter


def create_table(lang: str):
    verzeichnis = os.path.join(".log", "real_data", "encrypted", lang, "conversation")
    dateinamen = sorted([
        f for f in os.listdir(verzeichnis)
        if os.path.isfile(os.path.join(verzeichnis, f)) and f.endswith(".log")
    ])

    ausgabepfad = os.path.join(".log", f"auswertung_llm_{lang}.xlsx")
    arbeitsmappe = xlsxwriter.Workbook(ausgabepfad)
    tabelle = arbeitsmappe.add_worksheet("Bewertungen")

    fett = arbeitsmappe.add_format({'bold': True, 'border': 1, 'align': 'center'})
    farben = ['#E6FFE6', '#E6F2FF']  # Hellgrün und Hellblau
    rand_format = {'border': 1, 'align': 'center'}

    kopf = [
        "Datei", "Rolle", "Hallucinations", "Language Consistency",
        "Syntax Errors", "Role Consistency", "Information Consistency",
        "Score", "Max"
    ]

    spaltenbreiten = [35, 10, 15, 20, 15, 17, 22, 10, 7]
    for col, breite in enumerate(spaltenbreiten):
        tabelle.set_column(col, col, breite)

    for spalte, titel in enumerate(kopf):
        tabelle.write(0, spalte, titel, fett)

    zeile = 1
    for index, dateiname in enumerate(dateinamen):
        bg_color = farben[index % len(farben)]
        zeilen_format = arbeitsmappe.add_format({'bg_color': bg_color, **rand_format})

        for rolle in ["arzt", "patient"]:
            if rolle == "arzt":
                tabelle.write(zeile, 0, dateiname, zeilen_format)
            else:
                tabelle.write(zeile, 0, "", zeilen_format)

            tabelle.write(zeile, 1, rolle, zeilen_format)
            # Leere Zellen für die Kriterien
            for spalte in range(2, 7):
                tabelle.write(zeile, spalte, "", zeilen_format)

            # Formel für Score anstelle Summe
            formel = (
                f"=IF(SUM(C{zeile + 1}:G{zeile + 1})=0,3,"
                f"IF(SUM(C{zeile + 1}:G{zeile + 1})=1,2,"
                f"IF(SUM(C{zeile + 1}:G{zeile + 1})=2,1,0)))"
            )
            tabelle.write_formula(zeile, 7, formel, zeilen_format)

            tabelle.write(zeile, 8, "/10", zeilen_format)

            zeile += 1

    arbeitsmappe.close()
    print(f"[{lang}] {zeile - 1} Zeilen geschrieben. Datei: {ausgabepfad}")



def main():
    create_table("de")
    create_table("en")

if __name__ == "__main__":
    main()