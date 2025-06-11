from colorama import Fore, Style
import Users


print("Welcome To King Ahmed's Era <3" + Style.RESET_ALL)
print(Fore.RED + "Welcome To King Ahmed's Era <3" + Style.RESET_ALL)
print(Fore.YELLOW + "Welcome To King Ahmed's Era <3 " + Style.RESET_ALL)
print(Fore.BLUE + "Welcome To King Ahmed's Era <3 " + Style.RESET_ALL)
while True:
    selection = Users.functionInput()
    if selection == 1:
        user1 = Users.User()
    elif selection == 2:
        Users.UserLogin()
    elif selection == 3:
        email = Users.userEmailInput()
        password = Users.get_password("Enter your password:\n")
        Users.DeleteAccount(email, password)
        if not Users.Again():
            break
    elif not selection:
        break
