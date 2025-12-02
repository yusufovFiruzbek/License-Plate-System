import json
import os
import datetime

USERS_FILE = "users.json"
LICENSE_PLATES_FILE = "license_plates.json"
SALES_FILE = "sales.json"

class LicensePlateManagementSystem:
    def __init__(self):
        self.users = self.load_data(USERS_FILE)
        self.license_plates = self.load_data(LICENSE_PLATES_FILE)
        self.sales = self.load_data(SALES_FILE)

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def load_data(file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        return {}

    @staticmethod
    def save_data(file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def sign_up(self):
        self.clear_screen()
        print("\nSign Up:")
        username = input("Enter username: ")
        if username in self.users:
            print("Username already exists.")
            return
        password = input("Enter password: ")
        address = input("Enter address: ")
        user_id = len(self.users) + 1
        self.users[user_id] = {"username": username, "password": password, "address": address}
        self.save_data(USERS_FILE, self.users)
        print("Account created successfully.")
        input("Press 'Enter' to go back...")

    def sign_in(self):
        self.clear_screen()
        print("\nSign In:")
        username = input("Enter username: ")
        password = input("Enter password: ")
        for user_id, user in self.users.items():
            if user["username"] == username and user["password"] == password:
                print("Login successful.")
                return username, "Admin" if username == "admin" else "Customer"
        print("Invalid credentials.")
        input("Press 'Enter' to go back...")
        return None, None

    def admin_menu(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\nAdmin Menu:")
            print("1. Manage license plate")
            print("2. View all license plates")
            print("3. View sales statistics")
            print("4. View purchase history")
            print("5. EXIT")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.manage_license_plate()
            elif choice == "2":
                self.view_license_plates()
            elif choice == "3":
                self.view_sales_statistics()
            elif choice == "4":
                self.view_purchase_history()
            elif choice == "5":
                print("Exiting Admin Menu.")
                break
            else:
                print("Invalid choice, please try again.")

    def customer_menu(self, username):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\nCustomer Menu:")
            print("1. View available license plates")
            print("2. Purchase license plate")
            print("3. Sell license plate")
            print("4. EXIT")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_available_plates()
            elif choice == "2":
                self.purchase_license_plate(username)
            elif choice == "3":
                self.sell_license_plate(username)
            elif choice == "4":
                print("Exiting Customer Menu.")
                break
            else:
                print("Invalid choice, please try again.")

    def manage_license_plate(self):
        self.clear_screen()
        print("\nManage License Plates:")
        print("1. Add license plate")
        print("2. Edit license plate")
        print("3. Delete license plate")
        choice = input("Enter your choice: ")

        if choice == "1":
            plate_number = input("Enter new license plate number: ")
            price = input("Enter price: ")
            if plate_number not in self.license_plates:
                self.license_plates[plate_number] = {"price": price, "status": 1}  # 1 for Available
                self.save_data(LICENSE_PLATES_FILE, self.license_plates)
                print(f"License plate {plate_number} added.")
            else:
                print("License plate already exists.")
            input("Press 'Enter' to go back...")
        elif choice == "2":
            plate_number = input("Enter license plate to edit: ")
            if plate_number in self.license_plates:
                new_status = input("Enter new status (1 for Available, 0 for Not Available): ")
                self.license_plates[plate_number]["status"] = int(new_status)
                self.save_data(LICENSE_PLATES_FILE, self.license_plates)
                print(f"License plate {plate_number} status updated.")
            else:
                print("License plate not found.")
            input("Press 'Enter' to go back...")
        elif choice == "3":
            plate_number = input("Enter license plate to delete: ")
            if plate_number in self.license_plates:
                del self.license_plates[plate_number]
                self.save_data(LICENSE_PLATES_FILE, self.license_plates)
                print(f"License plate {plate_number} deleted.")
            else:
                print("License plate not found.")
            input("Press 'Enter' to go back...")
        else:
            print("Invalid choice.")

    def view_license_plates(self):
        self.clear_screen()
        print("\nAll License Plates:")
        for plate, details in self.license_plates.items():
            status = "1" if details["status"] == 1 else "0"
            print(f"{plate}: Price: {details['price']}, Status: {status}")
        input("Press 'Enter' to go back...")

    def view_sales_statistics(self):
        self.clear_screen()
        print("\nSales Statistics:")
        for sale_id, sale in self.sales.items():
            print(f"ID: {sale_id}, Plate: {sale['plate_number']}, User ID: {sale['user_id']}")
        input("Press 'Enter' to go back...")

    def view_purchase_history(self):
        self.clear_screen()
        print("\nAll Purchase History:")
        try:
            if not self.sales:
                print("No purchase history available.")
                input("Press 'Enter' to go back...")
                return
            print(f"{'Username':<20}{'License Plate':<20}{'Purchased On':<20}")
            print("-" * 60)

            for sale_id, sale in self.sales.items():
                user_id = sale["user_id"]
                username = self.users.get(user_id, {}).get("username", "Unknown User")
                print(f"{username:<20}{sale['plate_number']:<20}{sale['purchased_on']:<20}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")        
        input("Press 'Enter' to go back...")

    def view_available_plates(self):
        self.clear_screen()
        print("\nAvailable License Plates:")
        for plate, details in self.license_plates.items():
            if details["status"] == 1:  # 1 for Available
                print(f"{plate}: Price: {details['price']}")
        input("Press 'Enter' to go back...")

    def purchase_license_plate(self, username):
        self.clear_screen()
        try:
            plate_number = input("Enter license plate to purchase: ").strip()
            plate = self.license_plates.get(plate_number)
            if plate and plate["status"] == 1:  # 1 for Available
                user_id = next((uid for uid, user in self.users.items() if user["username"] == username), None)
                if user_id:
                    purchase_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.license_plates[plate_number]["status"] = 0  # 0 for Not Available
                    self.sales[len(self.sales) + 1] = {
                        "plate_number": plate_number,
                        "user_id": user_id,
                        "purchased_on": purchase_date
                    }
                    self.save_data(LICENSE_PLATES_FILE, self.license_plates)
                    self.save_data(SALES_FILE, self.sales)
                    print(f"License plate {plate_number} purchased successfully on {purchase_date}.")
                else:
                    print("User not found.")
            else:
                print("License plate not available for purchase.")
        except KeyError as e:
            print(f"Key error occurred: {e}")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        input("Press 'Enter' to go back...")

    def sell_license_plate(self, username):
        self.clear_screen()
        plate_number = input("Enter license plate to sell: ")
        if plate_number not in self.license_plates:
            price = input("Enter price: ")
            self.license_plates[plate_number] = {"price": price, "status": 1} 
            self.save_data(LICENSE_PLATES_FILE, self.license_plates)
            print(f"License plate {plate_number} listed for sale.")
        else:
            print("License plate already exists in the platform.")
        input("Press 'Enter' to go back...")

    def main(self):
        self.clear_screen()
        while True:
            self.clear_screen()
            print("\nWelcome to the License Plate Management System")
            print("1. Sign In")
            print("2. Sign Up")
            print("3. EXIT")
            choice = input("Enter your choice: ")

            if choice == "1":
                username, role = self.sign_in()
                if role == "Admin":
                    self.admin_menu()
                elif role == "Customer":
                    self.customer_menu(username)
            elif choice == "2":
                self.sign_up()
            elif choice == "3":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice, please try again.")

system = LicensePlateManagementSystem()
system.main()
