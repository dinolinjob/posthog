from typing import Type

from rest_framework import mixins, response, serializers, status, viewsets

from posthog.models import PersonalAPIKey


class PersonalAPIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalAPIKey
        fields = ["id", "label", "created_at", "last_used_at"]
        read_only_fields = ["id", "created_at", "last_used_at", "team_id", "user_id"]


class PersonalAPIKeySerializerCreateOnly(PersonalAPIKeySerializer):
    class Meta:
        model = PersonalAPIKey
        fields = ["id", "label", "value", "created_at", "last_used_at"]
        read_only_fields = ["id", "value", "created_at", "last_used_at", "team_id", "user_id"]

    def create(self, validated_data: dict) -> PersonalAPIKey:
        user = self.context["request"].user
        personal_api_key = PersonalAPIKey.objects.create(user=user, team=user.team_set.get(), **validated_data)
        return personal_api_key


class PersonalAPIKeyViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = PersonalAPIKeySerializer
    queryset = PersonalAPIKey.objects.all()
    lookup_field = "id"

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        serializer_class = self.serializer_class
        if self.request.method == "POST":
            serializer_class = PersonalAPIKeySerializerCreateOnly
        return serializer_class