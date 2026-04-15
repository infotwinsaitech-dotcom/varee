from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile

# GET PROFILE
@api_view(['GET'])
def get_profile(request):
    profile = Profile.objects.first()

    if not profile:
        return Response({
            "name": "",
            "email": "",
            "phone": ""
        })

    return Response({
        "name": profile.name,
        "email": profile.email,
        "phone": profile.phone
    })


# UPDATE PROFILE
@api_view(['POST'])
def update_profile(request):
    data = request.data

    profile = Profile.objects.first()

    if not profile:
        profile = Profile.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone")
        )
    else:
        profile.name = data.get("name")
        profile.email = data.get("email")
        profile.phone = data.get("phone")
        profile.save()

    return Response({"message": "saved"})