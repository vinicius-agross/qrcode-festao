from allauth.account.forms import SignupForm
from django import forms
from qrcode.models import ClienteQtd


class CustomSignupForm(SignupForm):
    username = forms.CharField(
        max_length=14,
        label="CNPJ",
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o CNPJ'
        }),
        required=True
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Crie uma senha'
        }),
        required=True
    )

    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        }),
        required=True
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Verificar se o CNPJ está presente na tabela ClienteQtd
        if not ClienteQtd.objects.filter(cnpj=username).exists():
            raise forms.ValidationError(
                "CNPJ não encontrado na lista de clientes autorizados.")

        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        # Remove qualquer validação padrão, como comprimento mínimo
        if not password1:
            raise forms.ValidationError("Este campo é obrigatório.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Verifica se as senhas coincidem
        if password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return password2
