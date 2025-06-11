import os
import re
import msvcrt
from colorama import Fore, Style
import projects as projects_module  # Rename the import to avoid conflict
import datetime
import time


def goodbyemsg():
    print(Fore.RED + "Closing.")
    time.sleep(0.1)

    print(Fore.RED + "Closing..")
    time.sleep(0.1)

    print(Fore.RED + "Closing....")
    time.sleep(0.1)

    print(Fore.RED + "Goodbye <3......")
    time.sleep(0.4)

    # إعادة تعيين الألوان
    print(Fore.RESET)


# -*- coding: utf-8 -*-
# ���� ����� ����� + ����� ������� �������

# ����� ������ ������� �������
Main_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(Main_DIR, "users")  # مسار مجلد "users"


# Registration ##########################################
def clear_screen():
    os.system("cls")


def userFnameInput():
    while True:
        Fname = input("Enter your first name:\n")
        if Fname.isalpha():
            return Fname
        else:
            print("Please enter a valid first name without numbers.")


# ���� ����� ��� ���� �� �����
def userLnameInput():
    while True:
        Lname = input("Enter your last name:\n")
        if Lname.isalpha():
            return Lname
        else:
            print("Please enter a valid last name without numbers.")


def userEmailInput():
    while True:
        Email = input("Enter your Email:\n")
        # ���� ���� ��������� ���
        if re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            return Email
        else:
            print("Please enter a valid email address.")


def get_password(prompt):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b"\r" or char == b"\n":  # ��� �� ����� ��� Enter
            print("")
            break
        elif char == b"\x08":  # ��� �� ����� ��� Backspace
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)
    return password


def DeleteAccount(email, password):
    filename = os.path.join(BASE_DIR, f"{email}X_X{password}X_X.txt")
    if os.path.exists(filename):
        print(Fore.YELLOW + "Are you sure to delete your acccount?(Y,N)\n")
        confirmaion = input()
        if confirmaion == "Y" or confirmaion == "y":
            os.remove(filename)
            print(Fore.RED + "Your account has been deleted successfully.")
        else:
            print(Fore.GREEN + "Account deletion canceled.")
    else:
        print("This account does not exist.")


def userPasswordInput():
    return get_password("Enter a new password:\n")


def userPasswordConfirmationInput():
    return get_password("Confirm your password:\n")


def userPhoneInput():
    while True:
        MobilePhone = input("Enter your MobilePhone:\n")
        # ���� ���� ������� �� ��� ���
        if re.match(r"^01[0-2,5]{1}[0-9]{8}$", MobilePhone):
            return MobilePhone
        else:
            print("Please enter a valid Egyptian mobile phone number.")


