from django.db.models import Q
from django.db import transaction

from rentals.serializers.rentals import RentalSerializer
from rentals.models.rental import Rental
from common.helpers.response import CustomResponse


class RentalService:
    __slots__ = ['_request']

    cust_response = CustomResponse()
    rental_serializer_class =RentalSerializer

    def __init__(self, request):
        self._request = request

    @staticmethod
    def _is_int_like(value):
        if value is None:
            return False

        text = str(value).strip()
        return text.isdigit()

    def get_all_rents(self):
        try:
            requested_owner_id = self._request.query_params.get('owner_id')

            if self._request.user.is_superuser:
                if requested_owner_id:
                    rentals = Rental.objects.filter(
                        owner_id=requested_owner_id
                    )
                else:
                    rentals = Rental.objects.all()

            else:
                rentals = Rental.objects.filter(
                    owner=self._request.user
                )

            search_keyword = self._request.query_params.get('search')

            if search_keyword:
                rentals = rentals.filter(
                    Q(property_name__istartswith=search_keyword) |
                    Q(city__istartswith=search_keyword) |
                    Q(state__istartswith=search_keyword)
                )

            status_filter = self._request.query_params.get('status')

            if status_filter is not None:
                if status_filter.lower() == 'true':
                    rentals = rentals.filter(is_available=True)

                elif status_filter.lower() == 'false':
                    rentals = rentals.filter(is_available=False)

            city = self._request.query_params.get('city')

            if city:
                rentals =rentals.filter(
                    city__iexact=city
                )

            rentals = rentals.select_related('owner')

            return self.cust_response.paginated_response(
                queryset=rentals,
                serializer_class=self.rental_serializer_class,
                request=self._request,
                message="Rentals retrieved successfully!"
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to retrieve rentals: {str(e)}",
                None,
                400
            )

    def retrieve_rentals(self, pk):
        try:
            Rental_obj = Rental.objects.select_related(
                'owner'
            ).get(pk=pk)

            if (
                not self._request.user.is_superuser
                and Rental_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to view this rentals.",
                    None,
                    403
                )

            serializer = self.rental_serializer_class(Rental_obj)

            return self.cust_response.success_response(
                serializer.data,
                "Rentals retrieved successfully!",
                200
            )

        except Rental.DoesNotExist:
            return self.cust_response.error_response(
                "Rentals does not exist.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to retrieve rentals: {str(e)}",
                None,
                400
            )

    def create_rentals(self):
        try:
            data = (
            self._request.data.copy()
            if hasattr(self._request.data, "copy")
            else dict(self._request.data)
        )
            serializer = self.rental_serializer_class(data=data)

            if serializer.is_valid():
                with transaction.atomic():
                    rental_obj = Rental.objects.create(
                    owner=self._request.user,
                    **serializer.validated_data
                )
                    result_serializer = self.rental_serializer_class(
                        rental_obj
            )
                    return self.cust_response.success_response(
                result_serializer.data,
                "Rental created successfully!",
                201
            )
                return self.cust_response.error_response(
            "Failed to create rental. Validation failed.",
            serializer.errors,
            400
        )
        except Exception as e:
            return self.cust_response.error_response(
            f"Failed to create rental: {str(e)}",
            None,
            400
        )
    
    def update_rentals(self, pk, partial=False):
        try:
            rental_obj = Rental.objects.select_related(
                'owner'
            ).get(pk=pk)

            if (
                not self._request.user.is_superuser
                and rental_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to modify this rental.",
                    None,
                    403
                )

            data = (
                self._request.data.copy()
                if hasattr(self._request.data, 'copy')
                else dict(self._request.data)
            )

            # Normal user cannot change the owner
            if not self._request.user.is_superuser:
                data.pop('owner', None)

            serializer = self.rental_serializer_class(
            rental_obj,
                data=data,
                partial=partial
            )

            if serializer.is_valid():
                with transaction.atomic():
                    rental_obj = serializer.save()

                result_serializer = self.rental_serializer_class(
                    rental_obj
                )

                return self.cust_response.success_response(
                    result_serializer.data,
                    "rental updated successfully!",
                    200
                )

            return self.cust_response.error_response(
                "Failed to update rental. Validation failed.",
                serializer.errors,
                400
            )

        except Rental.DoesNotExist:
            return self.cust_response.error_response(
                "rental does not exist.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to update rental: {str(e)}",
                None,
                400
            )

    def delete_rental(self, pk):
        try:
            rental_obj = Rental.objects.get(pk=pk)

            if (
                not self._request.user.is_superuser
                and rental_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to delete this rental.",
                    None,
                    403
                )

            rental_obj.delete()

            return self.cust_response.success_response(
                None,
                "rentals deleted successfully!",
                200
            )

        except Rental.DoesNotExist:
            return self.cust_response.error_response(
                "rental not found.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to delete rental: {str(e)}",
                None,
                400
            )