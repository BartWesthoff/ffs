from src.cdms.memberClass import Member
from src.cdms.userinterfaceClass import UserInterface, Role
from src.cdms.menus import *

if __name__ == "__main__":
    # UserInterface().main_screen()
    member = Member().dummy_member()

    print(str(member))

    member = Member().create_member()
    print(str(member))
    print("\n")
    print(member)
