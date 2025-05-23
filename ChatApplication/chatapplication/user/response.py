from rest_framework.response import Response


class ResponseHandler:
    @staticmethod
    def success(message="", status_code=None, data=None):
        return Response({
            "success": True,
            "message": message,
            "status_code": status_code,
            "data": data
        }, status=status_code)

    @staticmethod
    def error(message="", status_code=None, details=None):
        return Response({
            "success": False,
            "message": message,
            "status_code": status_code,
            "details": details

        }, status=status_code)
