import unittest
from datetime import datetime
from profile import Profile, ProfileManager, DATETIME_FORMAT


class TestProfiles(unittest.TestCase):
    def setUp(self):
        self.profile_manager = ProfileManager()
        self.create_data = {
            "first_name": "Иван",
            "second_name": "Иванов",
            "middle_name": "Иванович",
            "birthday": "2001-02-03",
            "work": "Маг",
            "worked_years": 3
        }
        self.update_data = {
            "second_name": "Пупкин",
            "work": "Ученый",
            "worked_years": 4
        }

    def test_create_data_validation(self):
        result = self.profile_manager.is_create_data_valid(data=self.create_data)
        self.assertTrue(result)

    def test_create_profile(self):
        self.profile_manager.create(data=self.create_data)
        self.assertEqual(len(self.profile_manager.profiles), 1)
        self.assertEqual(self.profile_manager.profiles[0].first_name, "Иван")
        self.assertEqual(self.profile_manager.profiles[0].second_name, "Иванов")
        self.assertEqual(self.profile_manager.profiles[0].middle_name, "Иванович")
        self.assertEqual(self.profile_manager.profiles[0].birthday, "2001-02-03")
        self.assertEqual(self.profile_manager.profiles[0].worked_years, 3)
        self.assertEqual(self.profile_manager.profiles[0].work, "Маг")
        self.assertEqual(self.profile_manager.profiles[0].age, 23)
        self.assertEqual(self.profile_manager.profiles[0].created_date, datetime.now().date().strftime(DATETIME_FORMAT))

    def test_update_profile(self):
        self.profile_manager.create(data=self.create_data)
        self.profile_manager.update(profile_index=0, data=self.update_data)
        self.assertEqual(self.profile_manager.profiles[0].second_name, "Пупкин")
        self.assertEqual(self.profile_manager.profiles[0].work, "Ученый")
        self.assertEqual(self.profile_manager.profiles[0].worked_years, 4)

    def test_profile_age(self):
        profile = Profile(data=self.create_data)
        self.assertEqual(profile.age, 23)



if __name__ == "__main__":
    unittest.main()
