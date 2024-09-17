from django.db import models
from django.contrib.auth.models import User

class MedicalTerm(models.Model):
    concept_id = models.CharField(max_length=255, primary_key=True)
    tree_number = models.CharField(max_length=255)

    def __str__(self):
        return self.concept_id
    
class SelectedSuggestion(models.Model):
    data = models.ForeignKey(MedicalTerm, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data.concept_id}"
