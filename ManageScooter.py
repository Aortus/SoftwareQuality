import sqlite3
import Encryption
import datetime

def get_all_scooters():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters")
    scooters = cursor.fetchall()
    conn.close()

    decrypted_scooters = []
    for scooter in scooters:
        scooter_list = list(scooter)
        for i in range(0, len(scooter_list)):
            if i == 0:
                continue
            scooter_list[i] = Encryption.decrypt_data(scooter_list[i])
        decrypted_scooters.append(tuple(scooter_list))

    return decrypted_scooters

def print_all_scooters():
    scooters = get_all_scooters()
    for scooter in scooters:
        print_scooter_info(scooter)

def print_scooter_info(scooter):
    print(
        f"\nScooter Informatie:\n"
        f"1. ID: {scooter[0]}\n"
        f"2. Merk: {scooter[1]}\n"
        f"3. Model: {scooter[2]}\n"
        f"4. Serienummer: {scooter[3]}\n"
        f"5. Topsnelheid: {scooter[4]} km/h\n"
        f"6. Batterijcapaciteit: {scooter[5]} Ah\n"
        f"7. Laadniveau: {scooter[6]}\n"
        f"8. Doel-Laadniveau: {scooter[7]}\n"
        f"9. Locatie: {scooter[8]}\n"
        f"10. Buiten Gberuik: {'Ja' if scooter[9] == '1' else 'Nee'}\n"
        f"11. Kilometerstand: {scooter[10]} km\n"
        f"12. Laatste Onderhoudsbeurt: {scooter[11]}\n"
    )

def add_scooter(brand, model, serialnumber, topspeed, batterycapacity, stateofcharge, targetstateofcharge, location, outofservice, mileage, lastmaintenance):
    encrypted_brand = Encryption.encrypt_data(brand)
    encrypted_model = Encryption.encrypt_data(model)
    encrypted_serialnumber = Encryption.encrypt_data(serialnumber)
    encrypted_topspeed = Encryption.encrypt_data(topspeed)
    encrypted_batterycapacity = Encryption.encrypt_data(batterycapacity)
    encrypted_stateofcharge = Encryption.encrypt_data(stateofcharge)
    encrypted_targetstateofcharge = Encryption.encrypt_data(targetstateofcharge)
    encrypted_location = Encryption.encrypt_data(location)
    encrypted_outofservice = Encryption.encrypt_data(outofservice)
    encrypted_mileage = Encryption.encrypt_data(mileage)
    encrypted_lastmaintenance = Encryption.encrypt_data(lastmaintenance)

    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO scooters (brand, model, serialnumber, topspeed, batterycapacity, stateofcharge, targetstateofcharge, location, outofservice, mileage, lastmaintenance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (encrypted_brand, encrypted_model, encrypted_serialnumber, encrypted_topspeed, encrypted_batterycapacity, encrypted_stateofcharge, encrypted_targetstateofcharge, encrypted_location, encrypted_outofservice, encrypted_mileage, encrypted_lastmaintenance)
        )
        conn.commit()
        return "Scooter succesvol toegevoegd."
    except sqlite3.Error as e:
        return f"Fout bij het toevoegen van de scooter: {e}"
    finally:
        conn.close()

