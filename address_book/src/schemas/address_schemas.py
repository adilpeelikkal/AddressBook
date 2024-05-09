from pydantic import BaseModel, validator


class LocationMixin:
    """
    Mixin class for validating address-related fields.
    """

    @validator("latitude")
    def validate_latitude(cls, value):
        if not value:
            raise ValueError("latitude cannot be empty")
        if value < -90 or value > 90:
            raise ValueError("Latitude value must be in between -90 and 90")
        return value

    @validator("longitude")
    def validate_longitude(cls, value):
        if not value:
            raise ValueError("longitude cannot be empty")
        if value < -180 or value > 180:
            raise ValueError("Longitude value must be in between -180 and 180")
        return value

    @validator("street", check_fields=False)
    def validate_street(cls, value):
        if not value:
            raise ValueError("Street cannot be empty")
        return value

    @validator("city", check_fields=False)
    def validate_city(cls, value):
        if not value:
            raise ValueError("city cannot be empty")
        return value

    @validator("state", check_fields=False)
    def validate_state(cls, value):
        if not value:
            raise ValueError("state cannot be empty")
        return value

    @validator("country", check_fields=False)
    def validate_country(cls, value):
        if not value:
            raise ValueError("country cannot be empty")
        return value


class AddressBase(BaseModel):
    """
    Base model for address.
    """

    street: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float


class AddressCreate(LocationMixin, AddressBase):
    """
    Model for creating an address with validation mixins.
    """

    pass


class AddressUpdate(LocationMixin, AddressBase):
    """
    Model for updating an address with validation mixins.
    """

    pass


class AddressOut(AddressBase):
    """
    Model for outputting an address.
    """

    id: int

    class Config:
        from_attributes = True


class NearBySchema(LocationMixin, BaseModel):
    """
    Model for nearby locations filter with validation mixins.
    """

    latitude: float
    longitude: float
    radius: float
