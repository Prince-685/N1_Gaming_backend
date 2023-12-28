from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from django.core.validators import MinLengthValidator

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
class CustomUser(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    credit= models.IntegerField(default=5000)
    is_block=models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class DateModel(models.Model):
    date = models.DateField()

class TimeEntryModel(models.Model):
    date = models.ForeignKey(DateModel, related_name='time_entries', on_delete=models.CASCADE)
    Time = models.TimeField()
    A = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    B = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    C = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    D = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    E = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    F = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    G = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    H = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    I = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    J = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    K = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    L = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    M = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    N = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    O = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    P = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    Q = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    R = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    S = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    T = models.CharField(max_length=2, validators=[MinLengthValidator(2)])

    def __str__(self):
        return f"{self.date.date} - {self.Time}"
    


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, primary_key=True)  # Assuming transaction_id is a string
    username = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.username} - {self.transaction_id} - {self.date}"

class TSN(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    tsn_id = models.CharField(max_length=255, primary_key=True)  # Assuming TSN_id is a string
    gamedate_time = models.DateTimeField()
    playedpoints = models.IntegerField()
    slipdatetime = models.DateTimeField()
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction {self.transaction.transaction_id} - TSN {self.tsn_id} - {self.gamedate_time}"

    class Meta:
        ordering = ['gamedate_time']


class UserGame(models.Model):
    user = models.CharField(max_length=255)
    tsn_entry = models.ForeignKey(TSN, on_delete=models.CASCADE, related_name='user_games')
    game_name = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
                                                        ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'),
                                                        ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'),
                                                        ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T')])
    number = models.CharField(max_length=2)
    Playedpoints = models.IntegerField()
    # Add any other fields you might need

    def __str__(self):
        return f"{self.user} -GameDate_Time: {self.tsn_entry.gamedate_time}, Game: {self.game_name}, Number: {self.number}, Points: {self.Playedpoints}"
    

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    play_points = models.IntegerField()
    earn_points = models.IntegerField()
    end_points = models.IntegerField()
    profit = models.FloatField()
    net_profit = models.FloatField()

    def __str__(self):
        return f"User: {self.user.username} Date:{self.date} Time:{self.time}"
    
class Earn_Point(models.Model):
    date=models.ForeignKey(DateModel, on_delete=models.CASCADE)
    time=models.TimeField()
    A = models.CharField(max_length=255)
    B = models.CharField(max_length=255)
    C = models.CharField(max_length=255)
    D = models.CharField(max_length=255)
    E = models.CharField(max_length=255)
    F = models.CharField(max_length=255)
    G = models.CharField(max_length=255)
    H = models.CharField(max_length=255)
    I = models.CharField(max_length=255)
    J = models.CharField(max_length=255)
    K = models.CharField(max_length=255)
    L = models.CharField(max_length=255)
    M = models.CharField(max_length=255)
    N = models.CharField(max_length=255)
    O = models.CharField(max_length=255)
    P = models.CharField(max_length=255)
    Q = models.CharField(max_length=255)
    R = models.CharField(max_length=255)
    S = models.CharField(max_length=255)
    T = models.CharField(max_length=255)

    def __str__(self):
        return f"Game Date: {self.date.date} - Time : {self.time} "


class Win_Percent(models.Model):
    percent=models.IntegerField()
    pid=models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.percent}"