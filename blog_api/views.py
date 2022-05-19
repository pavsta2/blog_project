from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from blog.models import Note
from blog_api import serializers


class NoteListCreateAPIView(APIView):
    def get(self, request: Request):
        notes = Note.objects.all()

        serializer = serializers.NoteSerializer(
            instance=notes,
            many=True
        )
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = serializers.NoteSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )


class NoteDetailAPIView(APIView):
    def get(self, request: Request, pk):
        note = get_object_or_404(Note, pk=pk)
        return Response([
            serializers.note_to_json(note)
        ])

    def put(self, request: Request, pk):
        data = request.data
        note = get_object_or_404(Note, pk=pk)
        note.title = data['title']
        note.message = data['message']
        note.save()
        return Response([
            serializers.note_created(note)
        ])


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(public=True)