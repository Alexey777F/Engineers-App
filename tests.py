import unittest
from db import EngineerCalculateMetriks

class TestEngineerCalculateMetriks(unittest.TestCase):

    def setUp(self):
        self.engineer_calculator = EngineerCalculateMetriks()

    def test_engineers_directions_dict(self):
        # Тестирование метода engineers_directions_dict
        result = self.engineer_calculator.engineers_directions_dict()
        # Проверяем, что результат не пустой и является словарем
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

    def test_find_vacation(self):
        # Тестирование метода find_vacation
        direction = 'СПД'
        result = self.engineer_calculator.find_vacation(direction)
        # Проверяем, что результат не пустой и является списком
        self.assertTrue(result)
        self.assertIsInstance(result, list)

    def test_count_tasks(self):
        # Тестирование метода count_tasks
        find_vacation = [3, 6]
        result = self.engineer_calculator.count_tasks(find_vacation)
        # Проверяем, что результат не пустой и является списком
        self.assertTrue(result)
        self.assertIsInstance(result, list)

    def test_compare_last_orders(self):
        # Тестирование метода compare_last_orders
        count_tasks = [3, 6]
        result = self.engineer_calculator.compare_last_orders(count_tasks)
        # Проверяем, что результат не пустой и является числом или строкой
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, (int, str)))


if __name__ == '__main__':
    unittest.main()
