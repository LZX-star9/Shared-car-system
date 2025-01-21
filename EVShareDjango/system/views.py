from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from system.models import Payment


# Create your views here.


@login_required
def process_payment(request):
    if request.method == 'POST':
        order_type = request.POST.get('order_type')
        if order_type == 'recharge':
            recharge_amount = request.POST.get('amount')
            remark = request.POST.get('remark')
            try:
                recharge_amount = int(recharge_amount)
                if recharge_amount > 0:
                    user = request.user
                    user.balance += recharge_amount
                    user.save()
                    Payment.objects.create(customer=user, amount=recharge_amount,remark=remark)
                    return redirect('index')
                else:
                    error_message = "Please enter a valid amount greater than 0."
            except ValueError:
                error_message = "Please enter a valid number."

            return render(request, 'checkout.html', {'error_message': error_message})
        elif order_type == 'card1':
            user = request.user
            user.cardType = 1
            one_month_later = datetime.now() + timedelta(days=30)
            user.cardExpiry = one_month_later.date()
            user.save()
            remark = request.POST.get('remark')
            Payment.objects.create(customer=user, amount=10,remark=remark)
            return redirect('index')
        elif order_type == 'card2':
            user = request.user
            user.cardType = 2
            one_month_later = datetime.now() + timedelta(days=30)
            user.cardExpiry = one_month_later.date()
            user.save()
            remark = request.POST.get('remark')
            Payment.objects.create(customer=user, amount=15, remark=remark)
            return redirect('index')
    else:
        order_type = request.GET.get('order_type')
        remark = ""
        should_pay = 0
        if order_type == 'recharge':
            remark = "Recharge account"
        elif order_type == 'card1':
            remark = "buy a Plus Card"
            should_pay=10
        elif order_type == 'card2':
            remark = "buy a Super Plus Card"
            should_pay=15
        return render(request, 'checkout.html', {'order_type': order_type,'remark':remark,'should_pay':should_pay})