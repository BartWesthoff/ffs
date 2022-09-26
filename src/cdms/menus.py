from src.cdms.exceptions import Exceptions
from src.cdms.helperClass import Helper
from src.cdms.personCrudClass import PersonCRUD as crud
from src.cdms.userinterfaceClass import UserInterface, Role

## all actions

"""
list of users
check member
add member
modify member
delete member
add a new advisor
modify advisor
delete advisor
change password
add a new system administrator
modify system administrator
delete system administrator
make a backup
restore a backup
see log(s)
logout
"""


class Action:

    def __init__(self, name, access_level, function, argument):
        self.name = name
        self.acces_level = access_level
        self.function = function
        self.arguments = argument


def menu(user_access_level: int):
    """ TO DEBUG: menu(Role.SUPER_ADMINISTATOR) | menu(Role.SYSTEM_ADMINISTATOR) | menu(Role.ADVISOR) or use 0, 1, 2 """
    check_member = Action("check member", Role.ADVISOR, crud.search_person, "member")
    add_member = Action("add member", Role.ADVISOR, crud.addPerson, "member")
    modify_member = Action("modify member", Role.ADVISOR, crud.modify_person, "member")
    change_password = Action("change password", Role.ADVISOR, crud.changePassword, "advisor")

    list_of_users = Action("list of users", Role.SYSTEM_ADMINISTATOR, crud.checkUsers, None)
    add_new_advisor = Action("add advisor", Role.SYSTEM_ADMINISTATOR, crud.addPerson, "advisor")
    modify_advisor = Action("modify advisor", Role.SYSTEM_ADMINISTATOR, crud.modify_person, "advisor")
    delete_advisor = Action("delete advisor", Role.SYSTEM_ADMINISTATOR, crud.delete_person, "advisor")
    # reset_advisor_password = Action("reset advisor password", Role.SYSTEM_ADMINISTATOR) ## not implemented

    # TODO: testen!!!
    # make_a_backup = Action("make a backup", Role.SYSTEM_ADMINISTATOR, Helper.make_backup)
    # restore_a_backup = Action("restore a backup", Role.SYSTEM_ADMINISTATOR, Helper.restore_backup)
    # see_logs = Action("see log(s)", Role.SYSTEM_ADMINISTATOR, Helper.see_logs)

    delete_member = Action("delete member", Role.SYSTEM_ADMINISTATOR, crud.delete_person, "member")

    # reset_system_admin_password = Action("reset system administator password", Role.SUPER_ADMINISTATOR) ## not implemented
    add_system_administrator = Action("add system administrator", Role.SUPER_ADMINISTATOR, crud.addPerson,
                                      "systemadmin")
    modify_system_administrator = Action("modify system administrator", Role.SUPER_ADMINISTATOR, crud.modify_person,
                                         "systemadmin")
    delete_system_administrator = Action("delete system administrator", Role.SUPER_ADMINISTATOR, crud.delete_person,
                                         "systemadmin")

    logout = Action("logout", Role.ADVISOR, UserInterface.main_screen, None)

    actions = [list_of_users, check_member, add_member, modify_member, change_password, add_new_advisor, modify_advisor,
               delete_advisor,
               # make_a_backup, restore_a_backup, see_logs,
               delete_member, add_system_administrator,
               modify_system_administrator, delete_system_administrator, logout]

    available_actions = []
    for action in actions:
        if user_access_level >= action.acces_level:
            available_actions.append(action)
    options = [action.name for action in available_actions]
    choice = UserInterface().choices(options)

    chosen_function = available_actions[choice - 1]
    if chosen_function.arguments is None:
        chosen_function.function()
    else:
        chosen_function.function(chosen_function.arguments)
