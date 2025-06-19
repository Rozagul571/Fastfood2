from rest_framework_gis.serializers import GeoFeatureModelSerializer
from restaurants.models import Restaurant

class RestaurantSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Restaurant
        geo_field = "location"
        fields = ("id", "name", "description", "location")



    # def to_representation(self, instance):
    #      data = super(RestaurantSerializer, self).to_representation(instance)
