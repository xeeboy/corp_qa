from rest_framework import serializers
from . import models


class DwQuerySerializer(serializers.ModelSerializer):
    # ModelSerializer和Django中ModelForm功能相似
    # Serializer和Django中Form功能相似
    class Meta:
        model = models.UnPass
        # fields = '__all__'  # all field will show
        fields = ('id', 'up_type', 'customer', 'up_name', 'batch',
                  'pro_date', 'pro_qty', 'up_desc')
