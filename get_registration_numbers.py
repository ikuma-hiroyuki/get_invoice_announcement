class RegistrationNumbsers:
    def __init__(self):
        self.number_list = []
        self.__get_number_list()

    def __get_number_list(self):
        with open("registration_numbers.csv", "r") as file:
            self.number_list = [_.replace("\n", "") for _ in file.readlines()]
