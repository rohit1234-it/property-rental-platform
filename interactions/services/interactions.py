from django.db.models import Q
from django.db import transaction
from interactions.serializers.interactions import IntractionSerializer
from interactions.models.interactions import Interaction
from common.helpers.response import CustomResponse


class InteractionService:
    __slots__ = ['_request']

    cust_response = CustomResponse()
    interactions_serializer_class =IntractionSerializer

    def __init__(self, request):
        self._request = request

    @staticmethod
    def _is_int_like(value):
        if value is None:
            return False

        text = str(value).strip()
        return text.isdigit()

    def get_all_interactions(self):
        try:
            requested_owner_id = self._request.query_params.get('owner_id')

            if self._request.user.is_superuser:
                if requested_owner_id:
                    interactions = Interaction.objects.filter(
                        owner_id=requested_owner_id
                    )
                else:
                    interactions = Interaction.objects.all()

            else:
                interactions = Interaction.objects.filter(
                    owner=self._request.user
                )

            search_keyword = self._request.query_params.get('search')

            if search_keyword:
                interactions = interactions.filter(
                    Q(property_name__istartswith=search_keyword) |
                    Q(city__istartswith=search_keyword) |
                    Q(state__istartswith=search_keyword)
                )

            status_filter = self._request.query_params.get('status')

            if status_filter is not None:
                if status_filter.lower() == 'true':
                    interactions = interactions.filter(is_available=True)

                elif status_filter.lower() == 'false':
                    interactions = interactions.filter(is_available=False)

            city = self._request.query_params.get('city')

            if city:
                interactions=interactions.filter(
                    city__iexact=city
                )

            interactions = interactions.select_related('user',
    'property')

            return self.cust_response.paginated_response(
                queryset=interactions,
                serializer_class=self.interactions_serializer_class,
                request=self._request,
                message="Intractions retrieved successfully!"
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to retrieve interactions: {str(e)}",
                None,
                400
            )

    def retrieve_interactions(self, pk):
        try:
            interactions_obj = Interaction.objects.select_related(
                'user',
    'property'
            ).get(pk=pk)

            if (
                not self._request.user.is_superuser
                and interactions_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to view this interactions.",
                    None,
                    403
                )

            serializer = self.interactions_serializer_class(interactions_obj)

            return self.cust_response.success_response(
                serializer.data,
                "Intractions retrieved successfully!",
                200
            )

        except Interaction.DoesNotExist:
            return self.cust_response.error_response(
                "interactions does not exist.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to retrieve interactions: {str(e)}",
                None,
                400
            )

    def create_interactions(self):
        try:
            data = (
            self._request.data.copy()
            if hasattr(self._request.data, 'copy')
            else dict(self._request.data)
        )
            data['user'] = self._request.user.id

            serializer = self.interactions_serializer_class(data=data)
            

            if serializer.is_valid():

                with transaction.atomic():
                    interaction_obj = Interaction.objects.create(
                    **serializer.validated_data
                )
                    result_serializer = self.interactions_serializer_class(
                interaction_obj
            )
                    return self.cust_response.success_response(
                result_serializer.data,
                "Interaction created successfully!",
                201
            )
            return self.cust_response.error_response(
            "Failed to create interaction. Validation failed.",
            serializer.errors,
            400
        )

        except Exception as e:
            return self.cust_response.error_response(
            f"Failed to create interaction: {str(e)}",
            None,
            400
        )
    
    def update_interaction(self, pk, partial=False):
        try:
            interactions_obj= Interaction.objects.select_related(
                'user',
    'property'
            ).get(pk=pk)

            if (
                not self._request.user.is_superuser
                and interactions_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to modify this interaction.",
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

            serializer = self.interactions_serializer_class(
            interactions_obj,
                data=data,
                partial=partial
            )

            if serializer.is_valid():
                with transaction.atomic():
                    interactions_obj = serializer.save()

                result_serializer = self.interactions_serializer_class(
                    interactions_obj
                )

                return self.cust_response.success_response(
                    result_serializer.data,
                    "intreaction updated successfully!",
                    200
                )

            return self.cust_response.error_response(
                "Failed to update intraction2. Validation failed.",
                serializer.errors,
                400
            )

        except Interaction.DoesNotExist:
            return self.cust_response.error_response(
                "interaction does not exist.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to update interaction: {str(e)}",
                None,
                400
            )

    def delete_interactions(self, pk):
        try:
            interactions_obj = Interaction.objects.get(pk=pk)

            if (
                not self._request.user.is_superuser
                and interactions_obj.owner_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to delete this interaction.",
                    None,
                    403
                )

            interactions_obj.delete()

            return self.cust_response.success_response(
                None,
                "interaction  deleted successfully!",
                200
            )

        except Interaction.DoesNotExist:
            return self.cust_response.error_response(
                "interactionn not found.",
                None,
                404
            )

        except Exception as e:
            return self.cust_response.error_response(
                f"Failed to delete interaction: {str(e)}",
                None,
                400
            )