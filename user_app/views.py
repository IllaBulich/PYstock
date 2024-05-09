from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from item.models import Item, SalesItem

from user_app.forms import LoginForm, RegistrationForm, CustomPasswordResetForm, CustomSetPasswordForm, ProfileForm, UserInfoForm, UserPasswordForm


class CustomPasswordResetView(PasswordResetView):  
    template_name = 'user_app/password_reset.html'  
    email_template_name = 'user_app/password_reset_email.html'  
    form_class = CustomPasswordResetForm  
    success_url = reverse_lazy('user_app:password_reset_done')  


class CustomUserPasswordResetConfirmView(PasswordResetConfirmView):  
    template_name = 'user_app/password_reset_confirm.html'  
    success_url = reverse_lazy('user_app:password_reset_complete')  
    form_class = CustomSetPasswordForm


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user_app/login.html'
    extra_context = {'title': 'Авторизация на сайте'}

    def get_success_url(self):
        return reverse_lazy('home')


class CustomRegistrationView(CreateView):  
    form_class = RegistrationForm  
    template_name = 'user_app/signup.html'  
    extra_context = {'title': 'Регистрация на сайте'}  

    def get_success_url(self):  
        return reverse_lazy('user_app:login')  

    def form_valid(self, form):  
        user = form.save()  
        return super().form_valid(form)


class UserProfileView(TemplateView):  
    template_name = 'user_app/profile_page.html'  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        try:  
            user = get_object_or_404(User, username=self.kwargs.get('username'))  
        except User.DoesNotExist:  
            raise Http404("Пользователь не найден")  
        context['user_profile'] = user  
        
        context['user_item'] = Item.objects.filter(responsible = user).order_by('-id')[:3]
        context['user_selt_item'] = SalesItem.objects.filter(responsible = user).order_by('-id')[:3]
        context['title'] = f'Профиль пользователя {user}'  
        return context
    

class UserSettingsView(LoginRequiredMixin, TemplateView):  
    template_name = 'user_app/profile_settings_page.html'  

    def dispatch(self, request, *args, **kwargs):  
        if request.user == get_object_or_404(User, username=self.kwargs.get('username')):  
            return super().dispatch(request, *args, **kwargs)  
        else:  
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['user_info_form'] = UserInfoForm(instance=self.request.user)  
        context['user_password_form'] = UserPasswordForm(self.request.user)  
        context['user_profile_form'] = ProfileForm(instance=self.request.user.profile)
        context['title'] = f'Настройки профиля {self.request.user}'  
        return context  

    def post(self, request, *args, **kwargs):  
        if 'user_info_form' in request.POST:  
            user_info_form = UserInfoForm(request.POST, instance=request.user)  
            user_profile_form = ProfileForm(request.POST, request.FILES, instance=self.request.user.profile)
            if user_info_form.is_valid() and user_profile_form.is_valid():
                user_info_form.save()  
                user_profile_form.save()
                messages.success(request, 'Данные успешно изменены.')  
                return redirect('user_app:user_profile_settings', user_info_form.cleaned_data.get('username'))  
            else:  
                context = self.get_context_data(**kwargs)  
                context['user_info_form'] = user_info_form  
                context['user_profile_form'] = user_profile_form
                return render(request, self.template_name, context)  
            
        elif 'user_password_form' in request.POST:  
            form = UserPasswordForm(request.user, request.POST)  
            if form.is_valid():  
                form.save()  
                messages.success(request, 'Пароль успешно изменён.')  
                return self.get(request, *args, **kwargs)  
            else:  
                context = self.get_context_data(**kwargs)  
                context['user_password_form'] = form  
                return render(request, self.template_name, context)  
        else:  
            return self.get(request, *args, **kwargs)


class UserItemView(ListView):
    template_name = 'user_app/user_item_page.html'  
    context_object_name = 'items'  
    paginate_by = 10  

    def get_queryset(self): 
        try:  
            user = get_object_or_404(User, username=self.kwargs.get('username'))  
        except User.DoesNotExist:  
            raise Http404("Пользователь не найден")  
        
        return Item.objects.filter(responsible = user).order_by('-id')
         

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        try:  
            author = get_object_or_404(User, username=self.kwargs.get("username"))  
        except User.DoesNotExist:  
            raise Http404("Пользователь не найден")  
        context['author'] = author  
        context['title'] = f'Посты пользователя {author}'  
        return context
    

class UserSalesItemView(ListView):
    template_name = 'user_app/user_sales_item_page.html'  
    context_object_name = 'items'  
    paginate_by = 10  

    def get_queryset(self): 
        try:  
            user = get_object_or_404(User, username=self.kwargs.get('username'))  
        except User.DoesNotExist:  
            raise Http404("Пользователь не найден")  
        
        return SalesItem.objects.filter(responsible = user).order_by('-id')
         
    

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        try:  
            author = get_object_or_404(User, username=self.kwargs.get("username"))  
        except User.DoesNotExist:  
            raise Http404("Пользователь не найден")  
        context['author'] = author  
        context['title'] = f'Посты пользователя {author}'  
        return context