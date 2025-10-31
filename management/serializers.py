from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Event, RSVP, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('user','full_name','bio','location','profile_picture')


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    invited_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True, required=False)
    class Meta:
        model = Event
        fields = ('id','title','description','organizer','location','start_time','end_time','is_public','invited_ids','created_at','updated_at')
        read_only_fields = ('organizer','created_at','updated_at')


    def create(self, validated_data):
        invited = validated_data.pop('invited_ids', [])
        user = self.context['request'].user
        event = Event.objects.create(organizer=user, **validated_data)
        if invited:
            event.invited.set(invited)
            return event


    def update(self, instance, validated_data):
        invited = validated_data.pop('invited_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            if invited is not None:
                instance.invited.set(invited)
                instance.save()
                return instance


class RSVPSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = RSVP
        fields = ('id','event','user','status','created_at')
        read_only_fields = ('user','created_at')


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        rsvp, created = RSVP.objects.update_or_create(event=validated_data['event'], user=user, defaults={'status': validated_data['status']})
        return rsvp

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id','event','user','rating','comment','created_at')
        read_only_fields = ('user','created_at')


    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value


def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    review, created = Review.objects.update_or_create(event=validated_data['event'], user=validated_data['user'], defaults={'rating': validated_data['rating'],'comment':validated_data.get('comment','')})
    return review