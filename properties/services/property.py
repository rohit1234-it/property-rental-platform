from django.db.models import Q
from django.db import transaction

from properties.serializers.property import PropertySerializer
from properties.models.property import Property
from common.helpers.response import CustomResponse


class PropertyService:
    __slots__ = ['_request']

    cust_response = CustomResponse()
    project_serializer_class = PropertySerializer

    def __init__(self, request):
        self._request = request

    @staticmethod
    def _is_int_like(value):
        if value is None:
            return False

        text = str(value).strip()
        return text.isdigit()

    def get_all_properties(self):
        try:
            requested_owner_id = self._request.query_params.get('owner_id')

            if self._request.user.is_superuser:
                if requested_owner_id:
                    properties = Property.objects.filter(
                        owner_id=requested_owner_id
                    )
                else:
                    properties = Property.objects.all()

            else:
                properties = Property.objects.filter(
                    owner=self._request.user
                )

            search_keyword = self._request.query_params.get('search')

            if search_keyword:
                properties = properties.filter(
                    Q(property_name__istartswith=search_keyword) |
                    Q(city__istartswith=search_keyword) |
                    Q(state__istartswith=search_keyword)
                )

            status_filter = self._request.query_params.get('status')

            if status_filter is not None:
                if status_filter.lower() == 'true':
                    properties = properties.filter(is_available=True)

                elif status_filter.lower() == 'false':
                    properties = properties.filter(is_available=False)

            city = self._request.query_params.get('city')

            if city:
                properties = properties.filter(
                    city__iexact=city
                )

            properties = properties.select_related('owner')

            return self.cust_response.paginated_response(
                queryset=properties,
                serializer_class=self.project_serializer_class,
                request=self._request,
                message="Properties retrieved successfully!"
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to retrieve properties: {str(e)}",
                None,
                400
            )

    def retrieve_property(self, pk):
        try:
            property_obj = Property.objects.select_related(
                'owner'
            ).get(pk=pk)

            if (
                not self._request.user.is_superuser
                and property_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to view this property.",
                    None,
                    403
                )

            serializer = self.project_serializer_class(property_obj)

            return self.cust_response.success_response(
                serializer.data,
                "Property retrieved successfully!",
                200
            )

        except Property.DoesNotExist:
            return self.cust_response.error_response(
                "Property does not exist.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to retrieve property: {str(e)}",
                None,
                400
            )

    def create_property(self):
        try:
            data = (
            self._request.data.copy()
            if hasattr(self._request.data, 'copy')
            else dict(self._request.data)
        )
            data['owner'] = self._request.user.id
            serializer = self.project_serializer_class(data=data)
            if serializer.is_valid():
                with transaction.atomic():
                    property_obj = Property.objects.create(
                    **serializer.validated_data
                )
                    result_serializer = self.project_serializer_class(
                property_obj
            )
                    return self.cust_response.success_response(
                result_serializer.data,
                "Property created successfully!",
                201)
                return self.cust_response.error_response(
            "Failed to create property. Validation failed.",
            serializer.errors,
            400)
        except Exception as e:
            return self.cust_response.error_response(
            f"Failed to create property: {str(e)}",
            None,
            400
        )
    def update_property(self, pk, partial=False):
        try:
            property_obj = Property.objects.select_related(
                'owner'
            ).get(pk=pk)

            if (
                not self._request.user.is_superuser
                and property_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to modify this property.",
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

            serializer = self.project_serializer_class(
                property_obj,
                data=data,
                partial=partial
            )

            if serializer.is_valid():
                with transaction.atomic():
                    property_obj = serializer.save()

                result_serializer = self.project_serializer_class(
                    property_obj
                )

                return self.cust_response.success_response(
                    result_serializer.data,
                    "Property updated successfully!",
                    200
                )

            return self.cust_response.error_response(
                "Failed to update property. Validation failed.",
                serializer.errors,
                400
            )

        except Property.DoesNotExist:
            return self.cust_response.error_response(
                "Property does not exist.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to update property: {str(e)}",
                None,
                400
            )

    def delete_property(self, pk):
        try:
            property_obj = Property.objects.get(pk=pk)

            if (
                not self._request.user.is_superuser
                and property_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to delete this property.",
                    None,
                    403
                )

            property_obj.delete()

            return self.cust_response.success_response(
                None,
                "Property deleted successfully!",
                200
            )

        except Property.DoesNotExist:
            return self.cust_response.error_response(
                "Property not found.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to delete property: {str(e)}",
                None,
                400
            )