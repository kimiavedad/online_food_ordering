from allauth.account.forms import SignupForm
from django import forms
from accounts.models import Address


class CustomerSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'آدرس ایمیل'
        self.fields['email'].label = 'ایمیل'
        self.fields['password1'].widget.attrs['placeholder'] = ''
        self.fields['password1'].label = 'رمز عبور'

        self.fields['city'] = forms.CharField(label="شهر")
        self.fields['street'] = forms.CharField(required=True, label="خیابان")
        self.fields['plaque'] = forms.CharField(required=False, label="پلاک")
        print(self.visible_fields())
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, request):
        print(self.cleaned_data)
        city = self.cleaned_data['city']
        street = self.cleaned_data['street']
        plaque = self.cleaned_data['plaque']

        user = super().save(request)
        user.role = 'مشتری'
        user.is_staff = False
        user.is_superuser = False
        user.save()

        Address.objects.create(customer=user, city=city, street=street, plaque=plaque, primary=True)
        return user

    def clean_plaque(self):
        cleaned_data = super().clean()
        plaque = cleaned_data.get("plaque")
        if int(plaque) <= 0:
            raise forms.ValidationError("پلاک نامعتبر")
        return plaque
