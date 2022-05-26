from datetime import datetime

from rest_framework import serializers
from blog.models import Note, Comment


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("author",)


def note_to_json(note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "message": note.message,
        "public": note.public
    }


def note_created(note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "message": note.message,
        "public": note.public,
        "create_at": note.create_at,
        "update_at": note.update_at,
    }

class CommentSerializer(serializers.ModelSerializer):
    # todo serializers.SerializerMethodField
    # rating = serializers.SerializerMethodField('get_rating')
    #
    # def get_rating(self, obj):
    #     return {
    #         'value': obj.rating,
    #         'display': obj.get_rating_display()
    #     }

    class Meta:
        model = Comment
        fields = "__all__"


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Одна статья блога """
    authors = serializers.SlugRelatedField(
        many=True,
        slug_field="username",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
    )
    comment_set = CommentSerializer(many=True, read_only=True)  # one-to-many-relationships

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'create_at', 'update_at',  # из модели
            'authors', 'comment_set',   # из сериализатора
        )

    # def to_representation(self, instance):
    #     """ Переопределение вывода. Меняем формат даты в ответе """
    #     ret = super().to_representation(instance)
    #     # Конвертируем строку в дату по формату
    #     create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%f')
    #     # Конвертируем дату в строку в новом формате
    #     ret['create_at'] = create_at.strftime('%d %B %Y %H:%M:%S')
    #     return ret