class User:
    def __init__(self):
        self.Fname = userFnameInput()
        self.Lname = userLnameInput()
        self.Email = userEmailInput()

        if self.is_email_registered(self.Email):
            print("This email is already registered. Please use a different email.")
            return

        self.Password = userPasswordInput()
        while True:
            self.PasswordConfirmation = userPasswordConfirmationInput()
            if self.PasswordConfirmation == self.Password:
                break
            else:
                print("Passwords don't match")
        self.MobilePhone = userPhoneInput()
        self.create_user_file()
        print(Fore.YELLOW + "Registration successful. Returning to main menu.")
        return

    def __str__(self):
        return self.Fname + " " + self.Lname

    def FileName(self):
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        return os.path.join(BASE_DIR, f"{self.Email}X_X{self.Password}X_X.txt")

    def create_user_file(self):
        filename = self.FileName()
        with open(filename, "w") as file:
            file.write(f"First_name:{self.Fname}\n")
            file.write(f"Last_name:{self.Lname}\n")
            file.write(f"Email:{self.Email}\n")
            file.write(f"Password:{'*' * len(self.Password)}\n")
            file.write(f"Mobile phone:{self.MobilePhone}\n")

    def is_email_registered(self, email):
        email_files = os.listdir(BASE_DIR)
        for file in email_files:
            if (
                email.lower().strip() in file.lower().strip()
            ):  # ����� �� �� ������� ������� �������� �� ��� ����� ��� ���� ���� ����� ������ ��������
                return True
        return False

    @staticmethod
    def passwordReset():
        try:
            email = userEmailInput()
            matching_files = [f for f in os.listdir(BASE_DIR) if re.match(f"{email}X_X.*.txt", f)]
            if matching_files:
                old_file = os.path.join(BASE_DIR, matching_files[0])

                # قراءة محتويات الملف القديم
                content = None
                with open(old_file, "r") as file:
                    content = file.read().split("\n")

                if content:
                    phone_line = [line for line in content if "Mobile phone:" in line][0]
                    registered_phone = phone_line.split(":")[1]
                    entered_phone = userPhoneInput()

                    if entered_phone == registered_phone:
                        newPassword = userPasswordInput()
                        while True:
                            newPasswordConfirmation = userPasswordConfirmationInput()
                            if newPasswordConfirmation == newPassword:
                                # إنشاء اسم الملف الجديد
                                new_file = os.path.join(BASE_DIR, f"{email}X_X{newPassword}X_X.txt")

                                # كتابة المحتوى في الملف الجديد
                                with open(new_file, "w") as new_f:
                                    for line in content:
                                        if line.startswith("Password:"):
                                            new_f.write(f"Password:{'*' * len(newPassword)}\n")
                                        elif line.strip():  # تجنب الأسطر الفارغة
                                            new_f.write(f"{line}\n")

                                # حذف الملف القديم بعد إغلاق جميع المقابض المفتوحة
                                import time

                                time.sleep(0.1)  # انتظار قليلاً للتأكد من إغلاق الملف
                                try:
                                    if os.path.exists(old_file):
                                        os.remove(old_file)
                                    print(
                                        Fore.GREEN + "Password has been reset successfully." + Style.RESET_ALL
                                    )
                                    print(
                                        Fore.YELLOW + "Please login with your new password." + Style.RESET_ALL
                                    )
                                except Exception:
                                    print(
                                        Fore.YELLOW
                                        + "Password updated but couldn't remove old file. "
                                        + "Please restart the application."
                                        + Style.RESET_ALL
                                    )
                                break
                            else:
                                print(Fore.RED + "Passwords don't match" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Invalid phone number" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid email" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error occurred: {str(e)}" + Style.RESET_ALL)
            print(Fore.YELLOW + "Please try again later or restart the application." + Style.RESET_ALL)

    def update_user_file(self):
        filename = self.FileName()
        with open(filename, "w") as file:
            file.write(f"First_name:{self.Fname}\n")
            file.write(f"Last_name:{self.Lname}\n")
            file.write(f"Email:{self.Email}\n")
            file.write(f"Password:{'*' * len(self.Password)}\n")
            file.write(f"Mobile phone:{self.MobilePhone}\n")


def loginInput(email):
    try:
        print(Fore.GREEN + f"Welcome back {email}!" + Style.RESET_ALL)
        print(Fore.RED + "What would you like to do?" + Style.RESET_ALL)
        print("1. Show data")
        print("2. Show my projects only")
        print("3. Create a new project")
        print("4. Show ALL projects")
        print("5. Show my donations")
        print("6. Change your data")
        print("7. Add new info as you want")
        print(Fore.GREEN + "8. Back" + Style.RESET_ALL)

        func = int(input())
        if func not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid input")
            return None
        elif func == 8:
            return False
        else:
            return func
    except ValueError:
        print("Invalid input")
        return None


def loginSelection(email, password):
    filename = AccountLogin(email, password)
    while True:
        choosen = loginInput(email)
        if choosen is None:
            continue
        elif choosen == 1:
            with open(filename, "r") as file:
                content = file.read()
                print(content)
            if not Again():
                break
        elif choosen == 2:  # Show my projects only
            all_projects = projects_module.load_projects()  # Use the renamed module
            projects_module.list_my_projects_with_options(email, all_projects)
        elif choosen == 3:  # Create a new project
            try:
                project = projects_module.Project(email)
                project.save_to_file()
                print(Fore.GREEN + "Project created and saved successfully!" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error adding project: {e}" + Style.RESET_ALL)
        elif choosen == 4:  # Show ALL projects
            all_projects = projects_module.load_projects()  # Use the renamed module
            projects_module.list_all_projects_and_donate(all_projects, email)
        elif choosen == 5:  # Show my donations
            projects_module.list_my_donations(email)  # Use the renamed module
        elif choosen == 6:  # Change your data
            if editSelection(filename):
                break
        elif choosen == 7:  # Add new info as you want
            with open(filename, "a") as file:
                file.write(input("\n" + "What do you want to add?\n") + "\n")
                print("Data added successfully.")
            if not Again():
                break
        elif not choosen:
            break


def get_current_user_info(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            user_info = {}
            for line in lines:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    user_info[key] = value
            return user_info
    except Exception as e:
        print(f"Error reading user info: {e}")
        return None


def check_old_password(filename):
    try:
        # احصل على معلومات المستخدم الحالي
        user_info = get_current_user_info(filename)
        if not user_info:
            return False

        # اطلب كلمة السر القديمة
        old_password = get_password("Enter your current password:\n")

        # تحقق من الملف باستخدام البريد الإلكتروني وكلمة السر القديمة
        email = user_info["Email"]
        old_file = os.path.join(BASE_DIR, f"{email}X_X{old_password}X_X.txt")

        if os.path.exists(old_file):
            return old_password
        else:
            print(Fore.RED + "Incorrect current password!" + Style.RESET_ALL)
            return False

    except Exception as e:
        print(f"Error checking old password: {e}")
        return False


def editSelection(filename):
    options = {
        1: "First_name",
        2: "Last_name",
        3: "Password",
        4: "Mobile phone",
        5: Fore.GREEN + "back" + Style.RESET_ALL,
    }
    print(Fore.RED + "What do you want to change?" + Style.RESET_ALL)

    for key, value in options.items():
        print(f"{key}. {value}")

    try:
        choice = int(input())
        if choice not in options:
            print("Invalid input")
            return False

        if choice == 1:
            new_value = userFnameInput()
            update_file(filename, options[choice], new_value)
        elif choice == 2:
            new_value = userLnameInput()
            update_file(filename, options[choice], new_value)
        elif choice == 3:  # تغيير كلمة السر
            old_password = check_old_password(filename)
            if old_password:
                new_value = userPasswordInput()
                while new_value != userPasswordConfirmationInput():
                    print(Fore.RED + "Passwords don't match" + Style.RESET_ALL)
                    new_value = userPasswordInput()
                update_file(filename, options[choice], new_value)
                return True
            return False
        elif choice == 4:
            new_value = userPhoneInput()
            update_file(filename, options[choice], new_value)
        elif choice == 5:
            return False
        return False
    except ValueError:
        print("Invalid input")
        return False


def update_file(filename, field, new_value):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            if line.startswith(field):
                if field == "Password":
                    updated_lines.append(f"{field}:{'*' * len(new_value)}\n")
                else:
                    updated_lines.append(f"{field}:{new_value}\n")
            else:
                updated_lines.append(line)

        if field == "Password":
            email = None
            for line in lines:
                if line.startswith("Email"):
                    email = line.split(":")[1].strip()
                    break

            if email:
                new_filename = os.path.join(BASE_DIR, f"{email}X_X{new_value}X_X.txt")
                os.rename(filename, new_filename)
                filename = new_filename

        with open(filename, "w") as file:
            file.writelines(updated_lines)
        print(f"{field} updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the file: {e}")


def AccountLogin(email, password):
    filename = os.path.join(BASE_DIR, email + "X_X" + password + "X_X.txt")
    return filename


def UserLogin():
    email = userEmailInput()
    password = get_password("Enter your password:\n")
    filename = AccountLogin(email, password)
    if not os.path.exists(filename):
        print("Invalid login")
        reset = input("Did you forget your password?(Y,N)")
        if reset == "Y" or reset == "y":
            User.passwordReset()
        else:
            UserLogin()
    else:
        loginSelection(email, password)
        return email


def functionInput():
    try:
        print(Fore.RED + "What would you like to do?" + Style.RESET_ALL)
        print("1. Register")
        print("2. Login")
        print("3. Delete account")
        print(Fore.GREEN + "4. Exit" + Style.RESET_ALL)

        func = int(input())
        if func not in [1, 2, 3, 4]:
            print("Invalid input")
            return functionInput()
        elif func == 4:
            goodbyemsg()
            # print("Goodbye <3")
            return False
        else:
            return func
    except ValueError:
        print("Invalid input")
        return functionInput()


def Again():
    while True:
        again = input(Fore.YELLOW + "Do you need another function? (Y,N)\n" + Style.RESET_ALL)
        if again == "Y" or again == "y":
            return True
        elif again == "N" or again == "n":
            goodbyemsg()
            # print("Goodbye <3")
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


# ���� ������ �������� �� ��� ��������
def record_donation(email, amount, project_name):
    matching_files = [f for f in os.listdir(BASE_DIR) if re.match(f"{email}X_X.*.txt", f)]

    if matching_files:
        user_data_file = matching_files[0]
        donation_details = f"Donation Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        donation_details += f"Project: {project_name}\n"
        donation_details += f"Amount Donated: {amount}\n"

        # ��� ����� ����� ��������� ������ ������
        with open(os.path.join(BASE_DIR, user_data_file), "a") as file:
            file.write(donation_details)
        print(Fore.GREEN + f"Your donation of {amount} for {project_name} has been recorded successfully!")
    else:
        print("User file not found. Donation not recorded.")


# ��� ����� ����� ������ �� ��� ����� ������
def make_donation(email):
    project_name = input(Fore.CYAN + "Enter the project name you want to donate to:\n")
    try:
        amount = float(input("Enter the donation amount:\n"))
        if amount > 0:
            # ����� ������ �� ��� ��������
            record_donation(email, amount, project_name)
        else:
            print("Donation amount must be positive.")
    except ValueError:
        print("Invalid amount entered.")


##############
# print("Welcome To King Ahmed's Era <3" + Style.RESET ALL)
# print(Fore.RED + "Welcome To King Ahmed's Era <3" + Style.RESET ALL)
# print(Fore.YELLOW + "Welcome To King Ahmed's Era <3 " + Style.RESET ALL)
# print(Fore.BLUE + "Welcome To King Ahmed's Era <3 " + Style.RESET ALL)
# while True:
#     selection = functionInput()
#     if selection == 1:
#         user1 = User()
#     elif selection == 2:
#         UserLogin()
#     elif selection == 3:
#         email = userEmailInput()
#         password = get_password("Enter your password:\n")
#         DeleteAccount(email, password)
#         if not Again():
#             break
#     elif selection == False:
#         break
# loginInput()
