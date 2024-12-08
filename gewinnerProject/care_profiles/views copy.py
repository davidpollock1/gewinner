from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from .models import Patient, Caregiver, CarePlan
from .forms import PatientForm, CaregiverForm, CarePlanForm, Task, CarePlanTask, CarePlanTaskForm

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'care_profiles/patient_list.html', {'patients': patients})

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('care_profiles:patient_list')
    else:
        form = PatientForm()
    return render(request, 'care_profiles/patient_form.html', {'form': form})

def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('care_profiles:patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'care_profiles/patient_form.html', {'form': form})

def caregiver_list(request):
    caregivers = Caregiver.objects.all()
    return render(request, 'care_profiles/caregiver_list.html', {'caregivers': caregivers})

def caregiver_create(request):
    if request.method == 'POST':
        form = CaregiverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('care_profiles:caregiver_list')
    else:
        form = CaregiverForm()
    return render(request, 'care_profiles/caregiver_form.html', {'form': form})

def caregiver_update(request, pk):
    caregiver = get_object_or_404(Caregiver, pk=pk)
    if request.method == 'POST':
        form = CaregiverForm(request.POST, instance=caregiver)
        if form.is_valid():
            form.save()
            return redirect('care_profiles:caregiver_list')
    else:
        form = CaregiverForm(instance=caregiver)
    return render(request, 'care_profiles/caregiver_form.html', {'form': form})

def care_plan_list(request):
    care_plans = CarePlan.objects.all()
    care_plans.order_by('created_at')

    return render(request, 'care_profiles/care_plan_list.html', {'care_plans': care_plans})

def care_plan_create(request, *args, **kwargs):
    care_plan_form = CarePlanForm()
    CarePlanTaskFormSet = inlineformset_factory(CarePlan, CarePlanTask, form=CarePlanTaskForm, extra=1, can_delete=True)
        
    if request.method == 'POST':
        care_plan_form = CarePlanForm(request.POST)
        task_formset = CarePlanTaskFormSet(request.POST)

        if care_plan_form.is_valid():
            care_plan = care_plan_form.save()
            task_formset.instance = care_plan
  
        if task_formset.is_valid():
            task_formset.save()
            return redirect('home')
    

    if request.method == 'GET':
        care_plan_form = CarePlanForm()
        task_formset = CarePlanTaskFormSet(instance=CarePlan())
    
    return render(request, 'care_profiles/care_plan_form.html', {
        'care_plan_form': care_plan_form,
        'task_formset': task_formset,
    })
    
    
def care_plan_update(request, pk):
    care_plan = get_object_or_404(CarePlan, pk=pk)
    CarePlanTaskFormSet = inlineformset_factory(CarePlan, CarePlanTask, form=CarePlanTaskForm, extra=1, can_delete=True)

    if request.method == 'POST':
        care_plan_form = CarePlanForm(request.POST, instance=care_plan)
        task_formset = CarePlanTaskFormSet(request.POST, instance=care_plan)

        if care_plan_form.is_valid() and task_formset.is_valid():
            care_plan = care_plan_form.save()
            task_formset.instance = care_plan
            task_formset.save()
            return redirect('care_profiles:care_plan_list')
        
    if request.method == 'GET':
        care_plan_form = CarePlanForm(instance=care_plan)
        task_formset = CarePlanTaskFormSet(instance=care_plan)

    return render(request, 'care_profiles/care_plan_form.html', {
        'care_plan_form': care_plan_form,
        'task_formset': task_formset,
    })
    
# view for care plan. should display the care plan and the tasks associated with it.
def care_plan_detail(request, pk):
    care_plan = get_object_or_404(CarePlan, pk=pk)
    care_plan_form = CarePlanForm(instance=care_plan)
    
    CarePlanTaskFormSet = inlineformset_factory(CarePlan, CarePlanTask, form=CarePlanTaskForm, extra=1, can_delete=True)
    task_formset = CarePlanTaskFormSet(instance=care_plan)
        
    return render(request, 'care_profiles/care_plan_form.html', {
        'care_plan_form': care_plan_form,
        'task_formset': task_formset,
    })