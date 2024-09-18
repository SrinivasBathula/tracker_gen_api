from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid
import re
from datetime import datetime


# Create your views here.
class NextTrackingNumberView(APIView):
    @swagger_auto_schema(
        methods=["get"],
        manual_parameters=[
            openapi.Parameter(
                name="origin_country_id",
                in_=openapi.IN_QUERY,
                description="Origin country code (ISO 3166-1 alpha-2)",
                type=openapi.TYPE_STRING,
                required=True,
                example="MY",
            ),
            openapi.Parameter(
                name="destination_country_id",
                in_=openapi.IN_QUERY,
                description="Destination country code (ISO 3166-1 alpha-2)",
                type=openapi.TYPE_STRING,
                required=True,
                example="ID",
            ),
            openapi.Parameter(
                name="weight",
                in_=openapi.IN_QUERY,
                description="Order weight in kilograms (up to 3 decimal places)",
                type=openapi.TYPE_NUMBER,
                required=True,
                example=1.234,
            ),
            openapi.Parameter(
                name="customer_id",
                in_=openapi.IN_QUERY,
                description="Customer UUID",
                type=openapi.TYPE_STRING,
                required=True,
                example="de619854-b59b-425e-9db4-943979e1bd49",
            ),
            openapi.Parameter(
                name="customer_name",
                in_=openapi.IN_QUERY,
                description="Customer name",
                type=openapi.TYPE_STRING,
                required=True,
                example="RedBox Logistics",
            ),
            openapi.Parameter(
                name="customer_slug",
                in_=openapi.IN_QUERY,
                description="Customer slug (kebab-case)",
                type=openapi.TYPE_STRING,
                required=True,
                example="redbox-logistics",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Tracking number generated",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "tracking_number": openapi.Schema(type=openapi.TYPE_STRING),
                        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(description="Invalid request"),
        },
    )
    @action(methods=["get"], detail=False)
    def get(self, request):
        origin_country_id = request.GET.get("origin_country_id")
        destination_country_id = request.GET.get("destination_country_id")
        weight = request.GET.get("weight")
        # created_at = request.GET.get("created_at")
        customer_id = request.GET.get("customer_id")
        customer_name = request.GET.get("customer_name")
        customer_slug = request.GET.get("customer_slug")

        # Validate query parameters
        if not all(
            [
                origin_country_id,
                destination_country_id,
                weight,
                # created_at,
                customer_id,
                customer_name,
                customer_slug,
            ]
        ):
            return Response({"error": "Invalid request"}, status=400)

        # Generate tracking number
        tracking_number = self.generate_tracking_number()

        return Response(
            {
                "tracking_number": tracking_number,
                "created_at": datetime.now().isoformat(),
            },
            status=200,
        )

    def generate_tracking_number(self):
        while True:
            tracking_number = uuid.uuid4().hex.upper()[:16]
            if (
                re.match("^[A-Z0-9]{1,16}$", tracking_number)
                # and not TrackingNumber.objects.filter(
                #     tracking_number=tracking_number
                # ).exists()
            ):
                return tracking_number
