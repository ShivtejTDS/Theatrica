from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    principal = models.CharField(max_length=100, blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_schools")  

    def __str__(self):
        return self.name


class Trainer(models.Model):
    user = models.OneToOneField("core.CustomUser", on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="trainers", null=True, blank=True)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')]
    )
    selfie = models.ImageField(
        upload_to="attendance_selfies/",
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )  
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.date} - {self.status} - {self.selfie} - {self.latitude} - {self.longitude}"
    


class Syllabus(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LogBook(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.DateField()
    topic_covered = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.date} - {self.topic_covered}"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students", null=True, blank=True)

    def __str__(self):
        return self.name
    
class Class(models.Model):
    name = models.CharField(max_length=100)  
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='classes')
    subject = models.CharField(max_length=100)
    schedule = models.DateTimeField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')]
    )

    def __str__(self):
        return f"{self.student.name} - {self.class_obj.name} - {self.date} - {self.status}"


class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    attendance_percentage = models.FloatField(default=0.0)
    grades = models.CharField(max_length=5, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')])
    feedback = models.TextField(blank=True, null=True)

    def update_attendance(self):
        total_classes = StudentAttendance.objects.filter(student=self.student, class_obj=self.class_obj).count()
        attended_classes = StudentAttendance.objects.filter(student=self.student, class_obj=self.class_obj, status="Present").count()
        if total_classes > 0:
            self.attendance_percentage = (attended_classes / total_classes) * 100
            self.save()

    def __str__(self):
        return f"{self.student.name} - {self.class_obj.name} - {self.grades}"

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Emergency Leave', 'Emergency Leave'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)  
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)  
    type_of_leave = models.CharField(max_length=20, choices=LEAVE_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="leave_requests", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.type_of_leave} - {self.status}"

    
class Assignment(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.class_obj.name}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/') 
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Graded', 'Graded')],
        default='Pending'
    )
    def __str__(self):
        return f"{self.student.name} - {self.assignment.title} - {self.submitted_on}"
