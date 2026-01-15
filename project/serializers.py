from rest_framework import serializers
from project.models import CategoriyaProject, Project, FavoritesProject, Notification
from authen.serializers import UserInformationSerializer


class CategoryProjectSerializer(serializers.ModelSerializer):
    ''' Project Category '''
    class Meta:
        model = CategoriyaProject
        fields = ['id', 'name', 'logo']


class ProjectsSerializer(serializers.ModelSerializer):
    ''' Projects Serializer '''
    category = CategoryProjectSerializer(read_only=True)
    owner = UserInformationSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()
    valuta = serializers.CharField(source='get_valuta_display')
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'contact', 'valuta', 'price', 'skils', 'description', 'image', 'category', 'is_owner', 'favorite', 'owner', 'create_at']

    def get_is_owner(self, obj):
        request = self.context.get('request', None)  # Request mavjudligini tekshirish
        if request and hasattr(request, 'user'):
            return obj.owner == request.user
        return False
    
    def get_favorite(self, obj):
        user = self.context.get("owner")
        user_favorities = FavoritesProject.objects.filter(owner=user)
        if user_favorities.filter(project__id=obj.id).exists():
            return True
        return False


class ProjectSerializer(serializers.ModelSerializer):
    ''' Project CRUD Serializer '''
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    skils = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'contact', 'valuta', 'price', 'skils', 'description', 'image', 'category', 'owner', 'create_at']

    def create(self, validated_data):
        skils_data = validated_data.pop('skils', [])

        project = Project.objects.create(**validated_data)
        project.owner = self.context.get('owner')
        project.skils = skils_data
        project.save()
        return project
    
    def update(self, instance, validated_data):
        skils_data = validated_data.pop('skils', [])

        instance.name = validated_data.get('name', instance.name)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.valuta = validated_data.get('valuta', instance.valuta)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)

        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)

        instance.skils = skils_data
        instance.save()
        return instance
    

class FavoritesProjectSerializer(serializers.ModelSerializer):
    ''' Favorite Project Serializer '''
    project = ProjectsSerializer(read_only=True)
    owner = UserInformationSerializer(read_only=True)

    class Meta:
        model = FavoritesProject
        fields = ['id', 'project', 'owner', 'create_at']


class FavoriteProjectSerializer(serializers.ModelSerializer):
    ''' Favorite Projecr CRUD Serializer '''
    class Meta:
        model = FavoritesProject
        fields = ['id', 'project', 'owner', 'create_at']

    def create(self, validated_data):
        favourite = FavoritesProject.objects.create(**validated_data)
        favourite.owner = self.context.get('owner')
        favourite.save()
        return favourite


class NotificationSerializer(serializers.ModelSerializer):
    favorite = FavoritesProjectSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'favorite', 'is_read']
