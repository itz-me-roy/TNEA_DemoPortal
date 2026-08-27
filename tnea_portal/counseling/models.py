from django.db import models
from django.contrib.auth.models import User

COMMUNITY_CHOICES = [
    ('OC', 'OC - Open Category'),
    ('BC', 'BC - Backward Class'),
    ('BCM', 'BCM - Backward Class Muslim'),
    ('MBC', 'MBC/DNC - Most Backward Class'),
    ('SC', 'SC - Scheduled Caste'),
    ('SCA', 'SCA - Scheduled Caste Arunthathiyar'),
    ('ST', 'ST - Scheduled Tribe'),
]
COLLEGE_TYPE_CHOICES = [
    ('GOVT', 'Government'),
    ('GOVT_AIDED', 'Government Aided'),
    ('UNIV_DEPT', 'University Department'),
    ('SELF_FIN', 'Self-Financing'),
]

class College(models.Model):
    college_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    college_type = models.CharField(max_length=20, choices=COLLEGE_TYPE_CHOICES, default='SELF_FIN')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.college_code} - {self.name}"

class Branch(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Cutoff(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='cutoffs')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='cutoffs')
    community = models.CharField(max_length=5, choices=COMMUNITY_CHOICES)
    cutoff_mark = models.DecimalField(max_digits=6, decimal_places=2)
    year = models.PositiveIntegerField(default=2025)

    class Meta:
        unique_together = ('college', 'branch', 'community', 'year')
        ordering = ['-cutoff_mark']

    def __str__(self):
        return f"{self.college.college_code} / {self.branch.code} / {self.community} / {self.year}: {self.cutoff_mark}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    community = models.CharField(max_length=5, choices=COMMUNITY_CHOICES, default='OC')
    phone = models.CharField(max_length=15, blank=True)
    cutoff_mark = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user.get_username()

class Application(models.Model):
    STATUS_CHOICES = [
        ('SAVED', 'Saved'),
        ('APPLIED', 'Applied'),
        ('ALLOTTED', 'Allotted'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    cutoff = models.ForeignKey(Cutoff, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SAVED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'cutoff')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} -> {self.cutoff}"