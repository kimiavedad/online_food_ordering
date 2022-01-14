from allauth.account.forms import SignupForm
from django import forms
from accounts.models import Address


class CustomerSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['city'] = forms.CharField(label="شعبه")
        self.fields['street'] = forms.CharField(required=True)
        self.fields['plaque'] = forms.CharField(required=False,)

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

        Address.objects.create(city=)
        b_obj = Branch.objects.create(manager=user, name=branch, restaurant=restaurant_obj, category=category,
                                      address=address, description=description, primary=primary)
        print(b_obj.name)
        return user

    def clean_branch(self):
        cleaned_data = super().clean()
        branch = cleaned_data.get("branch")
        restaurant = cleaned_data.get("restaurant")
        primary = cleaned_data.get('primary')

        if Branch.objects.filter(restaurant__name=restaurant, name=branch).exists():
            raise forms.ValidationError("این شعبه قبلا ثبت شده است.")

        return branch

    def clean_primary(self):
        cleaned_data = super().clean()
        restaurant = cleaned_data.get("restaurant")
        primary = cleaned_data.get('primary')

        print(Branch.objects.filter(restaurant__name=restaurant, primary=True).exists(), "shobe asli hast")
        print(primary, "inam zade asli")
        if Branch.objects.filter(restaurant__name=restaurant, primary=True).exists() and primary:
            raise forms.ValidationError("برای این رستوران قبلا شعبه اصلی ثبت شده است.")
        return primary
