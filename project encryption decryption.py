import multiprocessing
import os
import time
import logging

# --- Setup logging ---
logging.basicConfig(filename='activity.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# --- Cipher Functions ---
def caesar_encrypt(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=3):
    return caesar_encrypt(text, -shift)

def reverse_cipher(text):
    return text[::-1]

# --- Process Functions ---
def encryption_process(conn, message, method):
    try:
        if method == 1:
            encrypted = caesar_encrypt(message)
        elif method == 2:
            encrypted = reverse_cipher(message)
        else:
            encrypted = message

        with open("encrypted.txt", "w") as f:
            f.write(encrypted)

        logging.info("Message encrypted successfully.")
        conn.send(encrypted)
        conn.close()
    except Exception as e:
        logging.error(f"Error in encryption: {str(e)}")

def decryption_process(conn, method):
    try:
        encrypted = conn.recv()

        if method == 1:
            decrypted = caesar_decrypt(encrypted)
        elif method == 2:
            decrypted = reverse_cipher(encrypted)
        else:
            decrypted = encrypted

        with open("decrypted.txt", "w") as f:
            f.write(decrypted)

        log_message_history(encrypted, decrypted)

        logging.info("Message decrypted successfully.")
        conn.close()
    except Exception as e:
        logging.error(f"Error in decryption: {str(e)}")

# --- Extra Utility Functions ---
def log_message_history(encrypted, decrypted):
    with open("messages_log.txt", "a") as f:
        f.write(f"Encrypted: {encrypted} | Decrypted: {decrypted} | Time: {time.ctime()}\n")

def show_history():
    if os.path.exists("messages_log.txt"):
        with open("messages_log.txt", "r") as f:
            print("\n--- Message History ---")
            print(f.read())
    else:
        print("No message history found.")

def clear_files():
    for file in ["encrypted.txt", "decrypted.txt", "messages_log.txt"]:
        if os.path.exists(file):
            os.remove(file)
    print("All files cleared.")

# --- Main Menu ---
def main():
    while True:
        print("\n==== Secure Messaging System ====")
        print("1. Encrypt and Decrypt Message")
        print("2. View Message History")
        print("3. Clear All Files")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            message = input("Enter your message: ")
            print("Choose Encryption Method:\n1. Caesar Cipher\n2. Reverse Cipher")
            try:
                method = int(input("Enter method number: "))
                parent_conn, child_conn = multiprocessing.Pipe()
                p1 = multiprocessing.Process(target=encryption_process, args=(parent_conn, message, method))
                p2 = multiprocessing.Process(target=decryption_process, args=(child_conn, method))

                p1.start()
                p2.start()

                p1.join()
                p2.join()

                print("Encryption and Decryption completed. Check encrypted.txt and decrypted.txt")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "2":
            show_history()

        elif choice == "3":
            clear_files()

        elif choice == "4":
            print("Exiting Secure Messaging System.")
            break

        else:
            print("Invalid choice. Try again.")

# Entry point
if __name__ == "__main__":
    main()
