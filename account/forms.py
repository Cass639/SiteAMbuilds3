from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(
        label='Email ou Usuário',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-field',
                'placeholder': 'Informe o seu e-mail ou nome de usuário',
            }
        ),
    )
    password = forms.CharField(
        label='Senha',
        required=True,
        max_length=80,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-field',
                'placeholder': 'Informe a sua senha',
            }
        ),
    )


class RegisterForm(forms.Form):
    login = forms.CharField(
        label='Usuário',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-field',
                'placeholder': 'Crie um nome de usuário',
            }
        ),
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        max_length = 100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-field',
                'placeholder': 'Informe o seu e-mail',
            }
        ),
    )
    password = forms.CharField(
        label='Senha',
        required=True,
        max_length=80,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-field',
                'placeholder': 'Informe a sua senha',
            }
        ),
    )
    reenter_password = forms.CharField(
        label='Confirme a senha',
        required=True,
        max_length=80,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-field',
                'placeholder': 'Informe a senha novamente',
            }
        ),
    )
