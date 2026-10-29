import secrets
import string

print("===== Random Password Generator =====")

while True:
    try:
        length = int(input("\nEnter password length (8-64): "))

        if length < 8 or length > 64:
            print("Please enter a length between 8 and 64.")
            continue

        characters = (
            string.ascii_letters
            + string.digits
            + string.punctuation
        )

        password = ""

        for i in range(length):
            password += secrets.choice(characters)

        print("Generated Password:", password)

        choice = input(
            "Generate another password? (yes/no): "
        ).lower()

        if choice != "yes":
            print("Thank you for using the Password Generator!")
            break

    except ValueError:
        print("Invalid input! Please enter a number.")