from django import forms
from .models import PostagemForum
import datetime

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    postagem_imagens = MultipleFileField(
        label='Selecione no máximo 5 imagens.', required=False
    )

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'ativo',]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['usuario'].initial = user

            if user.is_superuser or user.groups.filter(name__in=['administrador', 'colaborador']).exists():
                self.fields['usuario'].disabled = True

        # Adiciona classes aos campos
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-check-input'
                field.widget.attrs['style'] = 'transform: scale(1.3); margin-left: 0.3rem;'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['ativo'].label = "Publicar agora?"
        self.fields['ativo'].required = False
