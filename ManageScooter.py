import sqlite3
import Encryption

def get_all_scooters():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters")
    scooters = cursor.fetchall()
    conn.close()

    decrypted_scooters = []
    for scooter in scooters:
        scooter_list = list(scooter)
        for i in range(0, len(scooter_list)):
            if i == 0:
                continue
            scooter_list[i] = Encryption.decrypt_data(scooter_list[i])
        decrypted_scooters.append(tuple(scooter_list))

    return decrypted_scooters

def print_all_scooters():
    scooters = get_all_scooters()
    for scooter in scooters:
        print_scooter_info(scooter)

def print_scooter_info(scooter):
    print(
        f"\nScooter Informatie:\n"
        f"1. ID: {scooter[0]}\n"
        f"2. Brand: {scooter[1]}\n"
        f"3. Model: {scooter[2]}\n"
        f"4. Serialnumber: {scooter[3]}\n"
        f"5. Topspeed: {scooter[4]} km/h\n"
        f"6. Batterycapacity: {scooter[5]} km\n"
        f"7. State Of Charge: {scooter[6]}\n"
        f"8. Target State Of Charge: {scooter[7]}\n"
        f"9. Location: {scooter[8]}\n"
        f"10. Out of Service: {'Ja' if scooter[9] == '1' else 'Nee'}\n"
        f"11. Mileage: {scooter[10]} km\n"
        f"12. Last Maintenance: {scooter[11]}\n"
    )