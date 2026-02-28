from app.protocols import Authenticator

users = [
    ("role_user1", "Role", "User 1", "Staff"),
    ("adumble", "Albus", "Dumbledore", "Staff"),
    ("mmcgonag", "Minerva", "McGonagall", "Staff"),
    ("fflitwick", "Filius", "Flitwick", "Staff"),
    ("rlupin", "Remus", "Lupin", "Staff"),
    ("ssnape", "Severus", "Snape", "Staff"),
    ("psprout", "Pomona", "Sprout", "Staff"),
    ("hpotter", "Harry", "Potter", "Student"),
    ("hgranger", "Hermione", "Granger", "Student"),
    ("rweasley", "Ronald", "Weasley", "Student"),
    ("gweasley", "Ginny", "Weasley", "Student"),
    ("dmalfoy", "Draco", "Malfoy", "Student"),
    ("sfinnigan", "Seamus", "Finnigan", "Student"),
    ("dthomas", "Dean", "Thomas", "Student"),
    ("cchang", "Cho", "Chang", "Student"),
    ("ccreevey", "Colin", "Creevey", "Student"),
    ("dcreevey", "Dennis", "Creevey", "Student"),
    ("lbrown", "Lavender", "Brown", "Student"),
    ("ppatil", "Parvati", "Patil", "Student"),
    ("bweasley", "Bill", "Weasley", "Student"),
    ("cweasley", "Charlie", "Weasley", "Student"),
    ("pweasley", "Percy", "Weasley", "Student"),
    ("cdiggory", "Cedric", "Diggory", "Student"),
    ("rgeller", "Ross", "Geller", "Student"),
    ("br99", "Bernadette", "Rostenkowski", "Student"),
]


def to_ldap_entry(login: str, first_name: str, surname: str, user_type: str) -> dict:
    return {
        "givenName": first_name,
        "name": login,
        "sn": surname,
        "distinguishedName": {"OU": ["doc"]},
        "extensionAttribute6": user_type,
    }


DUMMY_USER_BASE = {login: to_ldap_entry(login, *rest) for login, *rest in users}


class DummyLdapAuthenticator(Authenticator):
    def authenticate(self, username: str, password: str) -> dict | None:
        return DUMMY_USER_BASE.get(username, None)
