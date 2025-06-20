import os
import LoginUI
import sqlite3
import time
import ServiceEngineerLogic
import datetime
import ManageAdmin
import Backup
import Logs
import ManageScooter
import ManageTraveller
import Login

def account_beheer(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Accountbeheer")
        print("1. Profielgegevens bijwerken")
        print("2. Wachtwoord wijzigen")
        print("2. Account verwijderen")
        print("3. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-4): ")
        if keuze == "1":
            ManageAdmin.update_acc(username)
        elif keuze == "2":
            ServiceEngineerLogic.update_password(username)
        elif keuze == "3":
            print("Weet u zeker dat u dit account wilt verwijderen? Dit kan niet ongedaan worden gemaakt.")
            confirm = input("Typ 'ja' om te bevestigen: ").strip().lower()
            if confirm == 'ja':
                user_id = ManageAdmin.get_id_by_username(username)
                print(ManageAdmin.delete_entry_by_id("admins", user_id))
                print("Account succesvol verwijderd.")
                input("Druk op Enter om terug te keren naar het inlogscherm.")
                LoginUI.login_screen()
            else:
                print("Accountverwijdering geannuleerd.")
                input("Druk op Enter om terug te keren.")
        elif keuze == "3":
            break
        else:
            input("Ongeldige keuze. Druk op Enter.")

def scooter_beheer():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Scooterbeheer")
        print("1. Scooter toevoegen")
        print("2. Scootergegevens bijwerken")
        print("3. Scooter verwijderen")
        print("4. Scooter zoeken")
        print("5. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-5): ")
        if keuze == "1":
            try:
                print("\nVoer de gegevens van de scooter in:\n")
                brand = input("Merk: ")
                model = input("Model: ")
                serialnumber = input("Serienummer: ")

                topspeed = int(input("Topsnelheid (km/h): "))
                if topspeed <= 0:
                    raise ValueError("Topsnelheid moet positief zijn.")

                batterycapacity = int(input("Batterijcapaciteit (Ah): "))
                if batterycapacity <= 0:
                    raise ValueError("Batterijcapaciteit moet positief zijn.")

                stateofcharge = int(input("Huidige Laadniveau (%): "))
                if not 0 <= stateofcharge <= 100:
                    raise ValueError("Laadniveau moet tussen 0 en 100 zijn.")

                targetstateofcharge = int(input("Doellading (%): "))
                if not 0 <= targetstateofcharge <= 100:
                    raise ValueError("Doel-Laadniveau moet tussen 0 en 100 zijn.")

                location = input("Voer locatie in (latitude,longitude — bijv: 51.91,4.44): ")
                lat, lon = map(float, location.split(','))
                if not (51.8 <= lat <= 52.0 and 4.3 <= lon <= 4.6):
                    raise ValueError("Locatie moet binnen Rotterdam vallen.")

                outofservice = input("Buiten gebruik? (ja/nee): ").strip().lower()
                if outofservice not in ["ja", "nee"]:
                    raise ValueError("Alleen 'ja' of 'nee' toegestaan.")
                outofservice = "1" if outofservice == "ja" else "0"

                mileage = int(input("Kilometerstand: "))
                if mileage < 0:
                    raise ValueError("Kilometerstand mag niet negatief zijn.")

                lastmaintenance = input("Laatste onderhoudsbeurt (YYYY-MM-DD): ")
                datetime.datetime.strptime(lastmaintenance, "%Y-%m-%d")

                msg = ManageScooter.add_scooter(
                    brand, model, serialnumber, str(topspeed), str(batterycapacity),
                    str(stateofcharge), str(targetstateofcharge), location,
                    outofservice, str(mileage), lastmaintenance
                )
                input(f"{msg}\nDruk op Enter om verder te gaan.")

            except Exception as e:
                input(f"Fout: {e}\nDruk op Enter om opnieuw te proberen.")
        elif keuze == "2":
            ManageScooter.update_scooter_attributes(role="System Administrator")
        elif keuze == "3":
            ManageScooter.delete_scooter()
        elif keuze == "4":
            ServiceEngineerLogic.search_scooter()
        elif keuze == "5":
            break
        else:
            input("Ongeldige keuze. Druk op Enter.")


def traveller_beheer(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Travellerbeheer")
        print("1. Traveller toevoegen")
        print("2. Traveller bijwerken")
        print("3. Traveller verwijderen")
        print("4. Traveller zoeken")
        print("5. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-5): ")
        if keuze == "1":
            print("\nVoer de gegevens van de traveller in:\n")
            firstname = input("Voornaam: ")
            lastname = input("Achternaam: ")
            birthdate = input("Geboortedatum (YYYY-MM-DD): ")
            gender = input("Geslacht (M/V): ").strip().upper()
            streetname = input("Straatnaam: ")
            streetnumber = input("Huisnummer: ")
            zipcode = input("Postcode: ")
            city = input("Woonplaats: ")
            email = input("E-mailadres: ")
            mobilephone = input("Mobiele telefoon: ")
            drivinglicense = input("Rijbewijs: ").strip().lower()

            result = ManageTraveller.register_traveller(firstname, lastname, birthdate, gender, streetname, streetnumber, zipcode, city, email, mobilephone, drivinglicense)
            if result.startswith("Traveller successfully registered"):
                Logs.log_activity(username, "Traveller registratie", f"{firstname} {lastname} geregistreerd", 0)
        elif keuze == "2":
            ManageTraveller.update_traveller()
        elif keuze == "3":
            email = input("Voer het e-mailadres van de traveller in die u wilt verwijderen: ")
            print("Weet u zeker dat u deze traveller wilt verwijderen?")
            confirm = input("Typ 'ja' om te bevestigen: ").strip().lower()
            if confirm == 'ja':
                print(f"Traveller met e-mailadres {email} wordt verwijderd.")
                ManageTraveller.delete_traveller(email)
                input("Traveller succesvol verwijderd. Druk op Enter om verder te gaan.")
                Logs.log_activity(username, "Traveller verwijdering", f"Traveller met e-mailadres {email} verwijderd", 0)
            else:
                print("Traveller verwijdering geannuleerd.")
                input("Druk op Enter om terug te keren.")
        elif keuze == "4":
            search_term = input("Voer een zoekterm in (deel van voornaam, achternaam, e-mailadres, etc.): ").strip()
            if not search_term:
                input("Zoekterm mag niet leeg zijn. Druk op Enter om terug te keren.")
                continue
            print(ManageTraveller.search_traveller(search_term))
        elif keuze == "5":
            break
        else:
            input("Ongeldige keuze. Druk op Enter.")


def service_engineer_beheer():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Service Engineer Beheer")
        print("1. Engineer toevoegen")
        print("2. Engineer profiel bijwerken")
        print("3. Engineer verwijderen")
        print("4. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-5): ")
        if keuze == "1":
            ManageAdmin.AddAdmin()
        elif keuze == "2":
            username = input("Voer de username van de Service Engineer in die je wilt bijwerken: ")
            ManageAdmin.update_acc(username)
        elif keuze == "3":
            username = input("Voer de username van de Service Engineer in die je wilt verwijderen: ").strip()
            admin = ManageAdmin.get_admin_by_username(username)
            if not admin:
                input("Gebruiker niet gevonden. Druk op Enter om terug te keren.")
            elif admin['admin_type'] != "Service Engineer":
                input("Deze gebruiker is geen Service Engineer. Verwijderen niet toegestaan. Druk op Enter om terug te keren.")
            else:
                confirm = input(f"Weet je zeker dat je Service Engineer '{username}' wilt verwijderen? (ja/nee): ").strip().lower()
                if confirm == "ja":
                    msg = ManageAdmin.delete_entry_by_id("admins", admin['id'])
                    input(msg + " Druk op Enter om terug te keren.")
                else:
                    input("Verwijderen geannuleerd. Druk op Enter om terug te keren.")
        elif keuze == "4":
            break
        else:
            input("Ongeldige keuze. Druk op Enter.")


def backup_logs_menu(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Backup & Logs")
        print("1. Maak een backup")
        print("2. Herstel een backup met code")
        print("3. Bekijk logbestanden")
        print("4. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-4): ")
        if keuze == "1":
            password = input("Voer een wachtwoord in voor de backup: ")
            if not password or Login.has_null_byte(password):
                input("Wachtwoord mag niet leeg zijn. Druk op Enter om terug te keren.")
                continue
            Backup.backup_database(password)
        elif keuze == "2":
            backup_file = input("Voer de naam van het backup bestand in (bijv. SQDB_backup_20231001_1200.db): ")
            if not os.path.exists(backup_file):
                input(f"Backup bestand '{backup_file}' bestaat niet. Druk op Enter om terug te keren.")
                continue
            wwofcode = input("Herstel via wachtwoord of code? (1. Wachtwoord / 2. Code): ").strip()
            if wwofcode in ("1", "wachtwoord"):
                restore_password = input("Voer het wachtwoord in voor de backup: ")
                if not restore_password or Login.has_null_byte(restore_password):
                    input("Wachtwoord mag niet leeg zijn. Druk op Enter om terug te keren.")
                    continue
                Backup.restore_database_from_password(backup_file, restore_password)
            elif wwofcode in ("2", "code"):
                restore_code = input("Voer de herstelcode in: ")
                if not restore_code or Login.has_null_byte(restore_code):
                    input("Herstelcode mag niet leeg zijn. Druk op Enter om terug te keren.")
                    continue
                Backup.restore_backup_through_code(backup_file, restore_code, username)
        elif keuze == "3":
            print("\nAlle logs:")
            decrypted = Logs.get_all_logs()
            for log in decrypted:
                print(f"Log ID      : {log[0]}")
                print(f"Timestamp   : {log[1]}")
                print(f"User ID     : {log[2]}")
                print(f"Action      : {log[3]}")
                print(f"Details     : {log[4]}")
                print(f"Status      : {log[5]}")
                print(f"Read Status : {log[6]}\n")
            input("\nDruk op Enter om terug te keren.")
        elif keuze == "4":
            break
        else:
            input("Ongeldige keuze. Druk op Enter.")
