import bcrypt
import sqlite3
import datetime
import Login

def update_password(username):
    new_password = input("Nieuw wachtwoord: ")
    if Login.is_valid_password(new_password):
        Login.change_password(username, new_password)
        input("Wachtwoord succesvol gewijzigd. Druk op Enter om terug te keren.")
    else:
        input("Ongeldig wachtwoord. Zorg ervoor dat het minstens 12 tekens lang is, een hoofdletter, een kleine letter, een cijfer en een speciaal teken bevat. Druk op Enter om opnieuw te proberen.")


def search_scooter():
    serial = input("Voer het serienummer van de scooter in: ")

    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters WHERE serialnumber = ?", (serial,))
    scooter = cursor.fetchone()
    conn.close()

    if scooter:
        print("\nScootergegevens:")
        for i, col in enumerate(cursor.description):
            print(f"{col[0]}: {scooter[i]}")
    else:
        print("Scooter niet gevonden.")
    input("Druk op Enter om terug te keren.")


def update_scooter_attributes():
    serial = input("Voer het serienummer van de scooter in: ")

    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters WHERE serialnumber = ?", (serial,))
    if not cursor.fetchone():
        input("Scooter niet gevonden. Druk op Enter om terug te keren.")
        conn.close()
        return

    try:
        soc = int(input("Nieuwe State of Charge (0-100): "))
        if not 0 <= soc <= 100:
            raise ValueError("SoC moet tussen 0 en 100 zijn.")

        target_soc = int(input("Nieuwe Target SoC (0-100): "))
        if not 0 <= target_soc <= 100:
            raise ValueError("Target SoC moet tussen 0 en 100 zijn.")

        lat = float(input("Latitude (51.8 - 52.0): "))
        lon = float(input("Longitude (4.3 - 4.6): "))
        if not (51.8 <= lat <= 52.0 and 4.3 <= lon <= 4.6):
            raise ValueError("Locatie moet binnen Rotterdam vallen (lat: 51.8–52.0, lon: 4.3–4.6).")

        out_of_service = input("Out-of-Service? (ja/nee): ").strip().lower()
        if out_of_service not in ["ja", "nee"]:
            raise ValueError("Alleen 'ja' of 'nee' toegestaan voor out-of-service.")
        out_of_service = (out_of_service == "ja")

        mileage = int(input("Nieuwe kilometerstand: "))
        if mileage < 0:
            raise ValueError("Kilometerstand mag niet negatief zijn.")

        date_str = input("Laatste onderhoudsdatum (YYYY-MM-DD): ")
        try:
            maintenance_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Ongeldig datumformaat. Gebruik YYYY-MM-DD.")

        cursor.execute("""
            UPDATE scooters SET 
                stateofcharge = ?,
                targetstateofcharge = ?,
                outofservice = ?,
                mileage = ?,
                lastmaintenance = ?,
            WHERE serialnumber = ?
        """, (soc, target_soc, out_of_service, mileage, maintenance_date, serial))

        conn.commit()
        input("Scootergegevens succesvol bijgewerkt. Druk op Enter om terug te keren.")

    except Exception as e:
        input(f"Fout bij bijwerken: {e}\nDruk op Enter om terug te keren.")
    finally:
        conn.close()