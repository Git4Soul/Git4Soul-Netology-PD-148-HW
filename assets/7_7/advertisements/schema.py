from pydantic import BaseModel, ValidationError

from errors import HttpError


class CreateAdvertisement(BaseModel):
    title: str
    description: str | None = None
    owner: str


class UpdateAdvertisement(BaseModel):
    title: str | None = None
    description: str | None = None
    owner: str | None = None


def validate(
    json_data: dict,
    schema_cls: type[CreateAdvertisement | UpdateAdvertisement],
) -> dict:
    try:
        return schema_cls(**json_data).model_dump(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for e in errors:
            e.pop("ctx", None)
        raise HttpError(errors, 400)