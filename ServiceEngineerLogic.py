import bcrypt
import sqlite3
import datetime
import Login
import ManageScooter
import Encryption

def update_password(username):
    new_password = input("Nieuw wachtwoord: ")
    if Login.is_valid_password(new_password):
        Login.change_password(username, new_password)
        input("Wachtwoord succesvol gewijzigd. Druk op Enter om terug te keren.")
    else:
        input("Ongeldig wachtwoord. Zorg ervoor dat het minstens 12 tekens lang is, een hoofdletter, een kleine letter, een cijfer en een speciaal teken bevat. Druk op Enter om opnieuw te proberen.")


def search_scooter():
    query = input("Zoekterm (deel van serienummer, merk, model, etc.): ").strip().lower()

    scooters = ManageScooter.get_all_scooters()
    matches = []

    for scooter in scooters:
        fields_to_search = [str(s).lower() for s in scooter]
        if any(query in field for field in fields_to_search):
            matches.append(scooter)

    if not matches:
        input("Geen scooters gevonden met die zoekterm. Druk op Enter om terug te keren.")
        return

    for idx, scooter in enumerate(matches, 1):
        print(f"\nResultaat {idx}:")
        ManageScooter.print_scooter_info(scooter)

    input("\nDruk op Enter om terug te keren.")



