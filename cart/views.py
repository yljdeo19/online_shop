from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateResponseMixin
from my_site.models import Good
from .cart import Cart
from .forms import CartAddGoodForm

class CartAdd(View):

    def post(self, request, good_id):
        cart = Cart(request)
        good = get_object_or_404(Good, id=good_id)
        form = CartAddGoodForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(good=good,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
        return redirect('cart:cart_detail')

class CartRemove(View):

    def post(self, request, good_id):
        cart = Cart(request)
        good = get_object_or_404(Good, id=good_id)
        cart.remove(good)
        return redirect('cart:cart_detail')

class CartDetail(View, TemplateResponseMixin):
    template_name = 'card.html'

    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddGoodForm(initial={'quantity': item['quantity'],
                                'override': True})
        return self.render_to_response({'cart': cart})