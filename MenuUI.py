import os
import LoginUI


def main_menu(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Hoofdmenu (Ingelogd als: {username})")
        print("optie1")
        print("optie2")
        print("uitloggen3")

        keuze = input("\nMaak een keuze (1-3): ")

        if keuze == "1":
            input("Druk op Enter om terug te keren")
        elif keuze == "2":
            input("Druk op Enter om terug te keren")
        elif keuze == "3":
            input("Druk op Enter om terug te keren")
            LoginUI.login_screen()
            return 
        else:
            print("\nOngeldige keuze.")
            input("Druk op Enter om opnieuw te proberen")
