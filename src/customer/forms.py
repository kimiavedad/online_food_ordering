from django.contrib.auth.forms import UserChangeForm
from django import forms
from accounts.models import Customer


class CustomerUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    email = forms.EmailField(disabled=True)

    class Meta:
        model = Customer
        fields = ("email",)


# class ScheduledActionForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         self.firme = kwargs.pop('firme')
#         super(ScheduledActionForm, self).__init__(*args, **kwargs)
#         self.fields['node_ids'].queryset = Node.objects.filter(firm_id=self.firme.id)
#
#
#     date = forms.DateTimeField()
#     firm = forms.ModelChoiceField(
#         queryset=Firme.objects.all())  # why do you want a list of all firms here? Or do you want a single object?
#     node_ids = forms.ModelMultipleChoiceField(queryset=Node.objects.none()), widget = forms.CheckboxSelectMultiple)
#
#     class Meta:
#         model = ScheduledAction
#         fields = [
#             'date',
#             'firm',
#             'node_ids'
#         ]