def update_scooter_attributes(role):
    serial = input("Voer het serienummer van de scooter in: ")

    scooters = get_all_scooters()
    found_scooter = None
    for scooter in scooters:
        if scooter[3] == serial:
            found_scooter = list(scooter)
            break

    if not found_scooter:
        input("Scooter niet gevonden. Druk op Enter om terug te keren.")
        return

    if role.lower() in ["super administrator", "system administrator"]:
        editable_fields = list(range(2, 13)) 
    else:
        editable_fields = list(range(7, 13)) 

    while True:
        print_scooter_info(found_scooter)
        print(f"Bewerkbare velden voor jouw rol ({role}): {', '.join(map(str, editable_fields))}")
        idx = input("Kies een veld om aan te passen of typ 'exit' om terug te keren: ").strip()

        if idx.lower() == "exit":
            break

        try:
            idx = int(idx)
            if idx not in editable_fields:
                raise ValueError(f"Toegang geweigerd. Je mag alleen de velden {editable_fields} bewerken.")

            if idx == 2:
                merk = input("Nieuw merk: ")
                if has_null_byte(merk):
                    raise ValueError("Merk mag geen null bytes bevatten.")
                found_scooter[1] = merk.strip()
            elif idx == 3:
                model = input("Nieuw model: ")
                if has_null_byte(model):
                    raise ValueError("Model mag geen null bytes bevatten.")
                found_scooter[2] = model.strip()
            elif idx == 4:
                serienummer = input("Nieuw serienummer: ")
                if has_null_byte(serienummer):
                    raise ValueError("Serienummer mag geen null bytes bevatten.")
                found_scooter[3] = serienummer.strip()
            elif idx == 5:
                topspeed = int(input("Nieuwe topsnelheid (km/h): "))
                if topspeed <= 0:
                    raise ValueError("Topsnelheid moet positief zijn.")
                found_scooter[4] = str(topspeed)
            elif idx == 6:
                battery = int(input("Nieuwe batterijcapaciteit (km): "))
                if battery <= 0:
                    raise ValueError("Capaciteit moet positief zijn.")
                found_scooter[5] = str(battery)
            elif idx == 7:
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
                if has_null_byte(location):
                    raise ValueError("Locatie mag geen null bytes bevatten.")
                lat, lon = map(float, location.split(','))
                if not (51.8 <= lat <= 52.0 and 4.3 <= lon <= 4.6):
                    raise ValueError("Locatie moet binnen Rotterdam vallen.")
                found_scooter[8] = location
            elif idx == 10:
                out = input("Out-of-Service? (ja/nee): ").strip().lower()
                if has_null_byte(out):
                    raise ValueError("Input mag geen null bytes bevatten.")
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
                if has_null_byte(date_str):
                    raise ValueError("Datum mag geen null bytes bevatten.")
                maintenance_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                found_scooter[11] = maintenance_date.strftime("%Y-%m-%d")
            
            encrypted = [Encryption.encrypt_data(str(v)).decode() if i != 0 else v for i, v in enumerate(found_scooter)]

            conn = sqlite3.connect("SQDB.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE scooters SET 
                    brand = ?, model = ?, serialnumber = ?, topspeed = ?, batterycapacity = ?,
                    stateofcharge = ?, targetstateofcharge = ?, location = ?, 
                    outofservice = ?, mileage = ?, lastmaintenance = ?
                WHERE id = ?
            """, (
                encrypted[1], encrypted[2], encrypted[3], encrypted[4], encrypted[5],
                encrypted[6], encrypted[7], encrypted[8],
                encrypted[9], encrypted[10], encrypted[11],
                encrypted[0]
            ))
            conn.commit()
            conn.close()

            input("Gegevens succesvol bijgewerkt. Druk op Enter om verder te gaan.")

        except Exception as e:
            input(f"Fout: {e}\nDruk op Enter om opnieuw te proberen.")

def delete_scooter():
    serial = input("Voer het serienummer van de scooter in die u wilt verwijderen: ")

    scooters = get_all_scooters()
    found_scooter = None
    for scooter in scooters:
        if scooter[3] == serial:
            found_scooter = scooter
            break

    if not found_scooter:
        input("Scooter niet gevonden. Druk op Enter om terug te keren.")
        return

    print_scooter_info(found_scooter)
    found_scooter_id = found_scooter[0]
    confirm = input("Weet u zeker dat u deze scooter wilt verwijderen? (ja/nee): ").strip().lower()

    if confirm == "ja":
        conn = sqlite3.connect("SQDB.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scooters WHERE id = ?", (found_scooter_id,))
        conn.commit()
        conn.close()
        input("Scooter succesvol verwijderd. Druk op Enter om verder te gaan.")
    else:
        input("Verwijderen geannuleerd. Druk op Enter om terug te keren.")

def has_null_byte(s):
    return '\x00' in s

def search_scooter():
    query = input("Zoekterm (deel van serienummer, merk, model, etc.): ").strip().lower()

    scooters = get_all_scooters()
    matches = []

    for scooter in scooters:
        fields_to_search = [str(s).lower() for s in scooter]
        if any(query in field for field in fields_to_search):
            matches.append(scooter)

    if not matches:
        input("Geen scooters gevonden met die zoekterm. Druk op Enter om terug te keren.")
        return

    for idx, scooter in enumerate(matches, 1):
        print(f"\nResultaat {idx}:")
        print_scooter_info(scooter)

    input("\nDruk op Enter om terug te keren.")