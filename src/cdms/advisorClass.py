from src.cdms.memberClass import Member
from src.cdms.personCrudClass import PersonCRUD

""""
Advisor class
"""


class Advisor:

    def __init__(self):
        super().__init__()

    @staticmethod
    def add_member():
        Member().create_member()

    # To add a new member to the system
    @staticmethod
    def modify_member():
        PersonCRUD().modify_person("member")

    # To modify or update the information of a member in the system
    @staticmethod
    def search_member():
        PersonCRUD().search_person("member")
    # To search and retrieve the information of a member
