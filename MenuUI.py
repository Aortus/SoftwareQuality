import os
import LoginUI
import sqlite3
import time
import ServiceEngineerLogic
import Logs
import ManageAdmin
import ManageScooter
import SystemAdminUI
import SuperAdminUI

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
            ManageScooter.search_scooter()
        elif keuze == "4":
            print("Uitloggen...")
            time.sleep(10)
            LoginUI.login_screen()
            return
        else:
            input("Ongeldige keuze. Druk op Enter om opnieuw te proberen.")

def system_admin_menu(username):
    if Logs.check_unread_suspicious_logs():
        print("\nWaarschuwing: Er zijn ongelezen verdachte logbestanden!")
        keuze = input("Wil je deze nu bekijken? (ja/nee): ").lower()
        if keuze == "ja":
            logs = Logs.get_unread_suspicious_logs()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Verdachte ongelezen logbestanden:\n")
            for log in logs:
                print(f"Log ID      : {log[0]}")
                print(f"Timestamp   : {log[1]}")
                print(f"User ID     : {log[2]}")
                print(f"Action      : {log[3]}")
                print(f"Details     : {log[4]}")
                print(f"Status      : {log[5]}\n")
            input("Druk op Enter om verder te gaan naar het hoofdmenu...")

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
            ManageAdmin.print_all_admins()
            input("Druk op Enter om terug te keren naar het menu...")
        elif keuze == "7":
            print("Uitloggen...")
            time.sleep(1)
            LoginUI.login_screen()
            return
        else:
            input("Ongeldige keuze. Druk op Enter om opnieuw te proberen.")


def super_admin_menu(username):
    if Logs.check_unread_suspicious_logs():
        print("\nWaarschuwing: Er zijn ongelezen verdachte logbestanden!\n")
        keuze = input("Wil je deze nu bekijken? (j/n): ").lower()
        if keuze == "j":
            logs = Logs.get_unread_suspicious_logs()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Verdachte ongelezen logbestanden:\n")
            for log in logs:
                print(f"Log ID      : {log[0]}")
                print(f"Timestamp   : {log[1]}")
                print(f"User ID     : {log[2]}")
                print(f"Action      : {log[3]}")
                print(f"Details     : {log[4]}")
                print(f"Status      : {log[5]}\n")
            input("Druk op Enter om verder te gaan naar het hoofdmenu...")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Super Administrator Menu (Ingelogd als: {username})")
        print("1. Account beheer")
        print("2. Scooter beheer")
        print("3. Travellers beheer")
        print("4. Service Engineer beheer")
        print("5. System Administrator beheer")
        print("6. Backup/Logs")
        print("7. Lijst van alle gebruikers")
        print("8. Uitloggen")

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
            SuperAdminUI.system_admin_beheer()
        elif keuze == "6":
            SystemAdminUI.backup_logs_menu()
        elif keuze == "7":
            ManageAdmin.print_all_admins()
            input("Druk op Enter om terug te keren naar het menu...")
        elif keuze == "8":
            print("Uitloggen...")
            time.sleep(1)
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