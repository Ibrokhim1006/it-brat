from rest_framework import serializers

from authen.serializers import UserInformationSerializer
from resume.models import Heading, ResumeModel, FavoritesResume, NotificationResume


class HeadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Heading
        fields = ['id', 'name']


class ResumesSerializer(serializers.ModelSerializer):
    owner = UserInformationSerializer(read_only=True)
    heading = HeadingSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = ResumeModel
        fields = ['id', 'image', 'contact', 'experience', 'hard_skills', 'soft_skills', 'description', 'heading', 'owner', 'is_owner', 'favorite', 'create_at']

    def get_is_owner(self, obj):
        request = self.context.get('request').user
        return obj.owner == request
    
    def get_favorite(self, obj):
        request_user = self.context['request'].user
        user_favorites = FavoritesResume.objects.filter(owner=request_user, resume=obj)
        return user_favorites.exists()


class ResumeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    hard_skills = serializers.ListField(child=serializers.CharField(), write_only=True)
    soft_skills = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = ResumeModel
        fields = ['id', 'image', 'contact', 'experience', 'hard_skills', 'soft_skills', 'description', 'heading', 'owner', 'create_at']


    def create(self, validated_data):
        hard_skills = validated_data.pop('hard_skills', [])
        soft_skills = validated_data.pop('soft_skills', [])

        resume = ResumeModel.objects.create(**validated_data)

        resume.owner = self.context.get('owner')
        resume.hard_skills = hard_skills
        resume.soft_skills = soft_skills
        resume.save()
        return resume
    
    def update(self, instance, validated_data):
        hard_skills = validated_data.pop('hard_skills', [])
        soft_skills = validated_data.pop('soft_skills', [])

        instance.contact = validated_data.get('contact', instance.contact)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.description = validated_data.get('description', instance.description)
        instance.heading = validated_data.get('heading', instance.heading)

        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)

        instance.hard_skills = hard_skills
        instance.soft_skills = soft_skills
        instance.save()
        return instance


class FavroitesResumeSerializer(serializers.ModelSerializer):
    resume = ResumesSerializer(read_only=True)
    owner = UserInformationSerializer(read_only=True)

    class Meta:
        model = FavoritesResume
        fields = ['id', 'resume', 'owner', 'create_at']


class FavroiteResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoritesResume
        fields = ['id', 'resume', 'owner', 'create_at']

    def create(self, validated_data):
        favourite = FavoritesResume.objects.create(**validated_data)
        favourite.owner = self.context.get('owner')
        favourite.save()
        return favourite


class NotificationResumeSerializer(serializers.ModelSerializer):
    favorite = FavroitesResumeSerializer(read_only=True)

    class Meta:
        model = NotificationResume
        fields = ['id', 'favorite', 'is_read']