import os
import LoginUI
import sqlite3
import time
import ServiceEngineerLogic
import datetime
import ManageAdmin
import Login
import Backup
import Logs

def system_admin_beheer():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("System Administrator Beheer")
        print("1. System Administrator toevoegen")
        print("2. System Administrator profiel bijwerken")
        print("3. System Administrator verwijderen")
        print("4. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-4): ")
        if keuze == "1":
            ManageAdmin.AddAdmin()
            input("System Administrator toegevoegd. Druk op Enter om terug te keren.")
        elif keuze == "2":
            username = input("Voer de username van de System Administrator in die je wilt bijwerken: ")
            ManageAdmin.update_acc(username)
        elif keuze == "3":
            username = input("Voer de username van de Service Engineer in die je wilt verwijderen: ").strip()
            admin = ManageAdmin.get_admin_by_username(username)
            if not admin:
                input("Gebruiker niet gevonden. Druk op Enter om terug te keren.")
            elif admin['admin_type'] != "Service Engineer" or admin['admin_type'] != "System Administrator":
                input("Deze gebruiker is een Super Admin. Verwijderen niet toegestaan. Druk op Enter om terug te keren.")
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

def backup_beheer(username):
    while True:
        admins = ManageAdmin.get_all_admins()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Backup Beheer ===")
        print("1. Backup maken")
        print("2. Backup terugzetten met wachtwoord")
        print("3. Herstelcode aanmaken")
        print("4. Herstelcode verwijderen")
        print("5. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-5): ")

        if keuze == "1":
            pw = input("Voer het wachtwoord in om een backup te maken: ")
            if not Login.is_valid_password(pw):
                input("Ongeldig wachtwoord. Druk op Enter om opnieuw te proberen.")
                continue
            backup_file = Backup.backup_database(pw)
            print(f"Backup gemaakt: {backup_file}")
            Logs.log_activity(username, "Backup gemaakt", f"Backup succesvol gemaakt: {backup_file}", 0)
            input("Druk op Enter om terug te keren.")

        elif keuze == "2":
            backup_name = input("Voer de naam van de backup die je wilt terugzetten: ")
            if not os.path.exists(backup_name):
                input(f"Back-up bestand '{backup_name}' bestaat niet. Druk op Enter om terug te keren.")
                continue
            pw = input("Voer het wachtwoord in om de backup terug te zetten: ")
            result = Backup.restore_database_from_password(backup_name, pw)
            if result == "Ongeldig wachtwoord":
                input("Ongeldig wachtwoord. Druk op Enter om terug te keren.")
            else:
                print(f"Backup {backup_name} succesvol teruggezet.")
                Logs.log_activity(username, "Backup teruggezet", f"Backup succesvol teruggezet: {backup_name}", 0)
                input("Druk op Enter om terug te keren.")

        elif keuze == "3":
            backup_name = input("Voer de naam van de backup in waarvoor je een herstelcode wilt maken: ")
            if not os.path.exists(backup_name):
                input(f"Back-up bestand '{backup_name}' bestaat niet. Druk op Enter om terug te keren.")
                continue
            restore_code = input("Voer de herstelcode in: ")
            backup_un = input("Voer de username waarvoor je de herstelcode wilt aanmaken: ")
            if backup_un not in [admin[1] for admin in admins]:
                input("Username niet gevonden. Druk op Enter om opnieuw te proberen.")
                continue
            Backup.create_restore_code(backup_name, restore_code, backup_un)
            input("Druk op Enter om terug te keren.")

        elif keuze == "4":
            backup_name = input("Voer de naam van de backup in waarvan je de herstelcode wilt verwijderen: ")
            if not os.path.exists(backup_name):
                input(f"Back-up bestand '{backup_name}' bestaat niet. Druk op Enter om terug te keren.")
                continue
            backup_un = input("Voer de username waarvoor je de herstelcode wilt verwijderen: ")
            if backup_un not in [admin[1] for admin in admins]:
                input("Username niet gevonden. Druk op Enter om opnieuw te proberen.")
                continue
            Backup.delete_restore_code(backup_name, backup_un)
            input("Druk op Enter om terug te keren.")

        elif keuze == "5":
            break

        else:
            input("Ongeldige keuze. Druk op Enter om opnieuw te proberen.")
