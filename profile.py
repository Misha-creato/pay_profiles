from datetime import datetime
from typing import get_type_hints


DATETIME_FORMAT = "%Y-%d-%m"


class Profile:

    first_name: str
    second_name: str
    middle_name: str
    birthday: str
    work: str
    worked_years: int

    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
        self.created_date: str = datetime.now().strftime(DATETIME_FORMAT)

    @property
    def age(self):
        birth_date = datetime.strptime(self.birthday, DATETIME_FORMAT)
        diff = int((datetime.now() - birth_date).days / 365)
        return diff

    def show(self):
        print(
            f'First name: {self.first_name}'
            f'Second name: {self.second_name}'
            f'Middle name: {self.middle_name}'
            f'Birthday: {self.birthday}'
            f'Age: {self.age}'
            f'Work: {self.work}'
            f'Worked years: {self.worked_years}'
        )


class ProfileManager:

    # keys = [
    #     'first_name',
    #     'second_name',
    #     'middle_name',
    #     'birthday',
    #     'work',
    #     'worked_years',
    # ]

    def __init__(self):
        self.profiles = []
        self.profile_fields = list(Profile.__annotations__.keys())

    def create(self, data: dict):
        if self.is_create_data_valid(data=data):
            profile = Profile(data=data)
            self.profiles.append(profile)

    def update(self, profile_index: int, data: dict):
        profile = self.profiles[profile_index]
        for key, value in data.items():
            setattr(profile, key, value)

    @property
    def count(self):
        return len(self.profiles)

    def show_all_profiles(self):
        count = 1
        for profile in self.profiles:
            print(f'\nProfile {count}')
            profile.show()

    def is_create_data_valid(self, data: dict):
        if not isinstance(data, dict):
            return False

        type_hints = get_type_hints(Profile)

        for field in self.profile_fields:
            right_type = type_hints.get(field)
            if data.get(field) is None or not isinstance(data[field], right_type):
                return False

        return self.is_datetime_format_valid(date_sting=data['birthday'])

    def is_datetime_format_valid(self, date_sting: str):
        try:
            datetime.strptime(date_sting, DATETIME_FORMAT)
            return True
        except ValueError:
            return False

    def is_update_data_valid(self, data: dict):
        if not isinstance(data, dict):
            return False

        type_hints = get_type_hints(Profile)

        for key in data.keys():
            right_type = type_hints.get(key)
            if key not in self.profile_fields or not isinstance(data[key], right_type):
                return False

        return True

    def is_profile_index_valid(self, index: int):
        if not index.is_digit() or index not in range(len(self.profiles)):
            return False
        return True
