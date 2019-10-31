import yaml
import os
import pandas as pd
import tempfile

from core.models import Action, Unit, Category
from core.serializers import ActionSerializer, UnitSerializer, CategorySerializer

BATCH_SIZE = 50000


class UploadActions:
    def __init__(self, file):
        self._data = self.__parse_file(file)
        self._parents = {}
        self.__upload()

    def __parse_file(self, file):
        return yaml.safe_load(file)['actions']

    def __get_parent(self, identifier):
        if not identifier:
            return None
        return self._parents[identifier]

    def __upload(self):
        assert isinstance(self._data, list), 'Not a list'
        identifiers = set()

        for action in self._data:
            assert isinstance(action, dict), 'Action is not a dict'
            if 'id' not in action:
                raise KeyError('Field "id" is required')
            if 'parent_id' not in action:
                raise KeyError('Field "parent_id" is required')
            if 'phrases' not in action:
                raise KeyError('Field "phrases" is required')
            if action['parent_id'] and action['parent_id'] not in identifiers:
                raise ValueError('Tree node was defined before its parent')
            identifiers.add(action['id'])

        serializer = ActionSerializer(data=self._data, fields={'phrases'}, many=True)
        serializer.is_valid(raise_exception=True)

        Action.objects.all().delete()

        for action in self._data:
            instance = Action.objects.create(
                parent_id=self.__get_parent(action['parent_id']), phrases=action['phrases']
            )
            self._parents[action['id']] = instance.id


class UploadUnits:
    def __init__(self, file):
        self._data = self.__parse_file(file)
        self._parents = {}
        self.__upload()

    def __parse_file(self, file):
        return yaml.safe_load(file)['units']

    def __get_parent(self, identifier):
        if not identifier:
            return None
        return self._parents[identifier]

    def __upload(self):
        assert isinstance(self._data, list), 'Not a list'
        identifiers = set()

        for unit in self._data:
            assert isinstance(unit, dict), 'Unit is not a dict'
            if 'id' not in unit:
                raise KeyError('Field "id" is required')
            if 'parent_id' not in unit:
                raise KeyError('Field "parent_id" is required')
            if 'names' not in unit:
                raise KeyError('Field "names" is required')
            if unit['parent_id'] and unit['parent_id'] not in identifiers:
                raise ValueError('Tree node was defined before its parent')
            identifiers.add(unit['id'])

        serializer = UnitSerializer(data=self._data, fields={'names'}, many=True)
        serializer.is_valid(raise_exception=True)

        Unit.objects.all().delete()

        for unit in self._data:
            instance = Unit.objects.create(
                parent_id=self.__get_parent(unit['parent_id']), names=unit['names']
            )
            self._parents[unit['id']] = instance.id


class UploadCategories:
    def __init__(self, category_columns, file):
        self._columns = self.__parse_columns(category_columns)
        self._parents = {}
        self.__upload(file)

    def __parse_columns(self, columns_str):
        return list(col.strip() for col in columns_str.split(','))

    def __upload(self, file):
        with tempfile.NamedTemporaryFile() as fp:
            for chunk in file.chunks():
                fp.write(chunk)
            fp.seek(0)
            file_ext = os.path.splitext(file.name)[-1]
            if file_ext == '.csv':
                return self.__save_categories(fp.name)
            raise ValueError('Only csv files are supported!')

    def __save_categories(self, file_path):
        Category.objects.all().delete()

        depth = len(self._columns)
        categories = {(): None}
        for chunk in pd.read_csv(file_path, chunksize=BATCH_SIZE):
            chunk.fillna("", inplace=True)
            for i, row in chunk.iterrows():
                category_full = tuple(row[c_col] for c_col in self._columns)
                if category_full in categories:
                    # All parents are saved as well
                    continue
                for j in range(depth):
                    if category_full[:(j + 1)] not in categories:
                        name = category_full[j]
                        if not name:
                            break
                        serializer = CategorySerializer(data={'name': name}, fields={'name'})
                        serializer.is_valid(raise_exception=True)
                        obj = serializer.save(parent_id=categories[category_full[:j]])
                        categories[category_full[:(j + 1)]] = obj.pk
