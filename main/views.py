

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Car, Profile, CarImage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CarForm
from .brand_models import MODELS_BY_BRAND
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.mail import send_mail
import random


def home(request):
    cars = Car.objects.filter(featured=True)[:4]
    return render(request, 'main/home.html', {
        'cars': cars,
        'MODELS_BY_BRAND': MODELS_BY_BRAND
    })





def search(request):
    brand = request.GET.get('brand', '')
    model = request.GET.get('model', '')

    filtered_cars = Car.objects.all()

    if brand:
        filtered_cars = filtered_cars.filter(brand=brand)
    if model:
        filtered_cars = filtered_cars.filter(model=model)

    return render(request, 'main/search.html', {
        'cars': filtered_cars,
        'MODELS_BY_BRAND': MODELS_BY_BRAND
    })


#  Afiseaza toate anunturile în pagina Anunțuri
def ads(request):
    cars = Car.objects.all().order_by('-id')
    return render(request, 'main/ads.html', {
        'cars': cars,
        'MODELS_BY_BRAND': MODELS_BY_BRAND
    })

#  Detalii pentru fiecare anunț
def ad_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'main/ad_detail.html', {'car': car})


@login_required
def sell(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.transmission = request.POST.get('transmission')
            car.featured = 'featured' in request.POST
            car.premium = 'premium' in request.POST
            car.save()

            images = request.FILES.getlist("images")
            if len(images) > 8:
                messages.error(request, "Poți adăuga maximum 8 imagini suplimentare.")
                return render(request, "main/sell.html", {"form": form, "MODELS_BY_BRAND": MODELS_BY_BRAND})

            for image in images:
                CarImage.objects.create(car=car, image=image)

            messages.success(request, "Anunțul a fost publicat cu succes!")
            return redirect("ads")
    else:
        form = CarForm()

    return render(request, "main/sell.html", {
        "form": form,
        "MODELS_BY_BRAND": MODELS_BY_BRAND
    })


def ads(request):
    cars = Car.objects.all().order_by('-premium', '-id')  # 🔹 PREMIUM PRIMELE

    brand = request.GET.get("brand")
    model = request.GET.get("model")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")
    horsepower = request.GET.get("horsepower")
    fuel = request.GET.get("fuel")
    car_body = request.GET.get("car_body")
    year_min = request.GET.get("year_min")
    year_max = request.GET.get("year_max")
    km_min = request.GET.get("km_min")
    km_max = request.GET.get("km_max")
    hp_min = request.GET.get("hp_min")
    hp_max = request.GET.get("hp_max")
    cc_min = request.GET.get("cc_min")
    cc_max = request.GET.get("cc_max")
    transmission = request.GET.get("transmission")

    if brand:
        cars = cars.filter(brand=brand)
    if model:
        cars = cars.filter(model=model)
    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)
    if horsepower:
        cars = cars.filter(horsepower__gte=horsepower)
    if fuel:
        cars = cars.filter(fuel_type__icontains=fuel)
    if car_body:
        cars = cars.filter(car_body__icontains=car_body)
    if year_min:
        cars = cars.filter(year__gte=year_min)
    if year_max:
        cars = cars.filter(year__lte=year_max)
    if km_min:
        cars = cars.filter(mileage__gte=km_min)
    if km_max:
        cars = cars.filter(mileage__lte=km_max)
    if hp_min:
        cars = cars.filter(horsepower__gte=hp_min)
    if hp_max:
        cars = cars.filter(horsepower__lte=hp_max)
    if cc_min:
        cars = cars.filter(engine_capacity__gte=cc_min)
    if cc_max:
        cars = cars.filter(engine_capacity__lte=cc_max)
    if transmission:
        cars = cars.filter(transmission__iexact=transmission)

    return render(request, 'main/ads.html', {
        'cars': cars,
        'MODELS_BY_BRAND': MODELS_BY_BRAND
    })




def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "home")  # Redirecționează corect după login
            return redirect(next_url)
        else:
            messages.error(request, "Nume de utilizator sau parolă incorectă.")

    return render(request, "main/login.html")


def signup(request):
    if request.method == "POST":  # Dacă s-a trimis formularul
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        age = request.POST.get("age", "")
        address = request.POST.get("address", "")
        description = request.POST.get("description", "")

        if password != confirm_password:
            messages.error(request, "Parolele nu se potrivesc.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Acest email este deja folosit.")
            return redirect("signup")

        # Folosim email-ul ca username
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)
        messages.success(request, "Cont creat cu succes!")
        return redirect("home")

    return render(request, "main/signup.html")


@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")

        profile.phone = request.POST.get("phone", "")
        profile.age = request.POST.get("age", "")
        profile.address = request.POST.get("address", "")
        profile.description = request.POST.get("description", "")

        user.save()
        profile.save()

        messages.success(request, "Profilul a fost actualizat cu succes!")
        return redirect("home")  # Redirecționează către pagina principală

    return render(request, "main/edit_profile.html", {"user": user, "profile": profile})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, "main/profile.html", {"user": request.user})

@login_required
@require_POST
def toggle_favorite(request):
    car_id = request.POST.get("car_id")
    car = get_object_or_404(Car, id=car_id)

    profile, created = Profile.objects.get_or_create(user=request.user)

    if car in profile.favorites.all():
        profile.favorites.remove(car)
        return JsonResponse({"success": True, "is_favorite": False})
    else:
        profile.favorites.add(car)
        return JsonResponse({"success": True, "is_favorite": True})


@login_required
def favorites_view(request):
    profile = Profile.objects.get(user=request.user)
    favorite_cars = profile.favorites.all()
    return render(request, "main/favorites.html", {"cars": favorite_cars})

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.seller != request.user:
        messages.error(request, "Nu ai permisiunea să ștergi acest anunț.")
        return redirect("ad_detail", car_id)

    car.delete()
    messages.success(request, "Anunțul a fost șters cu succes.")
    return redirect("ads")

def confirm_email_before_password_change(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            code = str(random.randint(100000, 999999))
            request.session["reset_email"] = email
            request.session["reset_code"] = code

            send_mail(
                "Cod de resetare parolă - CarDealerPro",
                f"Codul tău de verificare este: {code}",
                "noreply@cardealerpro.ro",
                [email],
                fail_silently=False,
            )

            return redirect("confirm_code")
        except User.DoesNotExist:
            messages.error(request, "Nu există niciun cont cu acest email.")
    return render(request, "main/confirm_email_for_password_change.html")


def confirm_code_view(request):
    if request.method == "POST":
        code_entered = request.POST.get("code")
        if code_entered == request.session.get("reset_code"):
            return redirect("reset_password")
        else:
            messages.error(request, "Cod incorect.")
    return render(request, "main/confirm_code.html")


def reset_password_view(request):
    if request.method == "POST":
        password = request.POST.get("password")
        email = request.session.get("reset_email")
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Parola a fost schimbată cu succes.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "Eroare la schimbarea parolei.")
    return render(request, "main/reset_password.html")
