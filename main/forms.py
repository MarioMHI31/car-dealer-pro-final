from django import forms
from .models import Car, CarImage

class CarForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Car
        fields = [
            "brand", "model", "year", "price", "mileage",
            "engine", "horsepower", "fuel_type", "car_body",
            "location", "phone_number", "description", "main_image",
            "featured"
        ]

        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'horsepower': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            if self.cleaned_data.get("images"):
                for image in self.files.getlist("images"):
                    CarImage.objects.create(car=instance, image=image)
        return instance


