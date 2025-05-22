import logging
from datetime import timedelta

import requests
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from where_from.names.models import Country, Name, NameCountryProbability

from .serializers import NameResponseSerializer, PopularNameSerializer, UserCreateSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    summary='Get name nationality',
    description='Get the nationality probability for a given name',
    parameters=[
        OpenApiParameter(name='name', type=str, location='query', description='Name to analyze', required=True)
    ],
    responses=NameResponseSerializer,
)
@api_view(['GET'])
def name(request):
    name = request.GET.get('name', '')
    if not name:
        return Response({'error': 'Name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        name_obj = Name.objects.filter(name=name).first()
        one_day_ago = timezone.now() - timedelta(days=1)

        if name_obj and name_obj.last_accessed >= one_day_ago:
            name_obj.count_of_reguests += 1
            name_obj.save()

            probabilities = []
            for prob in NameCountryProbability.objects.filter(name_request=name_obj).select_related('country'):
                probabilities.append(
                    {
                        'country_code': prob.country.code,
                        'country_name': prob.country.name,
                        'probability': prob.probability,
                    }
                )

            return Response({'name': name, 'count': name_obj.count_of_reguests, 'countries': probabilities})

        nationalize_response = requests.get(f'https://api.nationalize.io/?name={name}', timeout=5)
        nationalize_response.raise_for_status()
        nationalize_data = nationalize_response.json()

        countries_data = nationalize_data.get('country', [])
        if not countries_data:
            return Response(
                {'message': f'No nationality data found for name: {name}'}, status=status.HTTP_404_NOT_FOUND
            )

        if name_obj:
            name_obj.count_of_reguests += 1
            name_obj.last_accessed = timezone.now()
            name_obj.save()
        else:
            name_obj = Name.objects.create(name=name, count_of_reguests=1, last_accessed=timezone.now())

        countries_data = nationalize_data.get('country', [])
        probabilities = []

        for country_data in countries_data:
            country_code = country_data['country_id']
            probability = country_data['probability']

            try:
                country = Country.objects.get(code=country_code)
            except Country.DoesNotExist:
                rest_countries_response = requests.get(
                    f'https://restcountries.com/v3.1/alpha/{country_code}', timeout=5
                )
                rest_countries_response.raise_for_status()
                rest_country_data = rest_countries_response.json()

                country_info = rest_country_data[0]
                country_data = {
                    'code': country_code,
                    'name': country_info['name']['common'],
                    'common_name': country_info['name'].get('common', ''),
                    'region': country_info.get('region', ''),
                    'independent': country_info.get('independent', True),
                    'google_maps': country_info.get('maps', {}).get('googleMaps', ''),
                    'open_street_maps': country_info.get('maps', {}).get('openStreetMaps', ''),
                    'capital': ', '.join(country_info.get('capital', [])),
                    'capital_coordinates': str(country_info.get('capitalInfo', {}).get('latlng', [])),
                    'flags': country_info.get('flags', {}).get('png', ''),
                    'flags_svg': country_info.get('flags', {}).get('svg', ''),
                    'flaf_alt': country_info.get('flags', {}).get('alt', ''),
                    'coat_of_arms_png': country_info.get('coatOfArms', {}).get('png', ''),
                    'coat_of_arms_svg': country_info.get('coatOfArms', {}).get('svg', ''),
                    'borders_with': ', '.join(country_info.get('borders', [])),
                }
                country = Country.objects.create(**country_data)

            prob_obj, prob_created = NameCountryProbability.objects.get_or_create(
                name_request=name_obj, country=country, defaults={'probability': probability}
            )

            if not prob_created:
                prob_obj.probability = probability
                prob_obj.save()

            probabilities.append(
                {'country_code': country.code, 'country_name': country.name, 'probability': probability}
            )

        response_data = {'name': name, 'count': nationalize_data.get('count'), 'countries': probabilities}
        return Response(response_data)

    except requests.RequestException as e:
        error_message = f'Failed to fetch data from external API: {str(e)}'
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary='Get popular names by country',
    description='Get the most popular names for a specific country',
    parameters=[
        OpenApiParameter(
            name='country',
            type=str,
            location='query',
            description='Two-letter country code (e.g., US, GB)',
            required=True,
        )
    ],
    responses=PopularNameSerializer(many=True),
)
@api_view(['GET'])
def popular_names(request):
    country_code = request.GET.get('country')
    if not country_code:
        return Response({'error': "The 'country' query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        country = Country.objects.get(code=country_code)
    except Country.DoesNotExist:
        return Response({'error': f"No country found with code '{country_code}'."}, status=status.HTTP_404_NOT_FOUND)

    top_names = (
        Name.objects.filter(namecountryprobability__country=country)
        .annotate(request_count=Count('id'))
        .order_by('-request_count')[:5]
    )

    if not top_names:
        return Response({'error': f"No data found for country '{country_code}'."}, status=status.HTTP_404_NOT_FOUND)

    result = [
        {
            'name': name.name,
            'count': name.count_of_reguests,
            'probability': name.namecountryprobability_set.get(country=country).probability,
        }
        for name in top_names
    ]

    return Response(result)


@extend_schema(
    summary='Create new user',
    description='Register a new user account',
    request=UserCreateSerializer,
    responses={201: UserCreateSerializer},
)
@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        user = serializer.save()
        return Response(UserCreateSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
