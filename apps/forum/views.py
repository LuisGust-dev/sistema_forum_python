from datetime import date
import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from apps.base.utils import add_form_errors_to_messages
from apps.forum import models
from django.contrib import messages
from apps.forum.forms import PostagemForumForm


def lista_postagem_forum(request):
    #valida as rotas
    if request.path == '/forum/':
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html'
    else: # Mostra no Dashboard
        user = request.user
        lista_grupos = ['administrador', 'colaborador']
        template_view = 'dashboard/dash-lista-postagem-forum.html'
        if any(grupo.name in lista_grupos for grupo in user.groups.all() ) or user.is_superuser:
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            postagens = models.PostagemForum.objects.filter(usuario=user)
    context = {'postagens': postagens}
    return render(request, template_view, context)

@login_required
def criar_postagem_forum(request):
    user = request.user
    lista_grupos = ['administrador', 'colaborador']
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES, user=request.user )
        if form.is_valid():
            forum = form.save(commit=False)
            if not (user.is_superuser or user.groups.filter(name__in=lista_grupos).exists()):
                forum.usuario = user
            forum.save()
            messages.success(request, 'Seu Post foi cadastrado com sucesso!')
            return redirect('lista-postagem-forum')
    else:
        form = PostagemForumForm(user=request.user)
    return render(request, 'form-postagem-forum.html', {'form': form})

# Detalhes da postagem (ID)
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    form = PostagemForumForm(instance=postagem)
    context = {'postagem': postagem, 'form': form}
    return render(request, 'detalhe-postagem-forum.html', context)

# Editar postagem (ID)
@login_required
def editar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '')
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+ postagem.titulo +' Foi atualizado com sucesso!'

    lista_grupos = ['administrador', 'colaborador']
    user = request.user
    if not (user.is_superuser or user.id == postagem.usuario.id or any(grupo.name in lista_grupos for grupo in user.groups.all())):
        messages.error(request, 'Seu usuário não tem permissão para acessar essa página!')
        return redirect('lista-postagem-forum')
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES, instance=postagem, user=user)
        if form.is_valid():
            postagem = form.save(commit=False)
            if not (user.is_superuser or user.groups.filter(name__in=lista_grupos).exists()):
                postagem.usuario = user
            postagem.save()
            messages.warning(request,message )
        else:
            add_form_errors_to_messages(request, form)
        return redirect(redirect_route)
    else:
        add_form_errors_to_messages(request, form) 
    return JsonResponse({'status': 'Ok'}) # Coloca por enquanto.

#Deletar postagem (ID)
@login_required
def deletar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '')
    print(redirect_route)
    postagem = get_object_or_404(models.PostagemForum, id=id)
    print(postagem)
    message = 'O Post '+ postagem.titulo +' foi deletado com sucesso!'
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'lista-postagem-forum'
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, message)

        if re.search(r'/forum/detalhe-postagem-forum/([^/]+)/', redirect_route):
            return redirect('lista-postagem-forum')
            return redirect(redirect_route)

    
        return redirect('lista-postagem-forum')
    return render(request, 'detalhe-postagem-forum.html', {'postagem': postagem, })
