from rest_framework import serializers
from uzbektube.models import Category, VideoContent, Comment

# Класс Сериализации для Категорий
# class CategoryListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'title')

# Создание своего Сериалайзера
class CategoriesSerializer(serializers.Serializer):
    title = serializers.CharField()

    # Метод Что бы Сериалайзер умел создавть и получать Пост запрос
    def create(self, validated_data):
        return Category.objects.create(**validated_data)



class ContentListSerializer(serializers.Serializer):
    title = serializers.CharField()
    image = serializers.ImageField()
    author = serializers.CharField()
    category_id = serializers.IntegerField()
    category = serializers.SlugRelatedField('title', read_only=True)
    count_views = serializers.IntegerField()

# Сериалайзер что бы видеть все комментарии (сериализовать для просмотра)
class CommentListSerializer(serializers.Serializer):
    text = serializers.CharField()
    user_id = serializers.IntegerField()
    user = serializers.SlugRelatedField('username', read_only=True)
    created_at = serializers.DateTimeField()


class ContentDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    image = serializers.ImageField()
    video = serializers.FileField()
    author = serializers.CharField()
    category_id = serializers.IntegerField()
    category = serializers.SlugRelatedField('title', read_only=True)
    count_views = serializers.IntegerField()
    created_ad = serializers.DateTimeField()
    comments = CommentListSerializer(many=True)


class CommentCreateSerializer(serializers.Serializer):
    text = serializers.CharField()
    user_id = serializers.IntegerField()
    content_id = serializers.IntegerField()

    def create(self, validated_data):  # validated_data аргумент в который будим получать словарь на созданеи коммента
        print(validated_data, '+++++++++++++++++++++++++++')
        return Comment.objects.create(**validated_data)