
from libros.models import Libro
from libros.serializers import LibroSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

#importamos el modulo de gestion de permisos de DRF
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.pagination import LimitOffsetPagination


from libros.serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'libros': reverse('libros-list', request=request, format=format)
    })


#clase para manejar multiples instancias
class LibroList(APIView):

    #agregamos esta propiedad para que solo los usuarios autenticados puedan tocar
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #Crea un nuevo libro
    def post(self, request, format=None):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def get(self, request):
        libros = Libro.objects.all().order_by('created_at')
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(libros, request)
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LibroDetails(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get(self, request, pk):
        libro = Libro.objects.filter(pk=pk).first()
        serializer = LibroSerializer(libro)
        if libro:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        libro = Libro.objects.filter(pk=pk).first()
        if libro:
            libro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('error', status=status.HTTP_404_NOT_FOUND)



    def put(self, request, pk):
        libro = Libro.objects.filter(pk=pk).first()
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
