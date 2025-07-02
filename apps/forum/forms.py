from django import forms
from .models import PostagemForum

class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo', 'anexar_imagem']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostagemForumForm, self).__init__(*args, **kwargs)

        # Adiciona classes aos campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-check-input'
                field.widget.attrs['style'] = 'transform: scale(1.3); margin-left: 0.3rem;'
            else:
                field.widget.attrs['class'] = 'form-control'

        # Renomeia o label do checkbox para algo mais amigável
        self.fields['ativo'].label = "Publicar agora?"
        self.fields['ativo'].required = False  # Garante que pode ser deixado desmarcado
