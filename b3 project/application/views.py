from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login ,logout,authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'home.html')
def register(request):
    if request.method == 'POST':
        First_Name = request.POST['name']
        Email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmation_password = request.POST['cnfm_password']
        if password == confirmation_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists, please choose a different one.')
                return redirect('register')
            else:
                if User.objects.filter(email=Email).exists():
                    messages.error(request, 'Email already exists, please choose a different one.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=Email,
                        first_name=First_Name,
                    )
                    user.save()
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
        return render(request, 'register.html')
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user=User.objects.get(username=username)
            if user.check_password(password):
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,'login successfull')
                    return redirect('/')
                else:
                   messages.error(request,'please check the Password Properly')
                   return redirect('login')
            else:
                messages.error(request,"please check the Password Properly")  
                return redirect('login') 
        else:
            messages.error(request,"username doesn't exist")
            return redirect('login')
    return render(request,'login.html')
# Load and preprocess the dataset
def logout_view(request):
    logout(request)
    return redirect('login')
from .models import Vehicle, Equipment, Booking, Review
@login_required
def add_vehicle(request):
    if request.method == 'POST':
        name = request.POST['name']
        brand = request.POST['brand']
        model = request.POST['model']
        registration_number = request.POST['registration_number']
        daily_rate = request.POST['daily_rate']

        Vehicle.objects.create(
            name=name,
            brand=brand,
            model=model,
            registration_number=registration_number,
            daily_rate=daily_rate,
            owner=request.user
        )
        messages.success(request, 'Vehicle added successfully!')
        return redirect('home')
    return render(request, 'add_vehicle.html')
@login_required
def vehicle_list(request):
    user=request.user
    if user.is_staff:
        vehicles = Vehicle.objects.filter(owner=request.user)
    else:
        vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})
@login_required
def add_equipment(request,pk):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        description = request.POST['description']
        condition = request.POST['condition']
        daily_rate = request.POST['daily_rate']
        vehicle_id = pk
        vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user)
        Equipment.objects.create(
            vehicle=vehicle,
            name=name,
            category=category,
            description=description,
            condition=condition,
            daily_rate=daily_rate,
            owner=request.user
        )
        messages.success(request, 'Equipment added successfully!')
        return redirect('equipment_list',pk=vehicle_id)

    vehicles = Vehicle.objects.filter(id=pk,owner=request.user,)
    
    return render(request, 'add_equipment.html', {'vehicles': vehicles})
@login_required
def equipment_list(request, pk):
    user = request.user
    
    if user.is_staff:
        if Vehicle.objects.filter(id=pk, owner=user).exists():
            vehicle = get_object_or_404(Vehicle, id=pk, owner=user)
            equipments = Equipment.objects.filter(owner=user, vehicle=vehicle)
        else:
            return redirect('vehicle_list')
    else:
        vehicle = get_object_or_404(Vehicle, id=pk)
        equipments = Equipment.objects.filter(vehicle=vehicle)
        bookings = Booking.objects.filter(vehicle=vehicle)
        return render(request, 'vehicleview.html', {'equipments': equipments, 'vehicle':vehicle,'vehicle_id': pk, 'bookings': bookings})

    return render(request, 'equipment_list.html', {'equipments': equipments, 'vehicle_id': pk})

@login_required
def delete_equipment(request,pk):
    equipment = get_object_or_404(Equipment, id=pk, owner=request.user)
    equipment.delete()
    messages.success(request, 'Equipment deleted successfully!')
    return redirect('equipment_list',pk=equipment.vehicle.id)
@login_required
def book_vehicle(request,pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    equipments = Equipment.objects.filter(vehicle=vehicle)
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_equipment_ids = request.POST.getlist('equipment')
        
        booking = Booking.objects.create(
            customer=request.user,
            vehicle=vehicle,
            start_date=start_date,
            end_date=end_date,
            payment_status='Pending',
            book_status='Pending'
        )
        
        for equipment_id in selected_equipment_ids:
            equipment = get_object_or_404(Equipment, id=equipment_id)
            booking.equipment = equipment
            booking.save()
        
        messages.success(request, 'Booking successful!')
        return redirect('equipment_list',pk=pk)
    
    bookings = Booking.objects.filter(vehicle=vehicle)
    return render(request, 'vehicle_detail.html', {'vehicle': vehicle, 'equipments': equipments, 'bookings': bookings})

# Add Review View
@login_required
def add_review(request, item_type, item_id):
    if item_type == 'vehicle':
        item = get_object_or_404(Vehicle, id=item_id)
    else:
        item = get_object_or_404(Equipment, id=item_id)

    if request.method == 'POST':
        rating = request.POST['rating']
        review_text = request.POST['review_text']

        Review.objects.create(
            customer=request.user,
            vehicle=item if item_type == 'vehicle' else None,
            equipment=item if item_type == 'equipment' else None,
            rating=rating,
            review_text=review_text
        )
        messages.success(request, 'Review submitted successfully!')
        return redirect('home')

    return render(request, 'add_review.html', {'item': item, 'item_type': item_type})

@login_required
def view_bookings(request):
    if request.user.is_staff:  # Admin/Owner views all bookings
        bookings = Booking.objects.filter(vehicle__owner=request.user,book_status='Pending')
    else:  # Normal users see only their bookings
        bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request,pk):
    booking = get_object_or_404(Booking, id=pk, customer=request.user)
    booking.book_status = 'Cancelled'
    booking.payment_status = 'Cancelled'
    booking.save()
    messages.success(request, 'Booking cancelled successfully!')
    return redirect('user_bookings')

@login_required
def confirm_booking(request,pk):
    booking = get_object_or_404(Booking, id=pk)
    booking.book_status = 'Confirm'
    booking.payment_status = 'pending'
    booking.save()
    messages.success(request, 'Booking cancelled successfully!')
    return redirect('view_bookings')

@login_required
def confirm_list(request):
    if request.user.is_staff:  # Admin/Owner views all bookings
        bookings = Booking.objects.filter(vehicle__owner=request.user,book_status='Confirm' or 'Cancel')
    return render(request, 'view_bookings.html', {'bookings': bookings,'confirmed':True})