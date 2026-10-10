from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignupForm,ProfileEditForm

from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import  login_required

from products.models import Product, Customization

from cart.models import CartItem

from cart.views import get_cart


def signup(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            # Profile.objects.create(
            #     user=user
            # )

            return redirect('login')

    else:

        form = SignupForm()


    return render(
        request,
        'accounts/signup.html',
        {'form': form}
    )

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('profile')

        else:
            return render(request, 'accounts/login.html', {'error':'Invalid username or password.'})


    return render(request, 'accounts/login.html')



def user_logout(request):

    logout(request)

    return redirect('login')


@login_required
def profile(request):
    return render(
        request,'accounts/profile.html'
    )

@login_required
def profile_edit(request):

    if request.method == 'POST':

        form = ProfileEditForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileEditForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/profile_edit.html',
        {'form': form}
    )


def home(request):
    trending_products = Product.objects.all().order_by('-id')

    print("TOTAL PRODUCTS:", Product.objects.count())
    print("TRENDING PRODUCTS:", trending_products.count())

    return render(
        request,
        'home.html',
        {'trending_products': trending_products}
    )

def shop(request):
    products = Product.objects.select_related('category').all()

    category_name = request.GET.get('category')

    if category_name:
        products = products.filter(category__name__iexact=category_name)

    return render(
        request,
        'shop.html',
        {'products': products}
    )
def product_detail(request, product_id):

    product = get_object_or_404(Product,id=product_id)

    return render(
        request,
        'product_detail.html',
        {'product': product}
    )


def customize_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        color = request.POST.get('color', 'White')
        name_to_print = request.POST.get('name', '').strip()
        photo = request.FILES.get('photo')
        message = request.POST.get('message', '').strip()

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 0

        if quantity < 1 or quantity > product.stock:
            return render(
                request,
                'customize_product.html',
                {
                    'product': product,
                    'error': 'Please select a valid quantity.'
                }
            )

        customization = Customization.objects.create(
            product=product,
            color=color,
            name_to_print=name_to_print,
            photo=photo,
            message=message,
            quantity=quantity
        )

        cart = get_cart(request)

        CartItem.objects.create(
            cart=cart,
            product=product,
            customization=customization,
            quantity=quantity
        )

        return redirect('cart')

    return render(
        request,
        'customize_product.html',
        {'product': product}
    )
