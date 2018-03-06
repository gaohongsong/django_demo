# -*- coding: utf-8 -*-
"""
    FBV - function based view
    在DRF中使用函数式视图的样例
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '20/day'


# api_view will will pass Request to view func and receive Response
@api_view(['GET', 'POST'])
# change api policies
@throttle_classes([OncePerDayUserThrottle])
@permission_classes((AllowAny,))
# support request specified format such as http://localhost:8000/snippets.json
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # return JsonResponse(serializer.data, safe=False)
        # return Response(serializer.data, content_type="application/json")
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # replace JsonResponse with Response
            # return JsonResponse(serializer.data, status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((AllowAny,))
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
