import unittest
from datetime import datetime
from profile import Profile, ProfileManager, DEFAULT_DATETIME_FORMAT


class TestProfiles(unittest.TestCase):
    def setUp(self):
        self.profile_manager = ProfileManager()
        self.create_data_correct_1 = {
            "first_name": "Иван",
            "second_name": "Иванов",
            "middle_name": "Иванович",
            "birthday": "2001-02-03",
            "work": "Преподаватель",
            "worked_years": 3
        }
        self.create_data_correct_2 = {
            "first_name": "Шишкин",
            "second_name": "Теодор",
            "middle_name": "Львович",
            "birthday": "1985-07-23",
            "work": "Шахтер",
            "worked_years": 20
        }
        self.create_data_incorrect_1 = {
            # отсутствует один из ключей "work"
            "first_name": "НеИван",
            "second_name": "НеИванов",
            "middle_name": "НеИванович",
            "birthday": "1991-11-10",
            "worked_years": 13
        }
        self.create_data_incorrect_2 = {
            # некорректный ключ "work_one"
            "first_name": "Петр",
            "second_name": "Петров",
            "middle_name": "Петрович",
            "birthday": "1990-12-05",
            "work_one": "Маг",
            "worked_years": 3
        }
        self.create_data_incorrect_3 = {
            # неверный формат даты "birthday"
            "first_name": "Джон",
            "second_name": "Джонов",
            "middle_name": "Джонович",
            "birthday": "95-04-01",
            "work": "Надзиратель",
            "worked_years": 9
        }
        self.create_data_incorrect_4 = {
            # неверный тип данных "worked_years"
            "first_name": "Имя",
            "second_name": "Фамилия",
            "middle_name": "Отчество",
            "birthday": "1995-04-01",
            "work": "Надзиратель",
            "worked_years": "14"
        }
        self.create_data_incorrect_5 = [
            # неверный тип данных
            "first_name",
            "Имя",
            "second_name",
            "Фамилия",
        ]
        self.update_data_correct = {
            "second_name": "Пупкин",
            "work": "Ученый",
            "worked_years": 4
        }
        self.update_data_incorrect = {
            # некорректный ключ "years"
            "second_name": "Шишкин",
            "work": "Водитель",
            "years": 6
        }

    # create data validation
    def test_create_data_validation_true(self):
        result = self.profile_manager.is_create_data_valid(data=self.create_data_correct_1)
        self.assertTrue(result)

    def test_create_data_validation_false_case_1(self):
        result = self.profile_manager.is_create_data_valid(data=self.create_data_incorrect_1)
        self.assertFalse(result)

    def test_create_data_validation_false_case_2(self):
        result = self.profile_manager.is_create_data_valid(data=self.create_data_incorrect_2)
        self.assertFalse(result)

    def test_create_data_validation_false_case_3(self):
        result = self.profile_manager.is_create_data_valid(data=self.create_data_incorrect_3)
        self.assertFalse(result)

    def test_create_data_validation_false_case_4(self):
        result = self.profile_manager.is_create_data_valid(data=self.create_data_incorrect_4)
        self.assertFalse(result)

    def test_create_data_validation_false_case_5(self):
        result = self.profile_manager.is_create_data_valid(data=self.create_data_incorrect_5)
        self.assertFalse(result)

    # update data validation
    def test_update_data_validation_true(self):
        result = self.profile_manager.is_update_data_valid(data=self.update_data_correct)
        self.assertTrue(result)

    def test_update_data_validation_false(self):
        result = self.profile_manager.is_update_data_valid(data=self.update_data_incorrect)
        self.assertFalse(result)

    # create profile
    def test_create_profile(self):
        self.profile_manager.create(data=self.create_data_correct_1)
        self.assertEqual(len(self.profile_manager.profiles), 1)
        profile = self.profile_manager.profiles[0]
        for key, value in self.create_data_correct_1.items():
            self.assertEqual(getattr(profile, key), value)
        self.assertEqual(profile.age, 23)
        date_today = datetime.now().date().strftime(DEFAULT_DATETIME_FORMAT)
        self.assertEqual(profile.created_date, date_today)

    # update profile
    def test_update_profile(self):
        self.profile_manager.create(data=self.create_data_correct_1)
        profile = self.profile_manager.profiles[0]
        self.profile_manager.update(profile_index=0, data=self.update_data_correct)
        for key, value in self.update_data_correct.items():
            self.assertEqual(getattr(profile, key), value)

    # profile age
    def test_profile_age(self):
        profile = Profile(data=self.create_data_correct_2)
        self.assertEqual(profile.age, 38)
