# S — Single Responsibility Principle (Принцип единственной ответственности)
# Класс должен иметь только одну причину для изменения.


# Плохой пример. Класс отвечает и за генерацию, и за сохранение
class Report:
    def __init__(self, data):
        self.data = data

    def generate(self):
        return f"Report data: {self.data}"

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate())

# Хороший пример. Каждая часть имеет свою зону ответсвенности
class Report:
    def __init__(self, data):
        self.data = data

    def generate(self):
        return f"Report data: {self.data}"


class ReportSaver:
    def __init__(self, data):
        self.data = data

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.data)

# Мартин также предалагет использовать паттерн "Фасад", чтобы создавать экземпляры класса и управлять ими в одном месте
# Фасад скроет детали взаимодействия между классами и предоставит один простой метод для клиента:
class ReportFacade:
    def __init__(self, data):
        self.data = data
        self.report = Report(data)

    def create_and_save(self, filename):
        generated = self.report.generate()
        saver = ReportSaver(generated)
        saver.save_to_file(filename)
        print(f"Report saved successfully to '{filename}'")