import os
import LoginUI
import sqlite3
import time
import ServiceEngineerLogic
import Encryption
import ManageAdmin
import ManageScooter
import SystemAdminUI

def get_admin_type(username):
    admins = ManageAdmin.get_all_admins()
    print(admins)
    for admin in admins:
        if admin[1] == username:
            return admin[6]

def service_engineer_menu(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Service Engineer Menu (Ingelogd als: {username})")
        print("1. Wachtwoord wijzigen")
        print("2. Scooterinformatie bewerken")
        print("3. Scooter opzoeken")
        print("4. Uitloggen")

        keuze = input("\nMaak een keuze (1-4): ")
        if keuze == "1":
            ServiceEngineerLogic.update_password(username)
        elif keuze == "2":
            ManageScooter.update_scooter_attributes(role="Service Engineer")
        elif keuze == "3":
            ServiceEngineerLogic.search_scooter()
        elif keuze == "4":
            print("Uitloggen...")
            time.sleep(10)
            LoginUI.login_screen()
            return
        else:
            input("Ongeldige keuze. Druk op Enter om opnieuw te proberen.")

def system_admin_menu(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"System Administrator Menu (Ingelogd als: {username})")
        print("1. Account beheer")
        print("2. Scooter beheer")
        print("3. Travellers beheer")
        print("4. Service Engineer beheer")
        print("5. Backup/Logs")
        print("6. Lijst van alle gebruikers")
        print("7. Uitloggen")

        keuze = input("\nMaak een keuze (1-7): ")
        if keuze == "1":
            SystemAdminUI.account_beheer(username)
        elif keuze == "2":
            SystemAdminUI.scooter_beheer()
        elif keuze == "3":
            SystemAdminUI.traveller_beheer()
        elif keuze == "4":
            SystemAdminUI.service_engineer_beheer()
        elif keuze == "5":
            SystemAdminUI.backup_logs_menu()
        elif keuze == "6":
            overzicht_gebruikers()
        elif keuze == "7":
            print("Uitloggen...")
            time.sleep(1)
            LoginUI.login_screen()
            return
        else:
            input("Ongeldige keuze. Druk op Enter om opnieuw te proberen.")


def super_admin_menu(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Super Administrator Menu (Ingelogd als: {username})")
        print("1. (placeholder)")
        print("2. (placeholder)")
        print("3. Uitloggen")

        keuze = input("\nMaak een keuze (1-3): ")
        if keuze == "1":
            input("(placeholder)")
        elif keuze == "2":
            input("(placeholder)")
        elif keuze == "3":
            print("Uitloggen...")
            time.sleep(10)
            LoginUI.login_screen()
            return
        else:
            input("Ongeldige keuze. Druk op Enter om opnieuw te proberen.")

def main_menu(username):
    admin_type = get_admin_type(username)

    if admin_type == "Service Engineer":
        service_engineer_menu(username)
    elif admin_type == "System Administrator":
        system_admin_menu(username)
    elif admin_type == "Super Administrator":
        super_admin_menu(username)
    else:
        print("Onbekend admin type. Neem contact op met de systeembeheerder.")
        input("Druk op Enter om terug te keren.")