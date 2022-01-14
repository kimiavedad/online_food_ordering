from allauth.account.forms import SignupForm
from django import forms
from online_food_ordering.models import Category, Branch, Restaurant


class ManagerSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['restaurant'] = forms.CharField(required=True, )
        self.fields['branch'] = forms.CharField(label="شعبه")
        self.fields['address'] = forms.CharField(required=True)
        self.fields['description'] = forms.CharField(required=False,
                                                     widget=forms.Textarea(
                                                         attrs={'placeholder': "توضیحات شعبه", })
                                                     )
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.all())

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['primary'] = forms.BooleanField(required=False)

    def save(self, request):
        print(self.cleaned_data)
        restaurant = self.cleaned_data['restaurant']
        branch = self.cleaned_data['branch']
        address = self.cleaned_data['address']
        primary = self.cleaned_data['primary']
        category = self.cleaned_data['category']
        description = self.cleaned_data['description']

        user = super().save(request)
        print(user.is_superuser)
        user.role = 'مدیر رستوران'
        user.is_staff = True
        user.save()

        restaurant_obj, created = Restaurant.objects.get_or_create(name=restaurant)
        print(branch)
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
