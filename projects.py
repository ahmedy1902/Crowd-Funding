# -*- coding: utf-8 -*-

import os
from datetime import datetime
from colorama import Fore, Style

Main_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(Main_DIR, "users")  # مسار مجلد "users"
PROJECTS_FILE = os.path.join(Main_DIR, "projects", "projects.txt")
DONATIONS_FILE = os.path.join(Main_DIR, "projects", "donations.txt")
USER_DONATIONS_FILE = os.path.join(Main_DIR, "users", "user_donations.txt")  # مسار ملف التبرعات
# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(USER_DONATIONS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(DONATIONS_FILE), exist_ok=True)


def startDateInput():
    while True:
        start_date = input("Enter project's start date (YYYY-MM-DD):\n")
        try:
            valid_date = datetime.strptime(start_date, "%Y-%m-%d")
            if valid_date >= datetime.now():
                return valid_date
            else:
                print("Start date cannot be in the past. Please enter a valid start date.")
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")


def endDateInput(start_date):
    while True:
        end_date = input("Enter project's end date (YYYY-MM-DD):\n")
        try:
            valid_date = datetime.strptime(end_date, "%Y-%m-%d")
            if valid_date >= start_date:
                return valid_date
            else:
                print("End date cannot be before the start date. Please enter a valid end date.")
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")


def targetInput():
    while True:
        target = input("Enter project's target (e.g., 250000):\n")
        if target.isdigit():
            return float(target)
        else:
            print(Fore.RED + "Invalid target. Please enter a numeric value." + Style.RESET_ALL)


def get_next_project_id():
    if not os.path.exists(PROJECTS_FILE):
        return 1
    try:
        with open(PROJECTS_FILE, "r") as file:
            lines = file.readlines()
        if not lines:
            return 1
        last_line = lines[-1]
        last_id = int(last_line.split(",")[0])
        return last_id + 1
    except Exception as e:
        print(f"Error retrieving next project ID: {e}")
        return 1


