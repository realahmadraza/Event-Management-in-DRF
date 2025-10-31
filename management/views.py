from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly, IsInvitedOrPublic


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().select_related('organizer').prefetch_related('invited')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsInvitedOrPublic, IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['organizer__username','location','is_public']
    search_fields = ['title','location','description','organizer__username']


    def get_queryset(self):
        # list only public events or invited if private for unauthenticated users
        qs = super().get_queryset()
        user = self.request.user
        if self.action == 'list':
            if user.is_authenticated:
                # authenticated: show public + private where invited or organizer
                return qs.filter(models.Q(is_public=True) | models.Q(organizer=user) | models.Q(invited=user)).distinct()
            return qs.filter(is_public=True)
        return qs


    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def rsvp(self, request, pk=None):
        event = self.get_object()
        serializer = RSVPSerializer(data={'event': event.id, 'status': request.data.get('status')}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        rsvp = serializer.save()
        return Response(RSVPSerializer(rsvp).data)


    @action(detail=True, methods=['get','post'], url_path='reviews', permission_classes=[IsAuthenticatedOrReadOnly])
    def reviews(self, request, pk=None):
        event = self.get_object()
        if request.method == 'GET':
            qs = event.reviews.all()
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = ReviewSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = ReviewSerializer(qs, many=True)
        return Response(serializer.data)


        # POST
        serializer = ReviewSerializer(data={'event': event.id, 'rating': request.data.get('rating'), 'comment': request.data.get('comment','')}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class RSVPViewSet(viewsets.GenericViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer


    @action(detail=False, methods=['patch'], url_path='(?P<event_pk>[^/.]+)/(?P<user_pk>[^/.]+)')
    def update_status(self, request, event_pk=None, user_pk=None):
        rsvp = get_object_or_404(RSVP, event_id=event_pk, user_id=user_pk)
        if request.user != rsvp.user and request.user != rsvp.event.organizer:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        rsvp.status = request.data.get('status', rsvp.status)
        rsvp.save()
        return Response(RSVPSerializer(rsvp).data)