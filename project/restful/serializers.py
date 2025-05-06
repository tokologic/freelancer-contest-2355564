from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator


class RegisterAuthSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")
        ]
    )
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirmation"]
        extra_kwargs = {
            "username": {"required": False},
            "email": {"required": True},
            "password": {"write_only": True},
            "password_confirmation": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": ["The password does not match."]}
            )

        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return data

    def create(self, validated_data):
        import random
        import string

        from django.contrib.auth.hashers import make_password

        validated_data.pop("password_confirmation")

        if "username" in validated_data:
            username = validated_data["username"]
        else:
            salt = "".join(random.choices(string.ascii_lowercase, k=10))
            splits = validated_data["email"].split("@")
            username = splits[0] + "-" + salt

        user = User.objects.create(
            username=username,
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
        )
        return user


class LoginAuthSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        return value

    def create(self, validated_data):
        from rest_framework_simplejwt.tokens import RefreshToken

        user = User.objects.filter(email=validated_data["email"]).last()
        is_matched = user.check_password(validated_data["password"])
        if not is_matched:
            raise exceptions.AuthenticationFailed("Password not match")

        refresh = RefreshToken.for_user(user)

        self._jwt_refresh = refresh

        return user

    def to_representation(self, instance):
        return {"access_token": str(self._jwt_refresh.access_token)}


class PaginationWrapper(serializers.BaseSerializer):
    def __init__(self, serializer_class, pagination_class, **kwargs):
        self.serializer_class = serializer_class
        self.pagination_class = pagination_class
        super().__init__(**kwargs)


class LinkSerializer(serializers.Serializer):
    self = serializers.URLField()
    related = serializers.DictField(required=False)


class LinkSerializerObject:
    def __init__(self, values):
        for key in values:
            setattr(self, key, values[key])
