from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic.base import View, TemplateResponseMixin
from .forms import CommentForm,UserRegistrationForm, BackCallForm
from django.contrib.auth import authenticate, login
from .models import Category, Good, Comment, Images
from cart.forms import CartAddGoodForm
from django.contrib import messages
from .forms import ImageForm, GoodForm
from django.forms import modelformset_factory
# Регистрация пользователя
class UserRegistrationView(TemplateResponseMixin, View):
    template_name = 'registration/registration.html' 

    def get(self,request):
        registration_form = UserRegistrationForm()
        return self.render_to_response(
            {'registration_form': registration_form})

    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration=registration_form.save(commit=False)
            registration.set_password(
                registration_form.cleaned_data['password']
            )
            registration.save()
            authenticate_user = authenticate(
                username=registration_form.cleaned_data['username'],
                password=registration_form.cleaned_data['password']
            )
            login(request, authenticate_user)
            return redirect('my_site:index')
        return self.render_to_response(
            {'registration_form': registration_form})

class IndexView(TemplateResponseMixin, View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        search_text = request.GET.get('search_text', '')
        categories = Category.objects.all()
        goods = Good.objects.all()
        cart_product_form = CartAddGoodForm()
        if category:
            goods = Good.objects.filter(category=category)
        if search_text:
            goods = Good.objects.filter(title__icontains=search_text)
        return self.render_to_response({
            'categories': categories,
            'goods': goods,
            'cart_product_form': cart_product_form,
            'search_text': search_text
            })

class DetailView(TemplateResponseMixin, View):
    template_name = 'detail.html'

    def get(self, request, id):
        form = CommentForm()
        good = Good.objects.get(id=id)
        cart_product_form = CartAddGoodForm()
        comments = Comment.objects.filter(good=id)
        return self.render_to_response({'good': good,
            'cart_product_form': cart_product_form, 'comments':comments,'form':form})

    def post(self, request, id):
        good = Good.objects.get(id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.good = good
            form_obj.save()
            return redirect('my_site:detail', id)
        form = CommentForm()
        return self.render_to_response({'form': form})


class AboutView(TemplateResponseMixin, View):
    template_name = 'about.html'

    def get(self, request):
        return self.render_to_response({})

class ContactsView(TemplateResponseMixin, View):
    template_name = 'contacts.html'

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        form = BackCallForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Спасибо, наши менеджеры свяжутся с Вами в ближайшее время!')
            return redirect('my_site:contacts')
        form = BackCallForm()
        messages.add_message(request, messages.INFO, 'Что-то пошло не так!')
        return redirect('my_site:contacts')

def post(request):

    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        postForm = GoodForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())


        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                #this helps to not crash if the user
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(post=post_form, image=image)
                    photo.save()
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = GoodForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'index.html',
                  {'postForm': postForm, 'formset': formset})


