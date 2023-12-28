from rest_framework import serializers
from .models import CustomUser, DateModel, TimeEntryModel,Admin,Transaction,TSN,UserGame,Account,Earn_Point

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def get_fields(self):
        fields = super().get_fields()
        fields.pop('last_login', None)
        return fields

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntryModel
        fields = '__all__'

class DateModelSerializer(serializers.ModelSerializer):
    time_data = TimeEntrySerializer(many=True, read_only=True)

    class Meta:
        model = DateModel
        fields = ['date', 'time_data']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'username', 'date']

class TSNSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    gamedate_time = serializers.DateTimeField(format='%d/%m/%Y %I:%M %p')
    slipdatetime =  serializers.DateTimeField(format='%d/%m/%Y %I:%M:%S')
    class Meta:
        model = TSN
        fields = ['transaction', 'tsn_id', 'gamedate_time', 'playedpoints', 'slipdatetime', 'cancel']

class UserGameSerializer(serializers.ModelSerializer):
    tsn_entry = TSNSerializer()

    class Meta:
        model = UserGame
        fields = ['user', 'tsn_entry.gamedate_time', 'game_name', 'number', 'Playedpoints']


class AccountSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Account
        fields = ('play_points', 'earn_points', 'end_points', 'profit', 'net_profit')


class EarnPointSerializer(serializers.ModelSerializer):
    date=DateModelSerializer()
    class Meta:
        model = Earn_Point
        fields = '__all__'