from django import forms


from .models import Product, Category, RFQ


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['created'].widget = DateTimeInput()
        self.fields["created"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

    class Meta:
        model = Product
        fields = ('category', 'name', 'slug', 'image', 'description', 'price', 'available', 'created')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class DateInput(forms.DateInput):
    input_type = 'date'


class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
        fields = ('Category_Type', 'Brand', 'Material_description', 'Location', 'Attachment')
