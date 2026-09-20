from typing import Any

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .utils import get_all_data
from .objects import CognitiveParameter


class CognitiveFieldDescriptor:
    """
    Lazily resolves a cognitive parameter ID to a CognitiveParameter object.
    """

    def __init__(self, field):
        self.field = field
        self.attname = field.attname

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        value = instance.__dict__.get(self.attname)

        if value is None:
            return None

        if isinstance(value, CognitiveParameter):
            return value

        cognitive = self.field.get_full_data(value)

        instance.__dict__[self.attname] = cognitive

        return cognitive

    def __set__(self, instance, value):
        instance.__dict__[self.attname] = value


class CognitiveArrayFieldDescriptor:
    """
    Lazily resolves cognitive parameter IDs to CognitiveParameter objects.
    """

    def __init__(self, field):
        self.field = field
        self.attname = field.attname

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        value = instance.__dict__.get(self.attname)

        if value is None:
            return None

        if not isinstance(value, (list, tuple)):
            return value

        if all(
            isinstance(item, CognitiveParameter)
            for item in value
        ):
            return value

        resolved = self.field.get_full_data_many(value)

        instance.__dict__[self.attname] = resolved

        return resolved

    def __set__(self, instance, value):
        instance.__dict__[self.attname] = value


class CognitiveField(models.CharField):
    """
    Stores a cognitive parameter ID in the database.

    The field accepts either a cognitive parameter ID or a
    CognitiveParameter instance when saving.
    """

    descriptor_class = CognitiveFieldDescriptor

    def __init__(
        self,
        *args,
        cache_timeout: int | None = None,
        timeout: int | None = None,
        **kwargs,
    ):
        kwargs.setdefault("max_length", 36)

        self.cache_timeout = cache_timeout
        self.timeout = timeout

        super().__init__(*args, **kwargs)

    def get_prep_value(
        self,
        value: CognitiveParameter | str | int | None,
    ) -> str | None:
        if value is None:
            return None

        if isinstance(value, CognitiveParameter):
            return str(value.id)

        if isinstance(value, (str, int)):
            return str(value)

        raise ValueError(
            "CognitiveField only accepts a cognitive parameter ID "
            "or a CognitiveParameter instance."
        )

    def from_db_value(
        self,
        value: Any,
        expression,
        connection,
    ) -> str | None:
        if value is None:
            return None

        return str(value)


    def get_full_data(
        self,
        value: str | int | CognitiveParameter | None,
    ) -> CognitiveParameter | None:
        """
        Resolve a cognitive parameter ID to a CognitiveParameter object.
        """

        if value is None:
            return None

        if isinstance(value, CognitiveParameter):
            return value

        value = str(value)

        cognitive_data = get_all_data(
            self.cache_timeout,
            self.timeout
        )

        data = cognitive_data.get(value)

        if data is None:
            raise ValueError(
                f"Cognitive parameter with ID '{value}' was not found."
            )

        return CognitiveParameter(data)

    def get_full_data_many(
        self,
        values: list[str | int | CognitiveParameter] | tuple,
    ) -> list[CognitiveParameter]:
        """
        Resolve multiple cognitive parameter IDs using the shared cache.
        """

        if not values:
            return []

        cognitive_data = get_all_data(
            self.cache_timeout,
            self.timeout
        )

        resolved = []

        for value in values:
            if isinstance(value, CognitiveParameter):
                resolved.append(value)
                continue

            value = str(value)

            data = cognitive_data.get(value)

            if data is None:
                raise ValueError(
                    f"Cognitive parameter with ID '{value}' was not found."
                )

            resolved.append(
                CognitiveParameter(data)
            )

        return resolved


class CognitiveArrayField(ArrayField):
    """
    Stores a list of cognitive parameter IDs in the database.

    Values are stored as IDs and lazily resolved to CognitiveParameter
    objects when the model attribute is accessed.
    """

    descriptor_class = CognitiveArrayFieldDescriptor

    def __init__(
        self,
        base_field=None,
        *args,
        cache_timeout: int | None = None,
        timeout: int | None = None,
        **kwargs,
    ):
        self.cache_timeout = cache_timeout
        self.timeout = timeout

        if base_field is None:
            base_field = CognitiveField(
                cache_timeout=cache_timeout,
                timeout=timeout,
            )

        super().__init__(
            base_field=base_field,
            *args,
            **kwargs,
        )

    def get_full_data(
        self,
        value: str | int | CognitiveParameter | None,
    ) -> CognitiveParameter | None:
        """
        Resolve a cognitive parameter ID to a CognitiveParameter object.
        """

        if value is None:
            return None

        if isinstance(value, CognitiveParameter):
            return value

        if isinstance(self.base_field, CognitiveField):
            return self.base_field.get_full_data(value)

        cognitive_field = CognitiveField(
            cache_timeout=self.cache_timeout,
            timeout=self.timeout,
        )

        return cognitive_field.get_full_data(value)

    def get_full_data_many(
        self,
        values: list[str | int | CognitiveParameter] | tuple,
    ) -> list[CognitiveParameter]:
        """
        Resolve multiple cognitive parameter IDs using the shared cache.
        """

        if not values:
            return []

        if isinstance(self.base_field, CognitiveField):
            return self.base_field.get_full_data_many(values)

        cognitive_field = CognitiveField(
            cache_timeout=self.cache_timeout,
            timeout=self.timeout,
        )

        return cognitive_field.get_full_data_many(values)

    def get_prep_value(
        self,
        value: Any,
    ) -> list[str] | None:
        """
        Prepare cognitive parameter values for database storage.
        """

        if value is None:
            return None

        if not isinstance(value, (list, tuple)):
            raise ValueError(
                "CognitiveArrayField only accepts a list or tuple."
            )

        return [
            self.get_prep_value_item(item)
            for item in value
        ]

    def get_prep_value_item(
        self,
        value: str | int | CognitiveParameter,
    ) -> str:
        """
        Prepare a single cognitive parameter value for database storage.
        """

        if isinstance(value, CognitiveParameter):
            return str(value.id)

        if isinstance(value, (str, int)):
            return str(value)

        raise ValueError(
            "CognitiveArrayField items must be cognitive parameter IDs "
            "or CognitiveParameter instances."
        )
