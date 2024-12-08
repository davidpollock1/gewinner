"""
FORMS
"""
from django import forms
from .models import CarePlan, CarePlanTask, Task, Caregiver, Patient, CarePlanTaskEvent, CaregiverCert

class PatientForm(forms.ModelForm):
    caregiver = forms.ModelChoiceField(queryset=Caregiver.objects.all(), required=False)

    class Meta:
        model = Patient
        fields = ['caregiver','first_name','middle_name','last_name','date_of_birth','gender',
                  'social_security_number','email','phone_number','address_line_1','address_line_2',
                  'zip_code','country','state','city','medical_history','language','alternative_id']

class CaregiverForm(forms.ModelForm):
    class Meta:
        model = Caregiver
        fields = ['first_name','middle_name','last_name','date_of_birth','social_security_number','email',
                  'phone_number','address_line_1','address_line_2','zip_code','country','state','city','gender',
                  'type','date_of_hire','date_of_termination']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']

class CarePlanTaskForm(forms.ModelForm):
    task = forms.ModelChoiceField(queryset=Task.objects.all(), required=False)
    
    class Meta:
        model = CarePlanTask
        fields = ['care_plan','task','frequency','active','time','date_time','day_of_week']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CarePlanForm(forms.ModelForm):
    class Meta:
        model = CarePlan
        fields = ['caregiver', 'patient', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
# form for CarePlanTaskEvent. This form is used to alter existing CarePlanTaskEvents only. I may be updating more than one CarePlanTaskEvent at a time.
class CarePlanTaskEventForm(forms.ModelForm):
    class Meta:
        model = CarePlanTaskEvent
        fields = '__all__'
        widgets = {
            'is_completed': forms.CheckboxInput(),
        }