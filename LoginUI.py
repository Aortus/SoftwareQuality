import os
import Login
import MenuUI

def login_screen():
    while True:
        print("Login Scherm")
        username = input("Username: ")
        password = input("Wachtwoord: ")

        result = Login.login(username, password)

        if result == "Login succesful":
            print("\nLogin gelukt! Welkom,", username)
            MenuUI.main_menu(username)
            break
        else:
            print("\nFout bij het inloggen:")
            input("Druk Enter om opnieuw te proberen")

if __name__ == "__main__":
    login_screen()