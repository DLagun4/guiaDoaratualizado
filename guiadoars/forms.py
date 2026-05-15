from django import forms
from .models import Instituicao, CategoriaDoacao, SugestaoInstituicao

class InstituicaoForm(forms.ModelForm):
    outros_categoria = forms.CharField(
        required=False,
        label="Outra categoria (escreva o nome)",
        help_text="Caso a categoria desejada não esteja na lista, digite aqui."
    )

    class Meta:
        model = Instituicao
        fields = '__all__'
        widgets = {
            'categorias_doacao': forms.CheckboxSelectMultiple,
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            outros_nome = self.cleaned_data.get('outros_categoria')
            if outros_nome:
                outros_nome = outros_nome.strip().title()
                categoria, created = CategoriaDoacao.objects.get_or_create(
                    nome=outros_nome,
                    defaults={'personalizada': True, 'descricao': 'Criada via formulário'}
                )
                instance.categorias_doacao.add(categoria)
        else:
            instance.save = lambda: self.save_m2m(instance)
        return instance

    def save_m2m(self, instance):
        instance.save()
        outros_nome = self.cleaned_data.get('outros_categoria')
        if outros_nome:
            outros_nome = outros_nome.strip().title()
            categoria, _ = CategoriaDoacao.objects.get_or_create(
                nome=outros_nome,
                defaults={'personalizada': True}
            )
            instance.categorias_doacao.add(categoria)


class SugestaoInstituicaoForm(forms.ModelForm):
    class Meta:
        model = SugestaoInstituicao
        fields = [
            'nome', 'descricao', 'tipo_instituicao',
            'endereco', 'cidade', 'estado', 'cep',
            'telefone', 'email', 'site',
            'categorias_doacao_texto',
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva brevemente a instituição...'}),
            'categorias_doacao_texto': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ex: Roupas, Alimentos, Brinquedos'}),
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo da instituição'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Ex: São Paulo'}),
            'estado': forms.TextInput(attrs={'placeholder': 'Ex: SP', 'maxlength': 2}),
            'cep': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(11) 99999-9999'}),
        }