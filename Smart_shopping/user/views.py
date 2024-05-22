from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from .models import CreateUserForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user.models import History, SavedHistory
from products.models import Product

# Create your views here.
def register(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'users/register.html', context)

def loginUser(request):
    message = ''
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            message = 'Mật khẩu không chính xác!'
    context = {'message': message}
    return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
def save_history(request):
    if request.method == 'POST':
        product1_id = request.POST.get('product1_id')
        product2_id = request.POST.get('product2_id')

        existing_history = SavedHistory.objects.filter_by_products(product1_id=product1_id, product2_id=product2_id, account_id=request.user).first()

        if existing_history:
            existing_history.delete()  # Xoá lịch sử nếu đã tồn tại
            return JsonResponse({'message': 'History deleted and new history created successfully'})
        else:
            new_history = SavedHistory(product1_id=product1_id, product2_id=product2_id, account_id=request.user)
            new_history.save()
            # Trả về một phản hồi JSON để thông báo rằng lịch sử đã được tạo mới
            return JsonResponse({'message': 'New history created successfully'})
    return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
def recent_history(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'Authentication required'}, status=400)
        
        product1_name = request.POST.get('product1_name')
        product2_name = request.POST.get('product2_name')
        product1_id = Product.objects.filter(product_name=product1_name).first().product_id
        product2_id = Product.objects.filter(product_name=product2_name).first().product_id

        # Kiểm tra xem cặp product1_id và product2_id đã tồn tại trong lịch sử hay chưa
        existing_history = History.objects.filter_by_products(product1_id=product1_id, product2_id=product2_id, account_id=request.user).first()

        if existing_history:
            # Nếu đã tồn tại lịch sử, cập nhật thời gian
            existing_history.save()
            # Trả về một phản hồi JSON để thông báo rằng lịch sử đã được cập nhật
            return JsonResponse({'message': 'History updated successfully'})
        else:
            # Nếu không tồn tại lịch sử, tạo mới
            new_history = History(product1_id=product1_id, product2_id=product2_id, account_id=request.user)
            new_history.save()
            # Trả về một phản hồi JSON để thông báo rằng lịch sử đã được tạo mới
            return JsonResponse({'message': 'New history created successfully'})

    # Nếu không phải là phương thức POST hoặc có lỗi xảy ra, trả về một phản hồi JSON trống với mã lỗi
    return JsonResponse({}, status=400)

def get_recent_history(request):
    # Lấy ra 5 lịch sử gần đây nhất
    products = History.objects.filter(account_id=request.user).order_by('-time')
    
    # Chuyển đổi các lịch sử thành một danh sách các từ điển
    return render(request, 'recent_history.html', {'products': products})

def get_saved_history(request):
    # Lấy ra 5 lịch sử gần đây nhất
    products = SavedHistory.objects.filter(account_id=request.user).order_by('-time')
    # Chuyển đổi các lịch sử thành một danh sách các từ điển

    return render(request, 'saved_history.html', {'products': products})

def check_history(product1_id, product2_id, user):
    existing_history = SavedHistory.objects.filter_by_products(product1_id=product1_id, product2_id=product2_id, account_id=user).first()

    if existing_history:
        return True
    
    return False

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'users/profile.html')
    else:
        return redirect('login')

def change_password(request):
    return render(request, 'users/password_reset.html') 