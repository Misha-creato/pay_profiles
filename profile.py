from datetime import datetime
from typing import get_type_hints


DEFAULT_DATETIME_FORMAT = "%Y-%m-%d"


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
        self.created_date: str = datetime.now().strftime(DEFAULT_DATETIME_FORMAT)

    @property
    def age(self):
        birth_date = datetime.strptime(self.birthday, DEFAULT_DATETIME_FORMAT)
        calculated_age = int((datetime.now() - birth_date).days / 365)
        return calculated_age

    def show(self):
        """
            Вывод профиля

            Returns:
                None
        """
        print(
            f'First name: {self.first_name}'
            f'Second name: {self.second_name}'
            f'Middle name: {self.middle_name}'
            f'Birthday: {self.birthday}'
            f'Age: {self.age}'
            f'Work: {self.work}'
            f'Worked years: {self.worked_years}'
        )

    def to_dict(self):
        """
            Приведение данных профиля к словарю

            Returns:
                Словарь данных
        """
        data = vars(self)
        data['age'] = self.age
        return data


class ProfileManager:

    def __init__(self):
        self.profiles = []
        # получение всех полей из класса Profile
        self.profile_fields = list(Profile.__annotations__.keys())

    def create(self, data: dict):
        """
            Создание профиля

            Args:
                data: данные профиля

            Returns:
                None
        """

        if self.is_create_data_valid(data=data):
            profile = Profile(data=data)
            self.profiles.append(profile)
        else:
            print(
                f'Не удалось создать профиль {data}'
            )

    def update(self, profile_index: int, data: dict):
        """
            Обновление профиля

            Args:
                profile_index: индекс профиля
                data: данные профиля

            Returns:
                None
        """

        if self.is_profile_index_valid(index=profile_index) and self.is_update_data_valid(data=data):
            profile = self.profiles[profile_index]
            for key, value in data.items():
                setattr(profile, key, value)
        else:
            print(
                f'Не удалось обновить данные профиля {profile_index} на данные {data}'
            )

    def get_profile(self, profile_index: int):
        """
            Получение профиля

            Args:
                profile_index: индекс профиля

            Returns:
                Профиль
        """

        if self.is_profile_index_valid(index=profile_index):
            return self.profiles[profile_index]

    @property
    def count(self):
        """
            Подсчет количества профилей

            Returns:
                Количество профилей
        """

        return len(self.profiles)

    def show_all_profiles(self):
        """
            Вывод всех профилей

            Returns:
                None
        """
        count = 1
        for profile in self.profiles:
            print(f'\nProfile {count}')
            profile.show()
            count += 1

    def is_create_data_valid(self, data: dict):
        """
            Проверка данных для создания профиля

            Args:
                data: данные для проверки

            Returns:
                Статус проверки
        """

        if not isinstance(data, dict):
            return False

        type_hints = get_type_hints(Profile)

        for field in self.profile_fields:
            right_type = type_hints.get(field)
            if data.get(field) is None or not isinstance(data[field], right_type):
                return False

        return self.is_datetime_format_valid(date_sting=data['birthday'])

    def is_datetime_format_valid(self, date_sting: str, datetime_format: str = DEFAULT_DATETIME_FORMAT):
        """
            Проверка формата datetime

            Args:
                date_sting: строка для проверки
                datetime_format: формат datetime

            Returns:
                Статус проверки
        """

        try:
            datetime.strptime(date_sting, datetime_format)
            return True
        except ValueError:
            return False

    def is_update_data_valid(self, data: dict):
        """
            Проверка данных для обновления профиля

            Args:
                data: данные для проверки

            Returns:
                Статус проверки
        """

        if not isinstance(data, dict):
            return False

        type_hints = get_type_hints(Profile)

        for key in data.keys():
            if key not in self.profile_fields or not isinstance(data[key], type_hints.get(key)):
                return False

        date = data.get('birthday')

        if date is not None:
            return self.is_datetime_format_valid(date_sting=date)

        return True

    def is_profile_index_valid(self, index: int):
        """
           Проверка индекса профиля

           Args:
               index: индекс профиля

           Returns:
               Статус проверки
       """

        if not isinstance(index, int) or index not in range(len(self.profiles)):
            return False
        return True
