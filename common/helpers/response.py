from rest_framework.response import Response


class CustomResponse:

    def success_response(self, data, message="Request successful", status_code=200):
        return Response(
            {
                "status": "success",
                "code": status_code,
                "message": message,
                "data": data,
            },
            status=status_code,
        )

    def error_response(self, error_message, errors=None, status_code=400):
        return Response(
            {
                "status": "error",
                "code": status_code,
                "message": error_message,
                "errors": errors,
            },
            status=status_code,
        )

    def paginated_response(
        self,
        queryset=None,
        serializer_class=None,
        request=None,
        message="Properties retrieved successfully",
        status_code=200,
    ):
        from rest_framework.pagination import PageNumberPagination

        paginator = PageNumberPagination()
        paginator.page_size = 10

        page = paginator.paginate_queryset(
            queryset,
            request
        )

        serializer = serializer_class(
            page,
            many=True,
            context={"request": request}
        )

        return Response(
            {
                "status": "success",
                "code": status_code,
                "message": message,
                "data": serializer.data,
                "pagination": {
                    "count": paginator.page.paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                },
            },
            status=status_code,
        )