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

def is_valid_zipcode(zc):
    pattern = r"^\d{4}[A-Za-z]{2}$"
    return re.match(pattern, zc) is not None

def is_valid_city(city):
    if city in ("Amsterdam", "Rotterdam", "Barendrecht", "Utrecht", "Eindhoven", "Tilburg", "Groningen", "Almere", "Breda", "Nijmegen"):
        return True
    return False

def is_valid_nl_mobile(number): #Only enter the number, without the +31 or 06
    pattern = r"^\d{8}$"
    return re.match(pattern, number) is not None

def is_valid_license(s):
    pattern = r"^([A-Za-z]{2}\d{7}|[A-Za-z]{1}\d{8})$"
    return re.match(pattern, s) is not None

def is_valid_email(email):
    travellers = get_all_travellers()
    for traveller in travellers:
        if traveller[9] == email:
            return False

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
    
    
     

# travellers = ManageTraveller.get_all_travellers()
# for traveller in travellers:
#     print(traveller)

