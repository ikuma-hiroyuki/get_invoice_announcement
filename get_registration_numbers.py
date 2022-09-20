def get_number_list():
    with open("registration_numbers.csv", "r") as file:
        return [_.replace("\n", "") for _ in file.readlines()]
