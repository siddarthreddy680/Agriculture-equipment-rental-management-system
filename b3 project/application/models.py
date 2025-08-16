from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50, unique=True)
    availability_status = models.BooleanField(default=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking to owner
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.model})"
    



class Equipment(models.Model):
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # Example: Seeder, Harvester, Plow
    description = models.TextField()
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used')])
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Equipment owner
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    




class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    payment_status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled')],
    default='Pending ')
    created_at = models.DateTimeField(auto_now_add=True)
    book_status=models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Confirm', 'Confirm'), ('Cancelled', 'Cancelled')],default='Pending '
    )
    def __str__(self):
        return f"Booking by {self.customer.username} from {self.start_date} to {self.end_date}"
    


    
class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who gives the review
    vehicle = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    equipment = models.ForeignKey('Equipment', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')],
        default=5
    )
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.username} - {self.rating} Stars"
