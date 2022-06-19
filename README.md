# Members-Data-Management-System
HRO year 2, period 4, assignment.


# NOTES

wnr je op een optie klikt voor bijvoorbeeld users, toon alle users en laat dan de gebruiker kiezen, dat is beter voor testen en usability voor de docenten. daar kunnen ze ook nog op gaan zeiken

lists of user werkt niet, TypeError: checkUsers() takes 0 positional arguments but 1 was given error.

telefoon nummer, zipcode etc moet nog encoden.

je kan alleen nog first en lastname aanpassen. dat moet alles zijn.

wnr je een password aanmaakt voor een advisor, admin etc krijg je deze error: 
TypeError: 'NoneType' object is not iterable
File "D:\Github\ffs\src\cdms\helperClass.py", line 19, in Encrypt
    for c in text:

logs zijn leeg.

voor input validation moet we white listing gebruiken. als we echt goed willen doen dit such as checking for NULL-Byte, range and length, Validation Functions, etc.

invalid input goed handelen ook belangrijk.

wnr je iets niet goed input, een berichtje zetten van invalid input try again, niet gwn de functie opnieuw aanroepen.