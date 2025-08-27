from django.shortcuts import render, redirect
from account.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def login(request):
    form = LoginForm()


    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            nome_usuario = form["login"].value().strip()
            senha = form["password"].value().strip()

            if nome_usuario == "" or senha == "":
                messages.error(request, "Todos os campos são obrigatórios!")
                return render(request, "conta/login.html", {"form": form})

            credenciais_usuario = auth.authenticate(
                request,
                username=nome_usuario,
                password=senha,
            )

            if credenciais_usuario == None:
                messages.error(request, "Usuário ou senha inválidos!")
                return render(request, "account/login.html", {"form": form})

            auth.login(request, credenciais_usuario)
            return redirect("index")

    return render(request, "account/login.html", {"form": form})


def logout(request):
    auth.logout(request)
    return redirect("login")


def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            nome_usuario = form["login"].value().strip()
            email_usuario = form["email"].value().strip()
            senha = form["password"].value().strip()
            confirma_senha = form["reenter_password"].value().strip()

            if (
                nome_usuario == ""
                or email_usuario == ""
                or senha == ""
                or confirma_senha == ""
            ):
                return redirect("register")

            if senha != confirma_senha:
                messages.error(request, "As senhas não coincidem!")
                return render(request, "conta/register.html", {"form": form})

            user_exists = User.objects.filter(username=nome_usuario).exists()
            email_exists = User.objects.filter(email=email_usuario).exists()

            if user_exists:
                messages.error(request, "Já existe um usúario com este nome")
                return render(request, "conta/register.html", {"form": form})

            if email_exists:
                messages.error(request, "Esse e-mail já está cadastrado!")
                return render(request, "conta/register.html", {"form": form})

            new_user = User.objects.create_user(
                username=nome_usuario,
                email=email_usuario,
                password=senha,
            )

            new_user.save()

            messages.success(request, "Usuário cadastrado com sucesso! Faça login para continuar.")
            return redirect("login")

    return render(request, "account/register.html", {"form": form})

def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            messages.error(request, "Informe o e-mail para redefinir a senha.")
            return render(request, "account/password_reset.html")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Nenhum usuário encontrado com esse e-mail.")
            return render(request, "account/password_reset.html")

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(f"/account/reset/{uid}/{token}/")

        subject = "Redefinição de senha"
        message = f"Olá,\n\nClique no link abaixo para redefinir sua senha:\n{reset_link}\n\nSe você não solicitou, ignore este e-mail."
        from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else None
        send_mail(subject, message, from_email, [email], fail_silently=False)

        messages.success(request, "Um e-mail foi enviado com instruções para redefinir sua senha.")
        return redirect("login")

    return render(request, "account/password_reset.html")