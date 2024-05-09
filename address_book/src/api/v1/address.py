from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import DuplicateException, ObjectNotFoundException
from src.helpers.utils import find_coordinates_within_radius, is_duplicate_lat_long
from src.schemas.response import Response
from src.schemas.address_schemas import (
    AddressCreate,
    AddressOut,
    AddressUpdate,
    NearBySchema,
)
from src.models.model import Address
from src.schemas.pagination import SkipLimit
from src.db.session import get_db
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_409_CONFLICT,
)

from src.helpers.crud_base import CrudBase
from src.core.dependencies import basic_security


# router = APIRouter(dependencies=[Depends(basic_security)])
router = APIRouter()

@router.get(
    "/address/near", response_model=Response[List[AddressOut]], status_code=HTTP_200_OK
)
async def get_nearby_addresses(
    user_input: NearBySchema = Depends(), db: Session = Depends(get_db)
):
    """
    Retrieves addresses within a given radius of a specified location.
    """
    crud_obj = CrudBase(Address)
    addresses = crud_obj.get_multi(db)
    data = find_coordinates_within_radius(
        user_input.latitude, user_input.longitude, addresses, user_input.radius
    )
    if not data:
        raise ObjectNotFoundException(
            message="No addresses found within the specified radius",
            status_code=HTTP_404_NOT_FOUND,
        )
    return Response(data=data)


@router.get(
    "/addresses/", response_model=Response[List[AddressOut]], status_code=HTTP_200_OK
)
async def get_address(
    skip: SkipLimit = Depends(), session: Session = Depends(get_db)
) -> Response:
    """
    Retrieves a list of addresses with pagination support.
    """
    return Response(
        data=CrudBase(Address).get_multi(
            session,
            skip=skip,
        )
    )


@router.get(
    "/addresses/{address_id}",
    response_model=Response[AddressOut],
    status_code=HTTP_200_OK,
)
def get_single_address(address_id: int, db: Session = Depends(get_db)):
    """
    Get a single address.
    """
    address = CrudBase(Address).get(db, query_filter=Address.id == address_id)
    if address:
        return Response(data=address)
    raise ObjectNotFoundException(
        message=f"address with id `{address_id}` not found",
        status_code=HTTP_404_NOT_FOUND,
    )


@router.post(
    "/addresses/", response_model=Response[AddressOut], status_code=HTTP_201_CREATED
)
def create_address(
    address: AddressCreate, session: Session = Depends(get_db)
) -> Response:
    """
    Create new address.
    """
    crud_obj = CrudBase(Address)
    if is_duplicate_lat_long(
        crud_obj=crud_obj,
        db=session,
        latitude=address.latitude,
        longitude=address.longitude,
    ):
        raise DuplicateException(
            message="address with same latitude and longitude already exist",
            status_code=HTTP_409_CONFLICT,
        )
    data = crud_obj.create(session=session, obj_to_create=address)
    return Response(data=data, message="The address was created successfully")


@router.put(
    "/addresses/{address_id}",
    response_model=Response[AddressOut],
    status_code=HTTP_200_OK,
)
def update_existing_address(
    address_id: int, updates: AddressUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing address with the provided updates.
    """
    crud_obj = CrudBase(Address)
    address = crud_obj.get(db, query_filter=Address.id == address_id)
    if not address:
        raise ObjectNotFoundException(
            message=f"address with id `{address_id}` not found",
            status_code=HTTP_404_NOT_FOUND,
        )
    if is_duplicate_lat_long(
        crud_obj=crud_obj,
        db=db,
        latitude=updates.latitude,
        longitude=updates.longitude,
        instance_id=address.id,
    ):
        raise DuplicateException(
            message="address with same latitude and longitude already exist",
            status_code=HTTP_409_CONFLICT,
        )
    updated_address = crud_obj.update(
        session=db, updated_obj=updates, db_obj_to_update=address
    )
    return Response(data=updated_address, message="address updated successfully")


@router.delete(
    "/addresses/{address_id}",
    response_model=Response[AddressOut],
    status_code=HTTP_200_OK,
)
def delete_existing_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address.
    """
    crud_obj = CrudBase(Address)
    address_obj = crud_obj.get(session=db, query_filter=Address.id == address_id)
    if address_obj:
        CrudBase(Address).delete(session=db, id_to_delete=address_id)
        return Response(message="Address deleted successfully")
    raise ObjectNotFoundException(
        message=f"address with id `{address_id}` not found",
        status_code=HTTP_404_NOT_FOUND,
    )
