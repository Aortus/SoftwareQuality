import bcrypt
import sqlite3
import datetime
import Login
import ManageScooter
import Encryption

def update_password(username):
    new_password = input("Nieuw wachtwoord: ")
    if Login.is_valid_password(new_password):
        Login.change_password(username, new_password)
        input("Wachtwoord succesvol gewijzigd. Druk op Enter om terug te keren.")
    else:
        input("Ongeldig wachtwoord. Zorg ervoor dat het minstens 12 tekens lang is, een hoofdletter, een kleine letter, een cijfer en een speciaal teken bevat. Druk op Enter om opnieuw te proberen.")


def search_scooter():
    serial = input("Voer het serienummer van de scooter in: ")

    scooters = ManageScooter.get_all_scooters()

    found_scooter = None
    for scooter in scooters:
        if scooter[3] == serial:
            found_scooter = scooter
            break

    if not found_scooter:
        input("Scooter niet gevonden. Druk op Enter om terug te keren.")
        return

    ManageScooter.print_scooter_info(found_scooter)
    input("Druk op Enter om terug te keren.")


def update_scooter_attributes():
    serial = input("Voer het serienummer van de scooter in: ")

    scooters = ManageScooter.get_all_scooters()

    found_scooter = None
    for scooter in scooters:
        if scooter[3] == serial:
            found_scooter = list(scooter)
            break

    if not found_scooter:
        input("Scooter niet gevonden. Druk op Enter om terug te keren.")
        return

    while True:
        ManageScooter.print_scooter_info(found_scooter)
        idx = input("Kies een veld om aan te passen (7-12), of typ 'exit' om terug te keren: ").strip()

        if idx.lower() == "exit":
            break

        try:
            idx = int(idx)
            if idx == 7:
                soc = int(input("Nieuwe State of Charge (0-100): "))
                if not 0 <= soc <= 100:
                    raise ValueError("SoC moet tussen 0 en 100 zijn.")
                found_scooter[6] = str(soc)

            elif idx == 8:
                target_soc = int(input("Nieuwe Target SoC (0-100): "))
                if not 0 <= target_soc <= 100:
                    raise ValueError("Target SoC moet tussen 0 en 100 zijn.")
                found_scooter[7] = str(target_soc)

            elif idx == 9:
                location = input("Nieuwe locatie (bijv: 51.91,4.44): ")
                lat, lon = map(float, location.split(','))
                if not (51.8 <= lat <= 52.0 and 4.3 <= lon <= 4.6):
                    raise ValueError("Locatie moet binnen Rotterdam vallen.")
                found_scooter[8] = location

            elif idx == 10:
                out = input("Out-of-Service? (ja/nee): ").strip().lower()
                if out not in ["ja", "nee"]:
                    raise ValueError("Alleen 'ja' of 'nee' toegestaan.")
                found_scooter[9] = "1" if out == "ja" else "0"

            elif idx == 11:
                mileage = int(input("Nieuwe kilometerstand: "))
                if mileage < 0:
                    raise ValueError("Kilometerstand mag niet negatief zijn.")
                found_scooter[10] = str(mileage)

            elif idx == 12:
                date_str = input("Laatste onderhoudsdatum (YYYY-MM-DD): ")
                maintenance_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                found_scooter[11] = maintenance_date.strftime("%Y-%m-%d")

            else:
                input("Ongeldige keuze, kies tussen 7-12. Druk op Enter om opnieuw te proberen.")
                continue

            encrypted = [Encryption.encrypt_data(str(v)).decode() if i != 0 else v for i, v in enumerate(found_scooter)]

            conn = sqlite3.connect("SQDB.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE scooters SET 
                    stateofcharge = ?, targetstateofcharge = ?, location = ?, 
                    outofservice = ?, mileage = ?, lastmaintenance = ?
                WHERE id = ?
            """, (
                encrypted[6], encrypted[7], encrypted[8], 
                encrypted[9], encrypted[10], encrypted[11],
                encrypted[0]
            ))
            conn.commit()
            conn.close()
            print("Gegevens succesvol bijgewerkt.")
            input("Druk op Enter om terug te gaan.\n")

        except Exception as e:
            input(f"Fout: {e}\nDruk op Enter om opnieuw te proberen.")

