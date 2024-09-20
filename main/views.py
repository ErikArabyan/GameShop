from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMessage
from GameShop.settings import EMAIL_HOST_USER
from django.core.paginator import Paginator
from math import ceil
import os

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator


def home(request):
    user = request.user
    welcometext = WelcomeText.objects.get()
    features = Feature.objects.all()
    genres = Genres.objects.all()
    games = Game.objects.all().order_by('?')
    mgames = games.filter(most_played = True)
    form = SubscribeForm()
    bestprice = Game.objects.all().order_by('discount').last()

    if 'search' in request.POST:
        keyword = request.POST.get('searchKeyword')
        games = Game.objects.filter(name__icontains = keyword).order_by('?')

    if 'subscribe' in request.POST:
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            subscriber = [request.POST.get('email')]
            email = EmailMessage(
                subject='Thank you for subscribing in our newspaper',
                body='Շնորհակալություն մեզ միանալու համար',
                from_email=EMAIL_HOST_USER,
                to = subscriber
            )
            email.send()
            return redirect('home')
        else:
            form = SubscribeForm()

    if 'game' in request.POST:
        user = CustomUser.objects.get(id=request.user.id)
        user.shopping_cart.add(request.POST.get('gameid'))

        
    for i in games:
        i.disc_price = int(i.price - i.price * i.discount / 100)
    context = {
        'welcometext': welcometext,
        'features': features,
        'games': games,
        'genres': genres,
        'mgames': mgames,
        'bestprice': bestprice
    }
    return render(request, 'index.html', context)

def details(request, id):
    game = get_object_or_404(Game, id=id)
    games = Game.objects.filter(GameGenre = game.GameGenre).order_by('?')
    disc_price = int(game.price - game.price * game.discount / 100)
    game_details = get_object_or_404(GameDetails, game_id=id)
    context = {
        'game': game,
        'games': games,
        'disc_price': disc_price,
        'game_details': game_details
    }
    return render(request, 'product-details.html', context)

def contact(request):
    user = request.user
    if request.method == 'POST':
        if user.username:
            email = EmailMessage(
                subject=request.POST.get('subject'),
                body=f'''{request.POST.get("message")}
                From User: {user.username}
                Email: {user.email}''',
                from_email=EMAIL_HOST_USER,
                to = [EMAIL_HOST_USER]
            )
            email.send()
        else:
            email = EmailMessage(
                subject=request.POST.get('subject'),
                body=f'{request.POST.get("message")} \n\n From: {request.POST.get("name")} {request.POST.get("surname")} \n Email: {request.POST.get("email")}',
                from_email=EMAIL_HOST_USER,
                to = [EMAIL_HOST_USER]
            )
            email.send()
    return render(request, 'contact.html')

def shop(request):
    games = Game.objects.all()
    p = Paginator(Game.objects.all().order_by('name'),4)
    Game_count = Game.objects.count()
    page_count = ceil(Game_count/4)
    page_count = list(range(1,page_count+1)) 
    page = request.GET.get('page')
    games = p.get_page(page)
    if page is not None:
        page = int(page)
    else:
        page = 1
    for i in games:
        i.disc_price = int(i.price - i.price * i.discount / 100)
    context = {
        'games': games,
        'page_count':page_count,
        'page': page,
    }
    return render(request, 'shop.html', context)

def Register(request):
    form = CreateUserF
    message = ''
    if 'register' in request.POST:
        form = CreateUserF(request.POST)
        if form.is_valid():
            global user
            user = form.save(commit=False)            
            current_site = get_current_site(request)
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
            message = render_to_string('verify_email.html',context=context,)
            email = EmailMessage(
                'Veryfi email',
                message,
                to=[user.email],
            )
            email.send()
            return redirect('confirm_email')
        
    elif 'login' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = email, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        message = 'Email or Password are wrong'
    return render(request, 'Register.html', {'form': form, 'message': message})

def confirm_email(request):
    return render(request, 'confirm_email.html')

def Emailverify(request, uidb64, token):
    global user
    if not 'user' in globals():
        return render(request, 'error404.html')   
    if user is not None and token_generator.check_token(user, token):
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'error404.html')   

def Logout(request):
    logout(request)
    return redirect('home')

def personal_account(request):
    global chgem
    chgem = [request.user, request.POST.get('email')]
    game = request.user.shopping_cart.values()
    for i in game:
        i['disc_price'] = int(i['price'] - i['price'] * i['discount'] / 100)
    user = request.user
    form = UpdateUserForm(instance=user)
    if 'changeinfo' in request.POST:
        new_image = str(request.FILES.get('img'))
        old_image = os.path.basename(form['img'].value().url)
        if old_image != new_image:
            form = UpdateUserForm(request.POST, request.FILES, instance=user)
        else:
            form = UpdateUserForm(request.POST, instance=user)

        if os.path.isfile(user.img.path) and 'img' in form.changed_data:
            os.remove(user.img.path)

        if form.is_valid():
            form.save()

        if chgem[1]:
            current_site = get_current_site(request)
            context = {
                'user': chgem[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(chgem[0].pk)),
                'token': token_generator.make_token(chgem[0]),
            }
            message = render_to_string('change_email.html',context=context,)
            email = EmailMessage(
                'Veryfi email',
                message,
                to=[chgem[1]],
            )
            email.send()
            return redirect('confirm_email')
        
    if 'game' in request.POST:
        user = CustomUser.objects.get(id=request.user.id)
        user.shopping_cart.remove(request.POST.get('gameid'))
        return redirect('personal_account')

    if 'sendemail' in request.POST:
        subscribers = Subscribe.objects.all()
        for i in subscribers: 
            email = EmailMessage(
                        subject=request.POST.get('Subject'),
                        body=f'{request.POST.get("message")}',
                        from_email=EMAIL_HOST_USER,
                        to = [i.email]
                    )
            email.send()
    context = {
        'game': game,
        'form': form
    }
    return render(request, 'personal_account.html', context)

def ChangeEmail(request, uidb64, token):
    global chgem
    if chgem[0] is not None and token_generator.check_token(chgem[0], token):
        user = CustomUser.objects.get(email = chgem[0].email)
        user.email = chgem[1]
        user.save()
        login(request, chgem[0])
        return redirect('home')
    return render(request, 'error404.html')  