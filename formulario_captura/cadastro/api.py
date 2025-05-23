from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ConsultorSerializer
from rest_framework import status
from .models import Consultor

@api_view(['GET'])
def get_consultor_id_by_email(request):
        email = request.query_params.get('email', None)
        print(email)
        if not email:
            return Response({"error": "O parâmetro 'email' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            consultor = Consultor.objects.get(consultorEmail=email)
            print(consultor)
            serializer = ConsultorSerializer(consultor)
            return Response(serializer.data)
        except Consultor.DoesNotExist:
            return Response({"error": "Consultor não encontrado"}, status=status.HTTP_404_NOT_FOUND) 