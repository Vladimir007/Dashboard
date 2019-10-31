import yaml
from io import BytesIO

from wsgiref.util import FileWrapper

from core.models import Action, Unit, Category


class ActionsFileGenerator(FileWrapper):
    def __init__(self):
        content = self.__get_actions()
        self.name = 'actions.yaml'
        self.size = len(content)
        super().__init__(BytesIO(content), 8192)

    def __get_actions(self):
        data = {'actions': []}
        for action in Action.objects.order_by('id'):
            data['actions'].append({
                'id': action.id,
                'parent_id': action.parent_id or 0,
                'phrases': action.phrases
            })
        return yaml.dump(data, allow_unicode=True).encode('utf-8')


class UnitsFileGenerator(FileWrapper):
    def __init__(self):
        content = self.__get_units()
        self.name = 'units.yaml'
        self.size = len(content)
        super().__init__(BytesIO(content), 8192)

    def __get_units(self):
        data = {'units': []}
        for unit in Unit.objects.order_by('id'):
            data['units'].append({
                'id': unit.id,
                'parent_id': unit.parent_id or 0,
                'names': unit.names
            })
        return yaml.dump(data, allow_unicode=True).encode('utf-8')


class CategoriesFileGenerator(FileWrapper):
    def __init__(self):
        content = self.__get_categories()
        self.name = 'categories.yaml'
        self.size = len(content)
        super().__init__(BytesIO(content), 8192)

    def __get_categories(self):
        data = {'categories': []}
        for category in Category.objects.order_by('id'):
            data['categories'].append({
                'id': category.id,
                'parent_id': category.parent_id or 0,
                'name': category.name
            })
        return yaml.dump(data, allow_unicode=True).encode('utf-8')
