from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group 
from django.shortcuts import render, redirect, get_object_or_404
from perfil.models import Perfil
from contas.models import MyUser
from contas.forms import CustomUserCreationForm, UserChangeForm
from contas.permissions import grupo_colaborador_required



def timeout_view(request):
    return render(request, 'timeout.html')
 
 
# Logout (Sair do sistema)
def logout_view(request):
    logout(request)
    return redirect('home')


# Autenticar um usuario
def login_view(request):
    if request.method == 'POST': 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        user = authenticate(request, email=email, password=password) 
        if user is not None: 
            login(request, user) 
            return redirect('home') 
        else:
            messages.error(request, 'Email ou senha inválidos')
    if request.user.is_authenticated: 
        return redirect('home')
    return render(request, 'login.html')


# Registrar um usuário
def register_view(request):
    if request.method == "POST": # metodo POST
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid(): 
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)
            Perfil.objects.create(usuario=usuario) 

            messages.success(request, 'Registrado. Agora faça o login para começar!')
            
            return redirect('login') 
        else:
            
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm() 
    return render(request, "register.html",{"form": form})



# Atualizar usuario autenticado (meu usuario)
@login_required()
def atualizar_meu_usuario(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

# Atualizar usuário passa um parametro ID de qualquer usuario
@login_required()
@grupo_colaborador_required(['administrador','colaborador'])
def atualizar_usuario(request, username):
    user = get_object_or_404(MyUser, username=username)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def lista_usuarios(request): # Lista Cliente
    lista_usuarios = MyUser.objects.select_related('perfil').filter(is_superuser=False)
    return render(request, 'lista-usuarios.html', {'lista_usuarios': lista_usuarios})