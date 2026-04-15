from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Contact

@api_view(['POST'])
def contact_api(request):
    name = request.data.get("name")
    email = request.data.get("email")
    subject = request.data.get("subject")
    message = request.data.get("message")

    if not name or not email or not message:
        return Response({"error": "Missing fields"}, status=400)

    # ✅ SAVE TO DATABASE
    Contact.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message
    )

    return Response({"message": "Message saved successfully"})