"""
This module defines the models for the care_profiles application.
Classes:
    Caregiver: A model representing a caregiver with fields for personal information.
    Patient: A model representing a patient with personal information and medical history.
Each class includes a __str__ method to return a string representation of the instance.
"""
from django.db import models
from django.core.exceptions import ValidationError
GENDER_CHOICES = [('Male', 'Male'),('Female', 'Female'),('Other', 'Other')]

class Caregiver(models.Model):
    """
    Represents a caregiver with personal and contact information.
    """
    TYPE_CHOICES = [('Familial', 'Familial'), ('Independent', 'Independent')]
    
    caregiver_id = models.BigAutoField(primary_key=True)
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    social_security_number = models.CharField(max_length=11)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    gender = models.CharField(
        null=True, blank=True, max_length=10, choices=GENDER_CHOICES)
    type = models.CharField(
        null=True, blank=True, max_length=25, choices=TYPE_CHOICES)
            
    date_of_hire = models.DateField(null=True, blank=True)
    date_of_termination = models.DateField(null=True, blank=True)
    
    def is_cna_certified(self):
        return self.caregivercert_set.filter(type='CNA', expiration_date__gt=models.functions.Now()).exists()
    
    def has_valid_cert(self):
        return self.caregivercert_set.filter(expiration_date__gt=models.functions.Now()).exists()
    
    def can_perform_task(self, task):
        if task.requires_cna_cert:
            return self.has_valid_cert()
        else:
            return True
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class CaregiverCert(models.Model):
    """
    Represents a caregiver certification with type and expiration date.
    """
    CERT_TYPE_CHOICES = [
        ('CNA', 'CNA'),
        ('TEMP', 'TEMP')]
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    type = models.CharField(
        null=False, max_length=15, choices=CERT_TYPE_CHOICES)
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.expiration_date}"
    
class Patient(models.Model):
    """
    Represents a patient with personal and contact information, and medical history.
    """
    patient_id = models.BigAutoField(primary_key=True)
    caregiver = models.ForeignKey(
        Caregiver, null=True, blank=True, on_delete=models.SET_NULL, default=None)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES)
    social_security_number = models.CharField(max_length=11)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    medical_history = models.TextField()
    language = models.CharField(max_length=100, null=True, blank=True)
    
    alternative_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class CarePlan(models.Model):
    """
    Represents a schedule for a caregiver & patient.
    """
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"Care Plan for {self.patient}"

class CarePlanTask(models.Model):
    FREQUENCY_CHOICES = [
        ('Once', 'Once'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
    ]
    
    DAY_OF_WEEK_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, related_name="tasks")
    task = models.ForeignKey('Task', on_delete=models.DO_NOTHING)
    notes = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=25, choices=FREQUENCY_CHOICES)
    active = models.BooleanField(default=True)

    time = models.TimeField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    day_of_week = models.CharField(choices=DAY_OF_WEEK_CHOICES,max_length=10, blank=True, null=True)

    
    def clean(self) -> None:
        if self.frequency == 'Once' and not self.date_time:
            raise ValidationError('Date and time are required for a one-time task.')
        
        if self.frequency == 'Weekly' and not self.day_of_week:
            raise ValidationError('Day of week is required for a weekly task.')
        
    # def clean(self):
    #     if self.is_completed and not self.time_spent:
    #         raise ValidationError('Time spent is required when the task is completed.')
    
class Task(models.Model):
    TYPE_CHOICES = [
        ('Homemaking', 'Homemaking'),
        ('Health Maintenance', 'Health Maintenance'),
        ('Personal Care', 'Personal Care')
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    reccomended_duration = models.DurationField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Task: {self.name} ({self.reccomended_duration})"
    
    def requires_cna_cert(self):
        return self.type == 'Personal Care'
    
class PatientEvent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_type = models.CharField(max_length=100)
    notes = models.TextField()
    
    def __str__(self):
        return f"{self.event_type} for {self.patient} on {self.event_date} at {self.event_time}"
    
    
class CarePlanTaskEvent(models.Model):
    """
    Represents an actual event for a CarePlanTask.
    """
    care_plan_task = models.ForeignKey(CarePlanTask, on_delete=models.CASCADE, related_name="events")
    event_date_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Event for {self.care_plan_task} on {self.event_date_time}"
    