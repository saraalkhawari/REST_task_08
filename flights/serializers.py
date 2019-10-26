from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date

from .models import Flight, Booking, Profile


class FlightSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flight
		fields = ['destination', 'time', 'price', 'id']


class BookingSerializer(serializers.ModelSerializer):
	flight = serializers.SlugRelatedField(
	read_only = True,
	slug_field = 'destination'
		)
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'id']


class BookingDetailsSerializer(serializers.ModelSerializer):
	total = serializers.SerializerMethodField()
	flight = FlightSerializer()
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'passengers', 'id' , 'total']

	def get_total(self,obj):
		price = obj.flight.price
		passengers = obj.passengers
		total = price*passengers
		return total 



class AdminUpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['date', 'passengers']


class UpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['passengers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class UserSerlializer(serializers.ModelSerializer):
	class Meta :
		model = User
		fields = ['first_name','last_name']



class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerlializer()
	past_bookings= serializers.SerializerMethodField()
	tier= serializers.SerializerMethodField()
	class Meta:
		model = Profile
		fields = ['user', 'miles','past_bookings', 'tier']

	def get_past_bookings(self,obj):
		bookings= Booking.objects.filter(user = obj.user, date__lt=date.today())
		serializer = BookingSerializer(bookings, many= True)
		return serializer.data

	def get_tier (self,obj):
		miles = obj.miles
		if miles < 10000 :
			return 'Blue'
		if miles < 60000 :
			return 'Silver'
		if miles < 100000 :
			return 'Gold'
		return 'Platinum' 










