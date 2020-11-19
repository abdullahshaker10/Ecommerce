from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView
from .models import Order, Product, OrderItem, ShippingAddress
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm
from django.contrib.auth import views as auth_views
from .forms import ShippingAddressForm
from .serializers import OrderSerializer, ItemSerializer
from rest_framework.generics import UpdateAPIView


class SignUpView(CreateView):
    template_name = 'store/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


class LoginView(auth_views.LoginView):
    template_name = 'store/login.html'
    success_url = 'store'


class LogoutView(auth_views.LogoutView):
    template_name = 'store/logout.html'


class Store(ListView):
    login_url = '/login/'
    redirect_field_name = 'store'
    template_name = 'store/store.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        if customer.is_authenticated:
            order, created = Order.objects.get_or_create(
                customer=customer, compleated=False)
            context['order_id'] = order.id
            context['num_items'] = order.get_cart_items
        context['products'] = self.queryset
        return context


class Cart(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        order, created = Order.objects.get_or_create(
            customer=customer, compleated=False)
        order_items = order.orderitem_set.all()
        context['num_items'] = order.get_cart_items
        context['items'] = order_items
        context['total'] = order.get_cart_total
        return context


class CheckOut(LoginRequiredMixin, FormView):
    template_name = 'store/checkout.html'
    form_class = ShippingAddressForm
    success_url = '/'

    def form_valid(self, form):
        address = form.cleaned_data['address']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']

        customer = self.request.user
        order, created = Order.objects.get_or_create(
            customer=customer, compleated=False)

        new_shipping_address, created = ShippingAddress.objects.get_or_create(
            order=order, customer=customer, address=address, city=city, state=state, zipcode=zipcode)

        new_shipping_address.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        order, created = Order.objects.get_or_create(
            customer=customer, compleated=False)
        order_items = order.orderitem_set.all()
        context['num_items'] = order.get_cart_items
        context['items'] = order_items
        context['total'] = order.get_cart_total
        context['shipping'] = order.shipping

        return context


class AddtoChart(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        customer = self.request.user
        product_id = int(data['productId'])
        order, created = Order.objects.get_or_create(
            customer=customer, compleated=False)

        product = Product.objects.get(id=product_id)

        new_item, created = OrderItem.objects.get_or_create(
            order=order, product=product)

        new_item.quantity = new_item.quantity + 1
        new_item.save()
        return super(AddtoChart, self).update(request, *args, **kwargs)


class UpdateItem(UpdateAPIView):
    serializer_class = ItemSerializer
    queryset = OrderItem.objects.all()

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = int(data['productId'])
        action = data['action']
        item_id = data['item']

        customer = self.request.user

        order, created = Order.objects.get_or_create(
            customer=customer, compleated=False)
        product = Product.objects.get(id=product_id)

        new_item, created = OrderItem.objects.get_or_create(
            order=order, product=product, id=item_id)

        if action == 'remove':
            new_item.quantity = new_item.quantity - 1

        else:
            new_item.quantity = new_item.quantity + 1

        if new_item.quantity <= 0:
            new_item.delete()
        else:
            new_item.save()

        return super(UpdateItem, self).update(request, *args, **kwargs)
