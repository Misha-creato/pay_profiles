import os

import requests
import datetime


class Pay:
    host = 'https://api.publicapis.org'
    api_key: str = os.environ.get('PAY_KEY', '6ad0d6d5-de6e-4bad-95ea-a5173f6ba6b6')

    def _check_pay(self, data: dict) -> bool:
        """
        Проверка на верную структуру платежа

        Args:
            data: данные для проверки

        Returns:
            Статус проверки
        """

        if not isinstance(data, dict):
            return False
        keys = [
            'requisite',
            'amount',
            'user_data'
        ]
        user_data_keys = [
            'first_name',
            'second_name',
            'middle_name',
            'birthday',
            'work',
            'created_date',
            'worked_years',
        ]
        for key in keys:
            if not data.get(key):
                return False

        user_data = data['user_data']
        if not isinstance(user_data, dict):
            return False

        for key in user_data_keys:
            if not user_data.get(key):
                return False
        return True

    def pay(self, data: dict) -> int:
        """
        Проведение платежа пользователя

        Args:
            data: данные платежа
            {
                "requisite": "+71234567890",
                "amount": 123.45,
                "user_data": {
                    "first_name": "Имя",
                    "second_name": "Фамилия",
                    "middle_name": "Отчество",
                    "birthday": "2001-02-03",
                    "work": "Старший учебник по этике",
                    "created_date": "2021-02-03",
                    "worked_years": 3
                }
            }

        Returns:
            Код состояния
            200
        """

        print(
            f'Проведение платежа {data}'
        )

        if not self._check_pay(data):
            print(
                f'Получена неверная структура платежа {data}'
            )
            return 400

        endpoint = '/entries'
        url = f'{self.host}/{endpoint}'
        headers = {
            'Autorization': self.api_key
        }

        try:
            response = requests.post(
                url=url, data=data, headers=headers
            )
        except Exception as exc:
            print(
                f'Не удалось отправить платёж {data}: {exc}'
            )
            return 500

        code = response.status_code
        if code != 200:
            print(
                f'Ошибка соверешния платежа {data}: {code}'
            )
        else:
            print(
                f'Платёж {data} успешно совершён'
            )
        return code
