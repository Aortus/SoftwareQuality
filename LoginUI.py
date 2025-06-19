import os
import Login
import MenuUI
import Logs

def login_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    count = 0
    while True:
        print("Login Scherm")
        username = input("Username: ")
        password = input("Wachtwoord: ")

        result = Login.login(username, password)

        if result == "Login succesful":
            print("\nLogin gelukt! Welkom,", username)
            Logs.log_activity(username, "Login", "User logged in successfully", 0)
            MenuUI.main_menu(username)
            break
        elif result == "Temporary password detected":
            print("\nTijdelijk wachtwoord gedetecteerd. Gelieve uw wachtwoord te wijzigen.")
            while True:
                new_password = input("Voer een nieuw wachtwoord in: ")
                confirm_password = input("Bevestig het nieuwe wachtwoord: ")
                if new_password == confirm_password and Login.is_valid_password(new_password):
                    change_result = Login.change_password(username, new_password)
                    if change_result == "Password changed successfully":
                        print("\nWachtwoord succesvol gewijzigd!")
                        Logs.log_activity(username, "Password Change", "User changed password successfully", 0)
                        MenuUI.main_menu(username)
                        break
                    else:
                        print("\nFout bij het wijzigen van het wachtwoord:", change_result)
                        Logs.log_activity(username, "Password Change", "User failed to change password", 1)
                        break
                else:
                    print("\nDe wachtwoorden komen niet overeen of zijn ongeldig. Probeer het opnieuw.")
        else:
            count += 1
            print("\nFout bij het inloggen:")
            Logs.log_activity(username, f"Login gefaald {count}", result, 1)
            input("Druk Enter om opnieuw te proberen")
