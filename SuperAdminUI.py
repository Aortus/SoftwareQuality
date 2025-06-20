import os
import LoginUI
import sqlite3
import time
import ServiceEngineerLogic
import datetime
import ManageAdmin

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
        elif keuze == "2":
            username = input("Voer de username van de System Administrator in die je wilt bijwerken: ")
            ManageAdmin.update_acc(username)
        elif keuze == "3":
            ManageAdmin.delete_entry_by_id()
        elif keuze == "4":
            break
        else:
            input("Ongeldige keuze. Druk op Enter.")