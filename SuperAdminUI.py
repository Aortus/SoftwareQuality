import os
import LoginUI
import sqlite3
import time
import ServiceEngineerLogic
import datetime
import ManageAdmin
import Login

def system_admin_beheer():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("System Administrator Beheer")
        print("1. System Administrator toevoegen")
        print("2. System Administrator profiel bijwerken")
        print("3. System Administrator verwijderen")
        print("4. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-5): ")
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