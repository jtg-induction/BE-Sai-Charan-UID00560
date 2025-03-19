from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer which includes the option of excluding specified fields.
    """

    class Meta:
        abstract = True

    # custom constructor for when we want exclude certain fields.
    def __init__(self, *args, exclude_fields=None, **kwargs):
        if exclude_fields:
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)
        super().__init__(*args, **kwargs)
