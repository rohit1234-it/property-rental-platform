from rest_framework.response import Response


class CustomResponse:

    def success_response(self, data, message="Request successful", status_code=200):
        response = {
            "status": "success",
            "code": status_code,
            "message": message,
            "data": data,
        }

        return Response(response, status=status_code)


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

