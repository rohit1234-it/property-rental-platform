from django.db.models import Q
from django.db import transaction

from interactions.serializers.interactions import IntractionSerializer
from interactions.models.interactions import Interaction
from common.helpers.response import CustomResponse


class InteractionService:

    __slots__ = ['_request']

    cust_response = CustomResponse()
    interactions_serializer_class = IntractionSerializer

    def __init__(self, request):
        self._request = request

    # =========================
    # GET ALL INTERACTIONS
    # =========================

    def get_all_interactions(self):
        try:

            if self._request.user.is_superuser:

                interactions = Interaction.objects.all()

            else:

                interactions = Interaction.objects.filter(
                    user=self._request.user
                )

            # Search
            search_keyword = self._request.query_params.get('search')

            if search_keyword:
                interactions = interactions.filter(
                    Q(message__icontains=search_keyword) |
                    Q(interaction_type__icontains=search_keyword)
                )

            # Status filter
            status_filter = self._request.query_params.get('status')

            if status_filter:
                interactions = interactions.filter(
                    status__iexact=status_filter
                )

            # Interaction type filter
            interaction_type = self._request.query_params.get(
                'interaction_type'
            )

            if interaction_type:
                interactions = interactions.filter(
                    interaction_type__iexact=interaction_type
                )

            interactions = interactions.select_related(
                'user',
                'property'
            )

            return self.cust_response.paginated_response(
                queryset=interactions,
                serializer_class=self.interactions_serializer_class,
                request=self._request,
                message="Interactions retrieved successfully!"
            )

        except Exception as e:

            return self.cust_response.error_response(
                f"Failed to retrieve interactions: {str(e)}",
                None,
                400
            )

    # =========================
    # GET SINGLE INTERACTION
    # =========================

    def retrieve_interactions(self, pk):
        try:

            interaction_obj = Interaction.objects.select_related(
                'user',
                'property'
            ).get(pk=pk)

            # Normal user can see only own interactions
            if (
                not self._request.user.is_superuser
                and interaction_obj.user_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to view this interaction.",
                    None,
                    403
                )

            serializer = self.interactions_serializer_class(
                interaction_obj
            )

            return self.cust_response.success_response(
                serializer.data,
                "Interaction retrieved successfully!",
                200
            )

        except Interaction.DoesNotExist:

            return self.cust_response.error_response(
                "Interaction does not exist.",
                None,
                404
            )

        except Exception as e:

            return self.cust_response.error_response(
                f"Failed to retrieve interaction: {str(e)}",
                None,
                400
            )

    # =========================
    # CREATE INTERACTION
    # =========================

    def create_interactions(self):
        try:

            data = (
                self._request.data.copy()
                if hasattr(self._request.data, 'copy')
                else dict(self._request.data)
            )

            # User comes from JWT
            data.pop('user', None)

            serializer = self.interactions_serializer_class(
                data=data
            )

            if serializer.is_valid():

                with transaction.atomic():

                    interaction_obj = Interaction.objects.create(
                        user=self._request.user,
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

    # =========================
    # UPDATE INTERACTION
    # =========================

    def update_interaction(self, pk, partial=False):
        try:

            interaction_obj = Interaction.objects.select_related(
                'user',
                'property'
            ).get(pk=pk)

            # Normal user can update only own interaction
            if (
                not self._request.user.is_superuser
                and interaction_obj.user_id != self._request.user.id
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

            # User must not be changed from frontend
            data.pop('user', None)

            serializer = self.interactions_serializer_class(
                interaction_obj,
                data=data,
                partial=partial
            )

            if serializer.is_valid():

                with transaction.atomic():

                    interaction_obj = serializer.save()

                result_serializer = self.interactions_serializer_class(
                    interaction_obj
                )

                return self.cust_response.success_response(
                    result_serializer.data,
                    "Interaction updated successfully!",
                    200
                )

            return self.cust_response.error_response(
                "Failed to update interaction. Validation failed.",
                serializer.errors,
                400
            )

        except Interaction.DoesNotExist:

            return self.cust_response.error_response(
                "Interaction does not exist.",
                None,
                404
            )

        except Exception as e:

            return self.cust_response.error_response(
                f"Failed to update interaction: {str(e)}",
                None,
                400
            )

    # =========================
    # DELETE INTERACTION
    # =========================

    def delete_interactions(self, pk):
        try:

            interaction_obj = Interaction.objects.get(pk=pk)

            # Normal user can delete only own interaction
            if (
                not self._request.user.is_superuser
                and interaction_obj.user_id != self._request.user.id
            ):
                return self.cust_response.error_response(
                    "You do not have permission to delete this interaction.",
                    None,
                    403
                )

            interaction_obj.delete()

            return self.cust_response.success_response(
                None,
                "Interaction deleted successfully!",
                200
            )

        except Interaction.DoesNotExist:

            return self.cust_response.error_response(
                "Interaction not found.",
                None,
                404
            )

        except Exception as e:

            return self.cust_response.error_response(
                f"Failed to delete interaction: {str(e)}",
                None,
                400
            )