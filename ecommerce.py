from datetime import datetime
import os
import hashlib

# Clear the console
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Decorative Banner
def banner():
    print("\n    Welcome to the Booking System\n")

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User class
class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = hash_password(password)

    def __str__(self):
        return f"{self.name} (ID: {self.user_id})"

# Property class
class Property:
    def __init__(self, property_id, location, price, amenities, is_available=True):
        self.property_id = property_id
        self.location = location
        self.price = price
        self.amenities = amenities
        self.is_available = is_available

    def __str__(self):
        return f"{self.location} - ${self.price} per night, Amenities: {', '.join(self.amenities)}"

# Booking class
class Booking:
    def __init__(self, booking_id, property_obj, customer, check_in, check_out):
        self.booking_id = booking_id
        self.property = property_obj
        self.customer = customer
        self.check_in = datetime.strptime(check_in, "%Y-%m-%d")
        self.check_out = datetime.strptime(check_out, "%Y-%m-%d")
        self.total_price = (self.check_out - self.check_in).days * self.property.price

    def __str__(self):
        return (f"Booking({self.booking_id}): {self.customer.name} booked {self.property.location} "
                f"from {self.check_in.date()} to {self.check_out.date()} at ${self.total_price}")

# Payment class
class Payment:
    def __init__(self, payment_id, booking, amount):
        self.payment_id = payment_id
        self.booking = booking
        self.amount = amount
        self.status = "Pending"

    def process_payment(self):
        self.status = "Completed"
        return self.status

    def __str__(self):
        return f"Payment({self.payment_id}): ${self.amount}, Status: {self.status}"

# System Data
users = []
properties = [
    Property(1, "New York", 150, ["WiFi", "Parking"]),
    Property(2, "San Francisco", 200, ["WiFi", "Breakfast", "Pool"]),
    Property(3, "Los Angeles", 180, ["WiFi", "Parking", "Gym"]),
    Property(4, "Miami", 220, ["WiFi", "Pool", "Ocean View"]),
    Property(5, "Chicago", 160, ["WiFi", "Breakfast", "Fitness Center"]),
    Property(6, "Seattle", 175, ["WiFi", "Parking", "Mountain View"]),
    Property(7, "Austin", 145, ["WiFi", "Breakfast", "Pet Friendly"]),
    Property(8, "Boston", 195, ["WiFi", "Parking", "Gym"]),
    Property(9, "Las Vegas", 250, ["WiFi", "Casino Access", "Entertainment"]),
    Property(10, "Orlando", 210, ["WiFi", "Pool", "Family Friendly"]),
]

bookings = []
payments = []

# User-related functions
def register_user():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    user_id = len(users) + 1
    user = User(user_id, name, password)
    users.append(user)
    print(f"\nRegistered successfully as {user}\n")
    return user

def login_user():
    name = input("Enter your registered name: ")
    password = input("Enter your password: ")
    user = next((u for u in users if u.name == name and u.password == hash_password(password)), None)
    if user:
        print(f"\nWelcome back, {user.name}!\n")
    else:
        print("\nLogin failed. Please check your name and password.\n")
    return user

# Property-related functions
def list_properties():
    print("\nAvailable Properties:\n")
    for prop in properties:
        if prop.is_available:
            print(f"Property ID: {prop.property_id} - {prop}")

# Booking-related
def create_booking(customer):
    list_properties()
    try:
        property_id = int(input("Enter the Property ID to book: "))
        check_in = input("Enter check-in date (YYYY-MM-DD): ")
        check_out = input("Enter check-out date (YYYY-MM-DD): ")
        prop = next((p for p in properties if p.property_id == property_id and p.is_available), None)
        if prop:
            booking_id = len(bookings) + 1
            booking = Booking(booking_id, prop, customer, check_in, check_out)
            bookings.append(booking)
            prop.is_available = False
            print(f"\nBooking created successfully: {booking}\n")
            return booking
        else:
            print("Property not available for booking.\n")
            return None
    except ValueError:
        print("Invalid input. Please enter valid data.\n")

# Payment-related
def process_payment(booking):
    payment_id = len(payments) + 1
    payment = Payment(payment_id, booking, booking.total_price)
    status = payment.process_payment()
    payments.append(payment)
    print(f"Payment Status: {payment}")
    return status

# View history
def view_history(customer):
    user_bookings = [b for b in bookings if b.customer.user_id == customer.user_id]
    user_payments = [p for p in payments if p.booking.customer.user_id == customer.user_id]
    
    if not user_bookings and not user_payments:
        print("No booking or payment history found for this user.")
    else:
        if user_bookings:
            print("\nYour Booking History:\n")
            for booking in user_bookings:
                print(booking)
        if user_payments:
            print("\nYour Payment History:\n")
            for payment in user_payments:
                print(payment)

# Checkout
def checkout(customer):
    user_bookings = [b for b in bookings if b.customer.user_id == customer.user_id]
    if not user_bookings:
        print("No active bookings found for checkout.")
        return

    print("\nYour Active Bookings:\n")
    for booking in user_bookings:
        print(booking)

    try:
        booking_id = int(input("Enter the Booking ID to checkout: "))
        booking = next((b for b in user_bookings if b.booking_id == booking_id), None)
        if booking:
            booking.property.is_available = True
            bookings.remove(booking)
            print(f"\nSuccessfully checked out from {booking.property.location}.\n")
        else:
            print("Invalid Booking ID. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a valid Booking ID.\n")

# Main Program Loop
current_user = None
booking = None

while True:
    banner()
    if current_user:
        print("1. List Available Properties")
        print("2. Create a Booking")
        print("3. Process Payment")  
        print("4. View History")
        print("5. Checkout")
        print("6. Logout")  
    else:
        print("1. Register as a New Customer")
        print("2. Login as a Returning Customer")
        print("3. Exit")  

    choice = input("Choose an option: ")

    if choice == "1":
        if current_user:
            list_properties()
        else:
            current_user = register_user()
    elif choice == "2":
        if current_user:
            booking = create_booking(current_user)
        else:
            current_user = login_user()
    elif choice == "3":
        if current_user:
            if booking:
                process_payment(booking)
            else:
                print("No booking found. Create a booking first.\n")
        else:
            print("Thank you for using the Booking System. Goodbye!")
            break
    elif choice == "4":
        if current_user:
            view_history(current_user)
        else:
            print("Please register or log in first.\n")
    elif choice == "5":
        if current_user:
            checkout(current_user)
        else:
            print("Please register or log in first.\n")
    elif choice == "6":
        if current_user:
            print(f"\n{current_user.name}, you have been logged out.\n")
            current_user = None
        else:
            print("Please log in first.\n")
    elif choice == "3" and not current_user:
        print("Thank you for using the Booking System. Goodbye!")
        break
