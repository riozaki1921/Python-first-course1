from abc import ABC, abstractmethod
from enum import IntEnum
import logging
from functools import wraps
from logger_config import init_logger

init_logger()
logger = logging.getLogger(__name__)

class Role(IntEnum):
    GUEST = 1
    RESIDENT = 2
    ADMIN = 3

    @property
    def value_str(self):
        return self.name.lower()


class User:
    def __init__(self, name, role: Role):
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.role.value_str})"


def requires_role(role: Role):
    def decorator(func):
        func.min_role = role

        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) > 1 and isinstance(args[1], User):
                user = args[1]
                if user.role < role:
                    logger.error(
                        f"Доступ запрещен для {user.name}! Недостаточно прав. "
                        f"(Ваш уровень: {int(user.role)}, Требуется: {int(role)})"
                    )
                    return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Device(ABC):
    def __init__(self, device_id, name):
        if device_id is None:
            raise TypeError("Device ID cannot be None")
        self.device_id = device_id
        self.name = name
        self.is_on = False

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def status(self):
        pass

    def get_base_status(self):
        return f"{self.name}: {'вкл' if self.is_on else 'выкл'}"


class Light(Device):
    def __init__(self, device_id, name, brightness=50):
        super().__init__(device_id, name)
        self._brightness = brightness

    @requires_role(Role.GUEST)
    def turn_on(self):
        self.is_on = True
        return f"Лампа {self.name} включена"

    @requires_role(Role.GUEST)
    def turn_off(self):
        self.is_on = False
        return f"Лампа {self.name} выключена"

    @requires_role(Role.RESIDENT)
    def set_brightness(self, value):
        if 0 <= value <= 100:
            self._brightness = value
            return f"Яркость лампы {self.name} изменена на {value}%"
        else:
            raise ValueError("Яркость должна быть в диапазоне от 0 до 100")

    def status(self):
        base = self.get_base_status()
        return f"{base}, яркость: {self._brightness}%"


class Thermostat(Device):
    def __init__(self, device_id, name, current_temp=20):
        super().__init__(device_id, name)
        self.current_temp = current_temp
        self.target_temp = current_temp

    @requires_role(Role.RESIDENT)
    def turn_on(self):
        self.is_on = True
        return f"Термостат {self.name} включен"

    @requires_role(Role.RESIDENT)
    def turn_off(self):
        self.is_on = False
        return f"Термостат {self.name} выключен"

    @requires_role(Role.RESIDENT)
    def set_temperature(self, temp):
        if 10 <= temp <= 30:
            self.current_temp = temp
            self.target_temp = temp
            return f"Температура установлена на {temp}°C"
        else:
            raise ValueError("Температура должна быть в диапазоне от 10 до 30°C")

    def status(self):
        base = self.get_base_status()
        return f"{base}, текущая: {self.current_temp}°C, целевая: {self.target_temp}°C"


class Camera(Device):
    def __init__(self, device_id, name):
        super().__init__(device_id, name)
        self.is_recording = False

    @requires_role(Role.ADMIN)
    def turn_on(self):
        self.is_on = True
        return f"Камера {self.name} включена"

    @requires_role(Role.ADMIN)
    def turn_off(self):
        self.is_on = False
        self.is_recording = False
        return f"Камера {self.name} выключена"

    @requires_role(Role.ADMIN)
    def start_recording(self):
        if self.is_on:
            self.is_recording = True
            return "Запись начата"
        return "Сначала включите камеру"

    @requires_role(Role.ADMIN)
    def stop_recording(self):
        self.is_recording = False
        return "Запись остановлена"

    def status(self):
        if getattr(self, "_broken", False):
            raise ConnectionError("Камера не отвечает по сети")
        base = self.get_base_status()
        recording_status = "идет запись" if self.is_recording else "запись остановлена"
        return f"{base}, статус: {recording_status}"


class SmartHome:
    def __init__(self):
        self.devices = {}

    @requires_role(Role.ADMIN)
    def add_device(self, user, device):
        if device is None:
            logger.error("Объект устройства равен None")
            return

        device_id = getattr(device, "device_id", None)
        if device_id is None:
            logger.error(f"Ошибка добавления: Устройство '{getattr(device, 'name', 'Неизвестно')}' не имеет корректного ID")
            return

        if device_id in self.devices:
            logger.warning(f"Ошибка добавления: Устройство с ID '{device_id}' уже существует ")
            return

        self.devices[device_id] = device
        logger.info(f"Устройство {device.name} успешно добавлено администратором {user.name}")

    @requires_role(Role.ADMIN)
    def remove_device(self, user, device_id):
        if device_id is None:
            logger.warning("Переданный device_id равен None")
            return

        if device_id in self.devices:
            device = self.devices.pop(device_id)
            logger.info(f"Устройство {device.name} удалено администратором {user.name}")
        else:
            logger.warning(f"Устройство {device_id} не найдено")

    def control_device(self, user, device_id, action, *args):
        if device_id is None:
            logger.warning("Переданный device_id равен None")
            return

        device = self.devices.get(device_id)
        if not device:
            logger.warning(f"Устройство {device_id} не найдено")
            return

        method = getattr(device, action, None)
        if method is None:
            logger.error(f"Ошибка: Устройство не поддерживает команду '{action}'.")
            return

        min_required_role = getattr(method, "min_role", Role.GUEST)

        if user.role < min_required_role:
            logger.error(
                f"Доступ запрещен для {user.name}! Недостаточно прав на устройство. "
                f"(Ваш уровень: {int(user.role)}, Требуется: {int(min_required_role)})")
            return

        try:
            result = method(*args)
            logger.info(f"Успешно ({user.name}): {result}")
        except Exception as e:
            logger.error(f"Ошибка выполнения '{action}' на {device_id}: {str(e)}")

    def list_devices(self):
        if not self.devices:
            logger.info("В системе нет зарегистрированных устройств")
            return

        logger.info("Устройства в системе:")
        for device_id, device in self.devices.items():
            try:
                device_status = device.status()
                logger.info(f"- {device_id}: {device_status}")
            except Exception as e:
                logger.error(f"Ошибка получения статуса ({str(e)})")


def demo_smart_home():
    home = SmartHome()

    admin = User("Аня", Role.ADMIN)
    guest = User("Иван", Role.GUEST)

    lamp = Light("L1", "Лампа в гостиной", brightness=50)
    thermostat = Thermostat("T1", "Термостат в спальне", current_temp=22)
    camera = Camera("C1", "Камера у входа")

    logger.info("Права на добавление устройств")
    home.add_device(guest, lamp)

    home.add_device(admin, lamp)
    home.add_device(admin, thermostat)
    home.add_device(admin, camera)

    logger.info("Дублирование устройств")
    duplicate_lamp = Light("L1", "Новая лампа-дубликат")
    home.add_device(admin, duplicate_lamp)

    logger.info("Работа системы")
    home.control_device(guest, "L1", "turn_on")
    home.control_device(guest, "L1", "set_brightness", 80)

    logger.info("Сбой устройства при выводе статуса")
    camera._broken = True
    home.list_devices()


if __name__ == "__main__":
    demo_smart_home()
