from doctest import master
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Label, HORIZONTAL, Frame, Toplevel
from number_entry import IntEntry, StringEntry
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

# Main function to start the program
def main():
    # Create the Tk root object.
    root = tk.Tk()

    # Create the main window.
    frm_main = Frame(root)
    frm_main.master.title("Strong Password Generator")
    frm_main.pack(padx=4, pady=3, fill=tk.BOTH, expand=1)

    # Call the populate_main_window function to add labels, text entry boxes, and buttons to the main window.
    password_length_var = tk.IntVar()
    lowercase_var = tk.BooleanVar()
    uppercase_var = tk.BooleanVar()
    numbers_var = tk.BooleanVar()
    symbols_var = tk.BooleanVar()
    filename_var = tk.StringVar()
    username_var = tk.StringVar()
    website_var = tk.StringVar()
    save_var = tk.BooleanVar()

    populate_main_window(frm_main, password_length_var, lowercase_var, uppercase_var, numbers_var, symbols_var,
                          filename_var, username_var, website_var, save_var)

    # Define the function to execute when the "Generate" button is clicked
    def generate_password_click():
        """
        Collects the data stored inside each of the text entry boxes and
        sends them to the other functions in the program to execute the code
        and create a new password.

        Parameters: none
        Returns: nothing
        """
        # Get the input values from the text entry boxes
        password_length = password_length_var.get()
        password_character_list = make_character_dict()

        # Remove character types based on the checkboxes
        if not lowercase_var.get():
            password_character_list.pop("lwr")
        if not uppercase_var.get():
            password_character_list.pop("upr")
        if not numbers_var.get():
            password_character_list.pop("num")
        if not symbols_var.get():
            password_character_list.pop("sym")

        # Generate a random new password
        password = generate_password(password_length, password_character_list)

        # Open a new window displaying the new password
        show_new_password(password)

        # Save the password to a text file if the checkbox is selected
        if save_var.get():
            save_password_to_file(website_var.get(), username_var.get(), password, filename_var.get())

    # Create a button to execute the program and generate a new password
    btn_generate = ttk.Button(frm_main, width=40, text="Generate", command=generate_password_click)
    btn_generate.grid(row=6, column=1, columnspan=4, padx=3, pady=3)

    # Start the tkinter loop that processes user events
    root.mainloop()


def populate_main_window(main_frame, password_length_var, lowercase_var, uppercase_var, numbers_var, symbols_var,
                         filename_var, username_var, website_var, save_var):
    """
    Populate the main window of the program.
    Add labels, text entry boxes, and buttons to the main window.

    Parameters:
        main_frame: the main frame (window)
        password_length_var: variable for password length
        lowercase_var: variable for lowercase checkbox
        uppercase_var: variable for uppercase checkbox
        numbers_var: variable for numbers checkbox
        symbols_var: variable for symbols checkbox
        filename_var: variable for the filename entry
        username_var: variable for the username entry
        website_var: variable for the website entry
        save_var: variable for the save checkbox
    Returns: nothing
    """
    # Create labels, checkboxes, and text entry boxes
    lbl_length = ttk.Label(main_frame, text="Password Length:")
    ent_length = IntEntry(main_frame, width=10, textvariable=password_length_var)

    lbl_character_types = ttk.Label(main_frame, text="Character Types:")
    chckbx_lowercase = tk.Checkbutton(main_frame, text="Lowercase", variable=lowercase_var)
    chckbx_uppercase = tk.Checkbutton(main_frame, text="Uppercase", variable=uppercase_var)
    chckbx_numbers = tk.Checkbutton(main_frame, text="Numbers", variable=numbers_var)
    chckbx_symbols = tk.Checkbutton(main_frame, text="Symbols", variable=symbols_var)

    chckbx_save = tk.Checkbutton(main_frame, text="Save to file?", variable=save_var, onvalue=True, offvalue=False)

    lbl_filename = ttk.Label(main_frame, text="File name:")
    ent_filename = StringEntry(main_frame, width=30, textvariable=filename_var)

    lbl_username = ttk.Label(main_frame, text="Username:")
    ent_username = StringEntry(main_frame, width=30, textvariable=username_var)

    lbl_website = ttk.Label(main_frame, text="Website:")
    ent_website = StringEntry(main_frame, width=30, textvariable=website_var)

    # Place labels, checkboxes, and text entry boxes on the window
    lbl_length.grid(row=0, column=0, padx=3, pady=3)
    ent_length.grid(row=0, column=1, columnspan=4, padx=3, pady=3)

    lbl_character_types.grid(row=1, column=0, padx=3, pady=3)
    chckbx_lowercase.grid(row=1, column=1, padx=3, pady=3)
    chckbx_uppercase.grid(row=1, column=2, padx=3, pady=3)
    chckbx_numbers.grid(row=1, column=3, padx=3, pady=3)
    chckbx_symbols.grid(row=1, column=4, padx=3, pady=3)

    chckbx_save.grid(row=2, column=0, columnspan=5, padx=3, pady=3, sticky="w")

    lbl_filename.grid(row=3, column=0, padx=3, pady=3)
    ent_filename.grid(row=3, column=1, columnspan=4, padx=3, pady=3)

    lbl_username.grid(row=4, column=0, padx=3, pady=3)
    ent_username.grid(row=4, column=1, columnspan=4, padx=3, pady=3)

    lbl_website.grid(row=5, column=0, padx=3, pady=3)
    ent_website.grid(row=5, column=1, columnspan=4, padx=3, pady=3)

    # Select all checkboxes by default
    chckbx_lowercase.select()
    chckbx_uppercase.select()
    chckbx_numbers.select()
    chckbx_symbols.select()


def show_new_password(password):
    """
    Opens a new window and displays the newly generated password for the user to see.

    Parameters:
        password: the newly generated password
    Returns: nothing
    """
    # Create a new window
    newWindow = Toplevel(master)

    # Set the title and geometry of the new window
    newWindow.title("New Password")
    newWindow.geometry("200x200")

    # Create a label to display the password
    lbl_password = Label(newWindow, text=f"New Password:\n{password}")

    # Place the label in the center of the window
    lbl_password.place(relx=0.5, rely=0.5, anchor="center")


def generate_password(length, characters):
    """
    Generates a password randomly based on the input received from the user.

    Parameters:
        length: the desired length of the password
        characters: a dictionary with the desired types of characters
    Returns: a randomly generated passsword of the desired length and
        character types.
    """
    # Create an empty string to start the password
    password = ""

    for i in range(length):
        # Randomly choose a character type and a character from that type
        random_key = random.choice(list(characters.keys()))
        random_character = random.choice(characters[random_key])
        password += f"{random_character}"

    return password


def save_password_to_file(website, username, password, passwords_file):
    """
    Creates or opens a file and saves the user's information to the file.

    Parameters:
        website: the given website by the user
        username: the given username by the user
        password: the generated password
        passwords_file: the file to save the account info to
    Returns: nothing
    """
    # Open or create the file
    save_file = open(passwords_file, "a")

    # Write the website, username, and password information to the file
    save_file.write(f"Website: {website}\n")
    save_file.write(f"Username: {username}\n")
    save_file.write(f"Password: {password}\n\n")

    # Close the file
    save_file.close()


def make_character_dict():
    """
    Creates a dictionary of characters to use in a password.

    Parameters: none
    Returns: a dictionary of potential password characters
    """
    characters_dict = {
        "lwr": list(ascii_lowercase),
        "upr": list(ascii_uppercase),
        "num": list(digits),
        "sym": list(punctuation)
    }

    return characters_dict


# If this file was executed directly, call the main function
if __name__ == "__main__":
    main()
