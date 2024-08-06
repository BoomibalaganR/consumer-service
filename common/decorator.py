from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def validatePayload(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.payload = serializer.validated_data
        return func(self, request, *args, **kwargs)
    return wrapper
