class RegistrationNumbsers:
    def __init__(self):
        self.number_list = []

    def get_number_list(self):
        with open("registration_numbers.csv", "r") as file:
            self.number_list = [_.replace("\n", "") for _ in file.readlines()]
