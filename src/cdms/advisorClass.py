
from src.cdms.personCrudClass import PersonCRUD


class Advisor:

    def __init__(self):
        super().__init__()

    def addMember(self):
        from src.cdms.memberClass import Member
        Member().newMember()

    # To add a new member to the system

    def modifyMember(self):
        PersonCRUD().modifyPerson("member")

    # To modify or update the information of a member in the system

    def searchMember(self):
        PersonCRUD().searchPerson("member")
    # To search and retrieve the information of a member
