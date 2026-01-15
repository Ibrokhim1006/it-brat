from rest_framework import serializers

from authen.models import CustomUser
from authen.serializers import UserInformationSerializer

from chat.models import Conversation, ChatMessage, Faq, NotificationChat


class MessagesSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    # sender_type = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', "sender", 'text', 'info', 'conversation_id', 'timestamp']

    def create(self, validated_data):
        sender = self.context.get('request')
        conversation = self.context.get('conversation')

        create_message = ChatMessage.objects.create(**validated_data)
        create_message.sender = sender
        create_message.conversation_id = conversation
        NotificationChat.objects.create(favorite=create_message)
        create_message.save()
        return create_message

    def get_sender_type(self, obj):
        user = self.context.get('request')
        sender = obj.sender
        if sender:
            return 'ini' 
        else:
            return 'res'

    

class ConversationListSerializer(serializers.ModelSerializer):
    sender_type = serializers.SerializerMethodField()
    initiator = UserInformationSerializer(read_only=True)
    receiver = UserInformationSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'sender_type']

    def get_sender_type(self, obj):
        user = self.context['request'].user  # Correctly access the user
        if user:
            if obj.initiator == user:
                return UserInformationSerializer(obj.receiver).data
            elif obj.receiver == user:
                return UserInformationSerializer(obj.initiator).data
        return 'initiator'

    

class MessageListSerializer(serializers.ModelSerializer):
    sender_type = serializers.SerializerMethodField()
    sender = UserInformationSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'text', 'info', 'timestamp', 'sender_type']
    
    def get_sender_type(self, obj):
        user = self.context['request']
        user = self.context['request'].user
        conversation = obj.conversation
        if user.id == obj.sender_id:
            if user.id == conversation.initiator_id:
                return 'initiator'
            elif user.id == conversation.receiver_id:
                return 'initiator'
        return 'resiver'


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageListSerializer(many=True, read_only=True)
    sender_type = serializers.SerializerMethodField()
    initiator = UserInformationSerializer(read_only=True)
    receiver = UserInformationSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'messages', 'sender_type']
    
    def get_sender_type(self, obj):
        user = self.context['request'].user  # Correctly access the user
        if user:
            if obj.initiator == user:
                return UserInformationSerializer(obj.receiver).data
            elif obj.receiver == user:
                return UserInformationSerializer(obj.initiator).data
        return 'initiator'
    
class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = ['id', 'title', 'description'] 


class ConversationsSerializer(serializers.ModelSerializer):
    sender_type = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'sender_type']

    def get_sender_type(self, obj):
        user = self.context['request'].user  # Correctly access the user
        if user:
            if obj.initiator == user:
                return UserInformationSerializer(obj.receiver).data
            elif obj.receiver == user:
                return UserInformationSerializer(obj.initiator).data
        return 'initiator'

class MessageListNotiSerializer(serializers.ModelSerializer):
    sender_type = serializers.SerializerMethodField()
    sender = UserInformationSerializer(read_only=True)
    conversation = ConversationsSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'text', 'info', 'timestamp', 'sender_type', 'conversation']
    
    def get_sender_type(self, obj):
        user = self.context['request']
        user = self.context['request'].user
        conversation = obj.conversation
        if user.id == obj.sender_id:
            if user.id == conversation.initiator_id:
                return 'initiator'
            elif user.id == conversation.receiver_id:
                return 'initiator'
        return 'resiver'

class NotificationChatSerializer(serializers.ModelSerializer):
    favorite = MessageListNotiSerializer(read_only=True)

    class Meta:
        model = NotificationChat
        fields = ['id', 'favorite', 'is_read', 'receiver']