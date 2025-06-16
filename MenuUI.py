import os
import LoginUI
import sqlite3
import time
import ServiceEngineerLogic

def get_admin_type(username):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT admin_type FROM admins WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

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
            ServiceEngineerLogic.update_scooter_attributes()
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