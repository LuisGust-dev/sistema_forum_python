import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.base.utils import add_form_errors_to_messages
from apps.forum.forms import PostagemForumForm
from django.contrib import messages  
from apps.forum import models
from django.core.paginator import Paginator





# Lista de Postagens.
def lista_postagem_forum(request):
    postagens = models.PostagemForum.objects.filter(ativo=True)
    context = {'postagens': postagens}
    return render(request, 'lista-postagem-forum.html', context)


# Cria postagens      
def criar_postagem_forum(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            postagem_imagens = request.FILES.getlist('postagem_imagens') # pega as imagens
            if len(postagem_imagens) > 5: # faz um count
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
            else:
                forum = form.save(commit=False)
                forum.usuario = request.user
                forum.save()
                for f in postagem_imagens:
                    models.PostagemForumImagem.objects.create(postagem=forum, imagem=f)
                # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
                messages.success(request, 'Seu Post foi cadastrado com sucesso!')
                return redirect('lista-postagem-forum')
    return render(request, 'form-postagem-forum.html', {'form': form})


# Detalhes da postagem
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    form = PostagemForumForm(instance=postagem)
    context = {'form': form, 'postagem': postagem}
    return render(request,'detalhe-postagem-forum.html', context)


# Edtar Postagem
@login_required
def editar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '') 
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+ postagem.titulo +' foi atualizado com sucesso!'

    # Verifica se o usuário autenticado é o autor da postagem
    if request.user != postagem.usuario and not (
            ['administrador', 'colaborador'] in request.user.groups.all() or request.user.is_superuser):
            return redirect('postagem-forum-list') 
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():

            contar_imagens = postagem.postagem_imagens.count() # Quantidade de imagens sque já tenho no post
            postagem_imagens = request.FILES.getlist('postagem_imagens') # Quantidade de imagens que estou enviando para salvar

            if contar_imagens + len(postagem_imagens) > 5:
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
                return redirect(redirect_route)
            else: 
                form.save()
                for f in postagem_imagens:  # for para pegar as imagens e salvar
                    models.PostagemForumImagem.objects.create(postagem=postagem, imagem=f)
                messages.warning(request, message)
                return redirect(redirect_route)
        else:
            add_form_errors_to_messages(request, form) 
    return JsonResponse({'status': 'Ok'})


# Deletar Postagem
@login_required 
def deletar_postagem_forum(request, id): 
    redirect_route = request.POST.get('redirect_route', '')
    print(redirect_route)
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+postagem.titulo+' foi deletado com sucesso!'
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, message)
        
        if re.search(r'/forum/detalhe-postagem-forum/([^/]+)/', redirect_route):
            return redirect('lista-postagem-forum')
        return redirect(redirect_route)

    return JsonResponse({'status':message}) 


# Lista de Postagens no Dashboard (Gerenciar)
def lista_postagem_forum(request):
    form_dict = {}
    if request.path == '/forum/':
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html'
    else: 
        user = request.user 
        template_view = 'dashboard/dash-lista-postagem-forum.html' 
        if ['administrador', 'colaborador'] in user.groups.all() or user.is_superuser:
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            postagens = models.PostagemForum.objects.filter(usuario=user)
    
    for el in postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
        
         
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    paginacao = Paginator(form_list, 3) 
    
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    form_dict = {postagem: form for postagem, form in page_obj}
    
    context = {'page_obj': page_obj, 'form_dict': form_dict}
    return render(request, template_view, context) 

    
    
def remover_imagem(request):
    imagem_id = request.GET.get('imagem_id') # Id da imagem
    verifica_imagem = models.PostagemForumImagem.objects.filter(id=imagem_id) 
    if verifica_imagem:
        postagem_imagem = models.PostagemForumImagem.objects.get(id=imagem_id) 
        # Excluir a imagem do banco de dados e do sistema de arquivos (pasta postagem-forum/)
        postagem_imagem.imagem.delete()
        postagem_imagem.delete()
    return JsonResponse({'message': 'Imagem removida com sucesso.'})