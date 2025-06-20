import re
import sqlite3
import Encryption
import datetime
import ManageAdmin


# ManageTraveller.register_traveller("John", "Doe", "10-05-1990", "M", "Wijnhaven", "109", "3011WN", "Rotterdam", "john@doe.com", "12365487", "A12345678")
def register_traveller(firstname, lastname, birthdate, gender, streetname, streetnumber, zipcode, city, email, mobilephone, drivinglicense):
    if not is_valid_zipcode(zipcode):
        return "Invalid zipcode, try again! (6 characters, being 4 numbers and 2 letters)"
    if not is_valid_city(city):
        return "Invalid city, try again! (Must be one of the predefined cities)"
    if not is_valid_nl_mobile(mobilephone):
        return "Invalid mobile phone number, try again! (8 digits, without +31 or 06)"
    if not is_valid_license(drivinglicense):
        return "Invalid driving license, try again! (2 letters and 7 numbers or 1 letter and 8 numbers)"
    if not is_valid_email(email):
        return "Invalid email, try again! (Email already exists in the database)"
    
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    registration_date = Encryption.encrypt_data(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    fn_enc = Encryption.encrypt_data(firstname)
    ln_enc = Encryption.encrypt_data(lastname)
    bd_enc = Encryption.encrypt_data(birthdate)
    gender_enc = Encryption.encrypt_data(gender)
    streetname_enc = Encryption.encrypt_data(streetname)
    streetnumber_enc = Encryption.encrypt_data(streetnumber)
    zipcode_enc = Encryption.encrypt_data(zipcode)
    city_enc = Encryption.encrypt_data(city)
    email_enc = Encryption.encrypt_data(email)
    mobilephone_enc = Encryption.encrypt_data(mobilephone)
    drivinglicense_enc = Encryption.encrypt_data(drivinglicense)

    try:
        cursor.execute("INSERT INTO users (registration_date, firstname, lastname, birthdate, gender, streetname, streetnumber, zipcode, city, email, mobilephone, drivinglicense) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (registration_date, fn_enc, ln_enc, bd_enc, gender_enc, streetname_enc, streetnumber_enc, zipcode_enc, city_enc, email_enc, mobilephone_enc, drivinglicense_enc))
        conn.commit()
        return "Traveller successfully registered"
    except sqlite3.IntegrityError:
        return "Traveller registration failed"

def print_traveller_info(traveller):
    print(
        f"\nTraveller Informatie:\n"
        f"1. Voornaam: {traveller[2]}\n"
        f"2. Achternaam: {traveller[3]}\n"
        f"3. Geboortedatum: {traveller[4]} km/h\n"
        f"4. Geslacht: {traveller[5]} km\n"
        f"5. Adres: {traveller[6]} {traveller[7]}, {traveller[8]} {traveller[9]}\n"
        f"6. Email: {traveller[10]}\n"
        f"7. Mobiel nummer: {traveller[11]}\n"
        f"8. Rijbewijs: {traveller[12]}\n"
    )
    
def update_traveller(role):
    email = input("Voer de email van de traveller in: ")

    travellers = get_all_travellers()
    traveller_found = None
    for traveller in travellers:
        if traveller[10] == email:
            traveller_found = list(traveller)
            break

    if not traveller_found:
        input("Traveller niet gevonden. Druk op Enter om terug te keren.")
        return

    if role.lower() in ["super administrator", "system administrator"]:
        # indexes based on your INSERT: (id=0, registration_date=1, firstname=2, lastname=3, ...)
        editable_fields = list(range(2, 13))  # allow editing all except id and registration_date
    else:
        print("Je hebt geen rechten om deze gegevens te bewerken.")
        return

    while True:
        print_traveller_info(traveller_found)
        print(f"Bewerkbare velden: {', '.join(map(str, editable_fields))}")
        idx = input("Kies een veld om aan te passen of typ 'q' om terug te keren: ").strip()

        if idx.lower() == "q":
            break

        try:
            idx = int(idx)
            if idx not in editable_fields:
                raise ValueError(f"Toegang geweigerd. Je mag alleen de velden {editable_fields} bewerken.")

            if idx == 2:
                traveller_found[2] = input("Nieuwe voornaam: ")
                if not is_valid_name(traveller_found[2]):
                    raise ValueError("Ongeldige voornaam. Gebruik alleen letters en spaties.")
            elif idx == 3:
                traveller_found[3] = input("Nieuwe achternaam: ")
                if not is_valid_name(traveller_found[3]):
                    raise ValueError("Ongeldige achternaam. Gebruik alleen letters en spaties.")
            elif idx == 4:
                traveller_found[4] = input("Nieuwe geboortedatum (YYYY-MM-DD): ")
                try:
                    datetime.datetime.strptime(traveller_found[4], "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Ongeldige geboortedatum. Gebruik het formaat YYYY-MM-DD.")
            elif idx == 5:
                traveller_found[5] = input("Nieuw geslacht: ")
            elif idx == 6:
                traveller_found[6] = input("Nieuwe straatnaam: ")
            elif idx == 7:
                traveller_found[7] = input("Nieuw huisnummer: ")
                if not traveller_found[8].isdigit:
                    raise ValueError("Ongeldige huisnummer.")
            elif idx == 8:
                traveller_found[8] = input("Nieuwe postcode: ")
                if not is_valid_zipcode(traveller_found[8]):
                    raise ValueError("Ongeldige postcode.")
            elif idx == 9:
                traveller_found[9] = input("Nieuwe stad: ")
                if not is_valid_city(traveller_found[9]):
                    raise ValueError("Ongeldige stad.")
            elif idx == 10:
                traveller_found[10] = input("Nieuw emailadres: ")
                if not is_valid_email(traveller_found[10]):
                    raise ValueError("Email is ongeldig of bestaat al.")
            elif idx == 11:
                traveller_found[11] = input("Nieuw mobiel nummer (8 cijfers): ")
                if not is_valid_nl_mobile(traveller_found[11]):
                    raise ValueError("Ongeldig mobiel nummer.")
            elif idx == 12:
                traveller_found[12] = input("Nieuw rijbewijsnummer: ")
                if not is_valid_license(traveller_found[12]):
                    raise ValueError("Ongeldig rijbewijsnummer.")

            # Encrypt all except ID
            encrypted = [
                traveller_found[0] if i == 0 else Encryption.encrypt_data(str(v)).decode()
                for i, v in enumerate(traveller_found)
            ]

            conn = sqlite3.connect("SQDB.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET 
                    firstname = ?, lastname = ?, birthdate = ?, gender = ?, 
                    streetname = ?, streetnumber = ?, zipcode = ?, city = ?, 
                    email = ?, mobilephone = ?, drivinglicense = ?
                WHERE user_id = ?
            """, (
                encrypted[2], encrypted[3], encrypted[4], encrypted[5],
                encrypted[6], encrypted[7], encrypted[8], encrypted[9],
                encrypted[10], encrypted[11], encrypted[12],
                encrypted[0]
            ))
            conn.commit()
            conn.close()

            input("Gegevens succesvol bijgewerkt. Druk op Enter om verder te gaan.")

        except Exception as e:
            input(f"Fout: {e}\nDruk op Enter om opnieuw te proberen.")

def is_valid_name(name):
    if has_null_byte(name):
        return False
    pattern = r"^[A-Za-z\s]+$"
    return re.match(pattern, name) is not None and len(name) > 0

def is_valid_zipcode(zc):
    if has_null_byte(zc):
        return False
    pattern = r"^\d{4}[A-Za-z]{2}$"
    return re.match(pattern, zc) is not None

def is_valid_city(city):
    if has_null_byte(city):
        return False
    if city in ("Amsterdam", "Rotterdam", "Barendrecht", "Utrecht", "Eindhoven", "Tilburg", "Groningen", "Almere", "Breda", "Nijmegen"):
        return True
    return False

def is_valid_nl_mobile(number): #Only enter the number, without the +31 or 06
    pattern = r"^\d{8}$"
    if has_null_byte(number):
        return False
    return re.match(pattern, number) is not None

def is_valid_license(s):
    pattern = r"^([A-Za-z]{2}\d{7}|[A-Za-z]{1}\d{8})$"
    if has_null_byte(s):
        return False
    return re.match(pattern, s) is not None

def is_valid_email(email):
    if has_null_byte(email):
        return False
    travellers = get_all_travellers()
    for traveller in travellers:
        if traveller[9] == email:
            return False
        
    return True if re.match(r"[^@]+@[^@]+\.[^@]+", email) else False

def has_null_byte(s):
    return '\x00' in s

def get_all_travellers():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    travellers = cursor.fetchall()
    conn.close()

    decrypted_travellers = []
    for traveller in travellers:
        traveller_list = list(traveller)
        for i in range(1, len(traveller_list)):
            traveller_list[i] = Encryption.decrypt_data(traveller_list[i])
        decrypted_travellers.append(tuple(traveller_list))

    return decrypted_travellers

def delete_traveller(email):
    travellers = get_all_travellers() 
    print(travellers)
    
    for traveller in travellers:
        if traveller[10] == email:
            return ManageAdmin.delete_entry_by_id("users", traveller[0])
    return "Traveller not found"
    
def search_traveller(search_term): # print(ManageTraveller.search_traveller("joh"))
    travellers = get_all_travellers()
    filtered_travellers = []

    for traveller in travellers:
        for data in traveller:
            if isinstance(data, str) and search_term.lower() in data.lower():
                filtered_travellers.append(traveller)
                break

    if filtered_travellers:
        return filtered_travellers
    else:
        return "Geen traveller gevonden met deze zoekterm"

