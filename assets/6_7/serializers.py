from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Advertisement, AdvertisementStatusChoices

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at',)
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # Валидация: не более 10 открытых объявлений у пользователя (только при создании)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Проверяем только при создании нового объявления (self.instance is None)
            if self.instance is None:
                open_count = Advertisement.objects.filter(
                    creator=request.user,
                    status=AdvertisementStatusChoices.OPEN
                ).count()
                if open_count >= 10:
                    raise serializers.ValidationError(
                        'У вас не может быть больше 10 открытых объявлений'
                    )

        return data
