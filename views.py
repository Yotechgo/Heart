from django.shortcuts import render, redirect
import joblib
import numpy as np
import os
from .models import HeartPrediction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "heart_disease_model.pkl")

# Load the ML model
model = joblib.load(MODEL_PATH)

@login_required(login_url='login')
def predict_heart_disease(request):
    prediction = None

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            data = [
                float(request.POST.get("age")),
                float(request.POST.get("sex")),
                float(request.POST.get("cp")),
                float(request.POST.get("trestbps")),
                float(request.POST.get("chol")),
                float(request.POST.get("fbs")),
                float(request.POST.get("restecg")),
                float(request.POST.get("thalach")),
                float(request.POST.get("exang")),
                float(request.POST.get("oldpeak")),
                float(request.POST.get("slope")),
                float(request.POST.get("ca")),
                float(request.POST.get("thal"))
            ]

            final_input = np.array(data).reshape(1, -1)

            # ----- HEALTHY OVERRIDE -----
            if (data[0] < 100 and data[3] <= 120 and data[4] <= 200 and
                data[5] == 0 and data[8] == 0 and data[9] <= 3.0 and data[11] == 0):
                prediction = "Low risk of Heart Disease"

            # ----- DANGEROUS OVERRIDE -----
            elif (data[3] >= 180 or data[4] >= 260 or data[8] == 1 or
                  data[9] >= 6.0 or data[11] >= 2):
                prediction = "High risk of Heart Disease"

            # ----- MODEL PREDICTION -----
            else:
                pred = model.predict(final_input)[0]
                if pred == 0:
                    prediction = "Low risk of Heart Disease"
                else:
                    prediction = "High risk of Heart Disease"

            # Save prediction
            HeartPrediction.objects.create(
                user=request.user,
                name=name,
                age=data[0],
                sex=int(data[1]),
                cp=int(data[2]),
                trestbps=data[3],
                chol=data[4],
                fbs=int(data[5]),
                restecg=int(data[6]),
                thalach=data[7],
                exang=int(data[8]),
                oldpeak=data[9],
                slope=int(data[10]),
                ca=int(data[11]),
                thal=int(data[12]),
                prediction=prediction
            )

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render(request, "prediction_form.html", {
        "prediction": prediction
    })


# ✅ Prediction History View
@login_required(login_url='login')
def prediction_history(request):
    risk_filter = request.GET.get("risk", "all")

    user_history = HeartPrediction.objects.filter(user=request.user)

    if risk_filter == "high":
        history = user_history.filter(prediction__icontains="High risk")
    elif risk_filter == "low":
        history = user_history.filter(prediction__icontains="Low risk")
    else:
        history = user_history

    history = history.order_by("-created_at")

    paginator = Paginator(history, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "prediction_history.html", {
        "page_obj": page_obj,
        "risk_filter": risk_filter
    })


# ✅ Homepage View
def homepage(request):
    return render(request, "homepage.html")


# ✅ User/Admin Login View
def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        return redirect('predict_heart_disease')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        role = request.POST.get('role', 'user')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if role == 'admin':
                    if user.is_staff or user.is_superuser:
                        login(request, user)
                        return redirect('/admin/')
                    else:
                        messages.error(request, "Access denied: This account does not have Admin privileges.")
                else:
                    login(request, user)
                    return redirect('predict_heart_disease')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# ✅ User Registration View
def register_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        return redirect('predict_heart_disease')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, "Registration successful! Please login below.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# ✅ User Logout View
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('homepage')
