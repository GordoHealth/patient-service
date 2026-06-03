from faker import Faker


class FakerFactory():
    def __init__(self, faker_instance):
        self._faker = faker_instance or Faker()
        self._builders = {}

    def _register_builder(self, model, builder):
        self._builders[model] = builder

    def create(self, model):
        builder = self._builders.get(model)
        return builder()
