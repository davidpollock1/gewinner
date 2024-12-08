from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, modelformset_factory
from .models import Patient, Caregiver, CarePlan, CarePlanTaskEvent
from datetime import timedelta, datetime
from django.utils.timezone import now
from .forms import PatientForm, CaregiverForm, CarePlanForm, Task, CarePlanTask, CarePlanTaskForm, CarePlanTaskEventForm

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
    cert = caregiver.caregivercert_set.filter(expiration_date__gt=now()).first()
    if request.method == 'POST':
        form = CaregiverForm(request.POST, instance=caregiver)
        if form.is_valid():
            form.save()
            return redirect('care_profiles:caregiver_list')
    else:
        form = CaregiverForm(instance=caregiver)
        
    context = {'form': form, 'cert': cert}
    return render(request, 'care_profiles/caregiver_form.html', context)

def care_plan_list(request):
    care_plans = CarePlan.objects.all()
    care_plans.order_by('created_at')

    return render(request, 'care_profiles/care_plan_list.html', {'care_plans': care_plans})

def care_plan_create(request, *args, **kwargs):
    care_plan_form = CarePlanForm()
        
    if request.method == 'POST':
        care_plan_form = CarePlanForm(request.POST)

        if care_plan_form.is_valid():
            care_plan = care_plan_form.save()
            return redirect('care_profiles:care_plan_update', pk=care_plan.pk)

    if request.method == 'GET':
        care_plan_form = CarePlanForm()
    
    return render(request, 'care_profiles/care_plan_form.html', {
        'care_plan_form': care_plan_form,
    })
    
    
def care_plan_update(request, pk):
    care_plan = get_object_or_404(CarePlan, pk=pk)
    CarePlanTaskFormSet = inlineformset_factory(CarePlan, CarePlanTask, form=CarePlanTaskForm, extra=1, can_delete=True)
    task_formset = CarePlanTaskFormSet(request.POST, instance=care_plan)
        
    if request.method == 'POST':
        care_plan_form = CarePlanForm(request.POST, instance=care_plan)

        if care_plan_form.is_valid():
            care_plan = care_plan_form.save()
  
        if task_formset.is_valid():
            for form in task_formset:
                if form.instance.task_id is not None:
                    if not form.instance.pk:
                        care_plan_task = form.save()
                        try:
                            create_task_events(care_plan_task, care_plan)
                        except Exception as e:
                            print(f"Error creating task events: {e}")
                    else:
                        care_plan_task = form.save()
                
            return redirect(request.path)
    
    
                
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
    
def create_task_events(task, care_plan):
    # Once
    if(task.frequency == 'Once'):
        CarePlanTaskEvent(care_plan_task=task, event_date_time=task.date_time.date()).save()
    # Weekly
    if(task.frequency == 'Weekly'):
        # create a event for the task['day_of_week'] of the week for every week between the start and end date of the care_plan
        # get the start and end date of the care_plan
        start_date = care_plan.start_date
        end_date = care_plan.end_date
        # get the day of the week for the task
        day_of_week = task.day_of_week
        # get the date of the first day_of_week in the care_plan
        event_date = start_date
        while event_date <= end_date:
            if event_date.strftime('%A') == day_of_week:
                CarePlanTaskEvent(care_plan_task=task, event_date_time=event_date).save()
            event_date += timedelta(days=1)
        CarePlanTaskEvent(care_plan_task=task, event_date_time=task.date_time.date()).save()
        
    # Daily
    if(task.frequency == 'Daily'):
        # get the start and end date of the care_plan
        start_date = care_plan.start_date
        end_date = care_plan.end_date
        # get the date of the first day_of_week in the care_plan
        event_date = start_date
        while event_date <= end_date:
            CarePlanTaskEvent(care_plan_task=task, event_date_time=event_date).save()
            event_date += timedelta(days=1)
    return

# functions for schedule urls
def schedule_list(request):
    care_plans = CarePlan.objects.all()
    care_plans.order_by('created_at')
    return render(request, 'care_profiles/schedule_list.html', {'care_plans': care_plans})

def get_week_range(date):
    start_of_week = date - timedelta(days=date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return start_of_week, end_of_week

def schedule_update(request, pk):
    EventFormSet = modelformset_factory(CarePlanTaskEvent, form=CarePlanTaskEventForm, extra=0)
    
    current_date = now().date()
    if 'date' in request.GET:
        current_date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()

    start_of_week, end_of_week = get_week_range(current_date)

    if request.method == "POST":
        formset = EventFormSet(request.POST)
        if formset.is_valid():
            formset.save()  # Save all updated events at once
            return redirect("weekly_schedule")
    else:
        care_plan = get_object_or_404(CarePlan, pk=pk)
        events = get_event_tasks(care_plan, start_of_week, end_of_week)
        formset = EventFormSet(queryset=events)

    context = {
        'formset': formset,
        'days_of_week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'previous_week': (start_of_week - timedelta(days=7)).strftime('%Y-%m-%d'),
        'next_week': (start_of_week + timedelta(days=7)).strftime('%Y-%m-%d'),
    }
    return render(request, 'care_profiles/schedule_form.html', context)

def get_event_tasks(care_plan, start_of_week, end_of_week):
    events = CarePlanTaskEvent.objects.filter(care_plan_task__care_plan=care_plan,
                                              event_date_time__date__range=(start_of_week, end_of_week)).select_related('care_plan_task')
    # .select_related('care_plan_task__task')
    week_events = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    for event in events:
        if(event.care_plan_task.frequency == 'Daily'):
            # add event to every day of the week
            for day in week_events:
                week_events[day].append(event)
        elif(event.care_plan_task.frequency == 'Weekly'):
            #add event to the day of the week
            week_events[event.care_plan_task.day_of_week].append(event)
        elif(event.care_plan_task.frequency == 'Once'):
            # add event to the day
            if event.event_date_time >= start_of_week and event.event_date_time <= end_of_week:
                week_events[event.event_date_time.strftime('%A')].append(event)
    return events