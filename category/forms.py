from django import forms
from leads.models import Lead, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "category",
        )


class CategoryForm2(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            "name",
        )