def load_projects():
    projects = []
    if not os.path.exists(PROJECTS_FILE):
        return projects

    try:
        with open(PROJECTS_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(",")

                # التحقق من صحة البيانات
                if len(data) != 10:
                    print(
                        f"Error: Invalid project data format in line: {line.strip()} "
                        f"(Incorrect number of columns)"
                    )
                    continue

                try:
                    project_data = {
                        "project_id": int(data[0]),
                        "email": data[1],
                        "title": data[2],
                        "details": data[3],
                        "category": data[4],
                        "target": float(data[5]),
                        "start_time": datetime.strptime(data[6], "%Y-%m-%d %H:%M:%S"),
                        "end_time": datetime.strptime(data[7], "%Y-%m-%d %H:%M:%S"),
                        "donations": float(data[8]),
                        "is_active": data[9] == "True",
                    }
                    project = Project.from_file(project_data)
                    projects.append(project)
                except ValueError as ve:
                    print(f"Error: Invalid value in line: {line.strip()} - {ve}")
                except Exception as e:
                    print(f"Error: Unexpected error in line: {line.strip()} - {e}")

    except FileNotFoundError:
        print(f"Error: Project file '{PROJECTS_FILE}' not found.")

    return projects


def show_all_projects():
    projects = load_projects()
    if not projects:
        print("No projects available.")
        return

    # عرض جميع المشاريع
    for project in projects:

        donation_percentage = (project.donations / project.target) * 100 if project.target > 0 else 0
        print(
            f"ID: {project.project_id}, Title: {project.title}, Target: {project.target:.1f}, "
            f"Donations: {project.donations:.1f}, Percentage Donated: {donation_percentage:.2f}%, "
            f"Status: {'Active' if project.is_active else 'Inactive'}, "
            f"End Time: {project.end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    print(Fore.CYAN + "1. Donate" + Style.RESET_ALL)
    print(Fore.GREEN + "2. Back" + Style.RESET_ALL)
    choice = input("Please enter the number of your choice:\n")
    if choice == "1":
        # التبرع للمشروع المحدد
        donate_to_project(projects)
    elif choice == "2":
        return
    else:
        print("Invalid choice. Please select 1 to donate or 2 to go back.")
        show_all_projects()


def donate_to_project(projects):
    project_id = input(Fore.CYAN + "Enter the ID of the project you want to donate to, or 0 to return:\n")

    if project_id == "0":
        return  # العودة
    project_id = int(project_id)
    project = next((p for p in projects if p.project_id == project_id), None)

    if project:
        # التبرع للمشروع المحدد
        amount = float(input(f"Enter donation amount for {project.title}: "))
        if amount > 0:
            project.donate(amount)
        else:
            print("Invalid donation amount.")
    else:
        print("Project not found.")


def list_projects(projects, active_only=True):
    for project in projects:
        if active_only and not project.is_active:
            continue
        print(
            f"ID: {project.project_id}, Title: {project.title}, Target: {project.target}, "
            f"Status: {'Active' if project.is_active else 'Inactive'}, End Time: {project.end_time}"
        )


def list_all_projects_and_donate(projects, email):
    if not projects:
        print(Fore.YELLOW + "No projects available at the moment." + Style.RESET_ALL)
        return
    # عرض جميع المشاريع مع تفاصيلها
    for project in projects:
        # Calculate donation percentage and remaining amount
        donation_percentage = (project.donations / project.target) * 100 if project.target > 0 else 0
        remaining_amount = max(0, project.target - project.donations)

        print(
            f"{Fore.YELLOW}ID: {project.project_id},{Style.RESET_ALL} Title: {project.title}, "
            f"Target: {project.target:.1f} EGP "
            f"Remaining: {remaining_amount:.1f} EGP\n"
            f"Status: {'Active' if project.is_active else 'Inactive'},"
            f"Status: {'Active' if project.is_active else 'Inactive'}, "
            f"Start Time: {project.start_time.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"End Time: {project.end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    while True:
        print(Fore.CYAN + "1. Donate" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Back" + Style.RESET_ALL)
        print("Please enter the number of your choice:")
        choice = input()
        if choice == "1":
            # عرض المشاريع النشطة فقط
            active_projects = [project for project in projects if project.is_active]
            print("\nActive Projects:\n")
            for project in active_projects:
                donation_percentage = (project.donations / project.target) * 100 if project.target > 0 else 0
                remaining_amount = max(0, project.target - project.donations)
                print(
                    f"{Fore.YELLOW}ID: {project.project_id},{Style.RESET_ALL} Title: {project.title}, "
                    f"Target: {project.target:.1f} EGP, Donations: {project.donations:.1f} EGP, "
                    f"Remaining: {remaining_amount:.1f} EGP, "
                    f"Completed: {donation_percentage:.2f}%, "
                    f"Status: {'Active' if project.is_active else 'Inactive'},"
                    f"Start Time: {project.start_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                    f"End Time: {project.end_time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            print(
                Fore.RED
                + "Enter the ID of the project you want to donate to, or 0 to return:"
                + Style.RESET_ALL
            )
            project_id = input()
            if project_id == "0":
                break
            # البحث عن المشروع باستخدام ID المشروع
            selected_project = next(
                (project for project in active_projects if project.project_id == int(project_id)), None
            )
            if selected_project:
                amount = float(input("Enter the amount you want to donate:\n"))
                selected_project.donate(amount, email)  # تمرير معرف المستخدم هنا
            else:
                print("Invalid project ID. Please try again.")
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def list_all_projects_details(projects):
    # عرض المشاريع النشطة فقط
    print("\nActive Projects:\n")
    for project in projects:
        print(
            f"ID: {project.project_id}, Title: {project.title}, Target: {project.target} EGP, "
            f"Donations: {project.donations} EGP, "
            f"Remaining: {max(0, project.target - project.donations)} EGP\n, "
            f"Completed: {((project.donations / project.target) * 100) if project.target != 0 else 0:.2f}%, "
            f"Status: {'Active' if project.is_active else 'Inactive'}, Start Time: {project.start_time}, "
            f"End Time: {project.end_time}"
        )


def list_my_donations(email):
    user_file = f"{USER_DONATIONS_FILE}/{email}_donations.txt"

    # التحقق من وجود ملف التبرعات
    if not os.path.exists(user_file):
        print(f"No donations have been made from {email}.")
        return

    try:
        # قراءة محتوى ملف التبرع
        with open(user_file, "r") as file:
            lines = file.readlines()

            # تصفية التبرعات الخاصة بالمستخدم المحدد
            user_donations = [line for line in lines if f"Email: {email}" in line]

            if not user_donations:
                print("You have not made any donations yet.")
                return

            # عرض التبرعات للمستخدم
            print(Fore.BLUE + f"Donations made by {email}:")
            for donation in user_donations:
                print(donation.strip())

    except FileNotFoundError:
        print(f"Error: Donations file for '{email}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class Project:
    def __init__(self, email):
        self.project_id = get_next_project_id()
        self.email = email
        self.title = input("Enter project's title!\n")
        self.details = input("Enter project's details!\n")
        self.category = input("Enter project's category!\n")
        self.target = targetInput()
        self.start_time = startDateInput()
        self.end_time = endDateInput(self.start_time)
        self.donations = 0.0
        self.is_active = True
        # حذف save_to_file من هنا لمنع التكرار
        print(Fore.YELLOW + "Project created successfully!")

    @classmethod
    def from_file(cls, data):
        project = cls.__new__(cls)
        project.project_id = data["project_id"]
        project.email = data["email"]
        project.title = data["title"]
        project.details = data["details"]
        project.category = data["category"]
        project.target = data["target"]
        project.start_time = data["start_time"]
        project.end_time = data["end_time"]
        project.donations = data["donations"]
        project.is_active = data["is_active"]
        return project

    def __str__(self):
        percentage_completed = (self.donations / self.target) * 100 if self.target > 0 else 0

        return (
            f"{Fore.RED}ID: {self.project_id}, Title: {self.title}, "
            f"Target: {self.target:.1f}, Donations: {self.donations:.1f}, "
            f"Percentage Donated: {percentage_completed:.2f}%, "
            f"Status: {'Active' if self.is_active else 'Inactive'}, "
            f"End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}"
        )

    def save_to_file(self):
        try:
            # التحقق من وجود المشروع قبل الكتابة
            if os.path.exists(PROJECTS_FILE):
                with open(PROJECTS_FILE, "r") as file:
                    lines = file.readlines()
                    # التحقق من عدم وجود المشروع مسبقاً
                    for line in lines:
                        if line.startswith(f"{self.project_id},"):
                            return  # إذا وجد المشروع، لا تقم بالكتابة مرة أخرى

            # إذا لم يوجد المشروع، قم بإضافته
            with open(PROJECTS_FILE, "a") as file:
                file.write(
                    f"{self.project_id},{self.email},{self.title},{self.details},{self.category},"
                    f"{self.target},{self.start_time},{self.end_time},"
                    f"{self.donations},{self.is_active}\n"
                )
        except Exception as e:
            print(f"Error saving project to file: {e}")

    def donate(self, amount, user_email):
        # التحقق من صحة مبلغ التبرع
        if amount <= 0:
            print("Donation amount must be greater than zero!")
            return

        self.donations += amount
        remaining_amount = max(0, self.target - self.donations)
        percentage_completed = (min(self.donations, self.target) / self.target) * 100

        if self.donations >= self.target:
            self.is_active = False
            self.donations = self.target  # Ensure donations don't exceed the target

        # تحديث حالة المشروع في الملف
        self.update_project_in_file()

        # حفظ تفاصيل التبرع في ملف المشروع
        self.save_donation_to_project_file(amount, remaining_amount, percentage_completed, user_email)

        # حفظ تفاصيل التبرع في ملف المستخدم
        self.save_donation_to_user_file(amount, remaining_amount, percentage_completed, user_email)

        print(Fore.GREEN + f"Thank you for donating {amount} EGP!")
        print(Fore.YELLOW + f"Remaining amount: {remaining_amount} EGP")
        print(Fore.CYAN + f"Completed: {percentage_completed:.2f}%")
        if not self.is_active:
            print(Fore.RED + "This project has reached its target and is now inactive.")

    def save_donation_to_project_file(self, amount, remaining_amount, percentage_completed, user_email):
        try:
            # الحصول على الوقت الحالي
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(DONATIONS_FILE, "a") as file:
                file.write(
                    f"Project ID: {self.project_id}, Donation: {amount}, Remaining: {remaining_amount}, "
                    f"Completed: {percentage_completed:.2f}%, Donor Email: {user_email}, Date: {timestamp}\n"
                )
        except Exception as e:
            print(f"Error saving donation to project file: {e}")

    def save_donation_to_user_file(self, amount, remaining_amount, percentage_completed, user_email):
        try:
            # الحصول على الوقت الحالي
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # تحديد مسار ملف التبرعات الخاص بالمستخدم
            user_file = os.path.join(USER_DONATIONS_FILE, f"{user_email}_donations.txt")

            # Ensure the directory exists
            os.makedirs(os.path.dirname(user_file), exist_ok=True)

            with open(user_file, "a") as file:
                file.write(
                    f"Project ID: {self.project_id}, Donation: {amount}, Remaining: {remaining_amount}, "
                    f"Completed: {percentage_completed:.2f}%, Donor Email: {user_email}, Date: {timestamp}\n"
                )
            print(Fore.YELLOW + "Donation saved successfully")
        except Exception as e:
            print(Fore.RED + f"Error saving donation to user file: {e}")

    ########
    def update_project_in_file(self):
        try:
            lines = []
            with open(PROJECTS_FILE, "r") as file:
                lines = file.readlines()
            with open(PROJECTS_FILE, "w") as file:
                for line in lines:
                    if line.startswith(f"{self.project_id},"):
                        file.write(
                            f"{self.project_id},{self.email},{self.title},{self.details},{self.category},"
                            f"{self.target},{self.start_time},{self.end_time},"
                            f"{self.donations},{self.is_active}\n"
                        )
                    else:
                        file.write(line)
        except Exception as e:
            print(f"Error updating project in file: {e}")


def list_my_projects(email, projects):
    my_projects = [project for project in projects if project.email == email]
    if not my_projects:
        print(Fore.YELLOW + "You have not created any projects yet." + Style.RESET_ALL)
        return

    for project in my_projects:
        print(
            f"ID: {project.project_id}, Title: {project.title}, Email: {project.email}, "
            f"Target: {project.target}, Status: {'Active' if project.is_active else 'Inactive'}, "
            f"End Time: {project.end_time}"
        )


def view_project_details(project):
    print(project)
    while True:
        print("1. Donate")
        print(Fore.GREEN + "2. Back" + Style.RESET_ALL)
        choice = input("Please enter the number of your choice:\n")
        if choice == "1":
            try:
                amount = float(input("Enter the amount you want to donate:\n"))
                project.donate(amount)
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
        elif choice == "2":
            return
        else:
            print("Invalid choice. Please enter 1 or 2.")


# def main_menu(email):
# while True:
#     print(Fore.RED + "\nWhat would you like to do?"+ Style.RESET_ALL)
#     print("1. Add a new project")
#     print("2. Donate to an existing project")
#     print("3. List all projects")
#     print(Fore.GREEN + "4. Back"+ Style.RESET_ALL)

#     choice = input("\nPlease enter your choice: ")

#     if choice == '1':
#         try:
#             project = Project(email)  # تمرير البريد الإلكتروني هنا
#             print(Fore.GREEN + "Project added successfully!\n")
#         except Exception as e:
#             print(Fore.RED + f"Error adding project: {e}")
#     elif choice == '2':
#         show_all_projects()
#     elif choice == '3':
#         all_projects = load_projects()  # تغيير اسم المتغير لتجنب التداخل
#         if all_projects:
#             list_projects(all_projects, active_only=False)
#         else:
#             print("No projects found.")
#     elif choice == '4':
#         break
#     else:
#         print(Fore.RED + "Invalid choice. Please try again.")


def list_my_projects_with_options(email, projects):
    my_projects = [project for project in projects if project.email == email]
    if not my_projects:
        print("You have not created any projects yet.")
        return

    for idx, project in enumerate(my_projects, 1):
        print(
            f"{idx}. ID: {project.project_id}, Title: {project.title}, Target: {project.target}, "
            f"Donations: {project.donations}, Status: {'Active' if project.is_active else 'Inactive'}, "
            f"End Time: {project.end_time}"
        )

    while True:
        try:
            choice = int(
                input(Fore.CYAN + "Enter the number of the project you want to view, or 0 to return:\n")
            )
            if choice == 0:
                break
            selected_project = my_projects[choice - 1]
            view_and_manage_project(selected_project)
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid project number.")


def view_and_manage_project(project):
    print(f"\nProject Details:\n{project}")
    print(Fore.RED + "\n1. Delete this project")
    print(Fore.GREEN + "2. Back" + Style.RESET_ALL)

    # Check if the project has received more than 25% of its target donations
    if project.donations >= (0.25 * project.target):
        print(
            Fore.YELLOW
            + "This project has already received more than 25% of its target donations. You cannot delete it."
        )

    while True:
        choice = input("Please enter the number of your choice:\n")
        if choice == "1":
            # Show confirmation message with options
            print(
                Fore.RED
                + f"Are you sure you want to delete the project '{project.title}'?\n"
                + Style.RESET_ALL
            )
            print("1. Yes")
            print("2. No")
            confirm = input()

            if confirm == "1":
                if project.donations < (0.25 * project.target):
                    delete_project(project)
                    print(Fore.YELLOW + "Project deleted successfully!" + Style.RESET_ALL)
                    break
                else:
                    print(
                        "This project cannot be deleted because it has received more than 25% "
                        "of its target donations."
                    )
                    break
            elif confirm == "2":
                print("Deletion canceled.")
                break
            else:
                print("Invalid choice. Please enter 1 for Yes or 2 for No.")
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1 to delete or 2 to go back.")


def delete_project(project):
    # Logic to delete the project from the file
    try:
        lines = []
        with open(PROJECTS_FILE, "r") as file:
            lines = file.readlines()

        with open(PROJECTS_FILE, "w") as file:
            for line in lines:
                if not line.startswith(f"{project.project_id},"):
                    file.write(line)
    except Exception as e:
        print(f"Error deleting project: {e}")
