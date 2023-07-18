from django.shortcuts import render
from django.views.generic.base import View, TemplateResponseMixin
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

class OrderCreate(View, TemplateResponseMixin):
    template_name = 'orders/order/create.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm()
        return self.render_to_response({
            'cart': cart,
            'form': form
            })

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        good=item['good'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})