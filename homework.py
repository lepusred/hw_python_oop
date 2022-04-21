from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = format(round(float(duration), 3), '.3f')
        self.distance = format(round(float(distance), 3), '.3f')
        self.speed = format(round(float(speed), 3), '.3f')
        self.calories = format(round(float(calories), 3), '.3f')

    def get_message(self) -> str:
        """Выводит сообщение"""
        return str(f'Тип тренировки: {self.training_type};'
                   + f' Длительность: {self.duration} ч.;'
                   + f' Дистанция: {self.distance} км;'
                   + f' Ср. скорость: {self.speed} км/ч;'
                   + f' Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = self.__class__.__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        object_info: InfoMessage = InfoMessage(training_type,
                                               duration,
                                               distance,
                                               speed,
                                               calories)
        return object_info


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action,
                         duration,
                         weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CONST1: int = 18
        CONST2: int = 20
        DURATION_MIN: int = 60
        return ((CONST1 * (super().get_mean_speed()) - CONST2)
                * self.weight / self.M_IN_KM * (self.duration * DURATION_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        MIN: int = 60
        CONST1: float = 0.035
        CONST2: float = 0.029
        return ((CONST1 * self.weight + (super().get_mean_speed()**2
                // self.height) * CONST2 * self.weight)
                * (self.duration * MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        CONST1: float = 1.1
        CONST2: int = 2
        return (self.get_mean_speed() + CONST1) * CONST2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    variant: Dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    my_train: variant[workout_type] = variant[workout_type](*data)
    return my_train


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180])]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
