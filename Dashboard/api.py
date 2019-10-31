from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        serializer_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if serializer_fields:
            # Drop any fields that are not specified in the `fields`
            for field_name in set(self.fields.keys()) - set(serializer_fields):
                self.fields.pop(field_name)
