from django.db import models

# Create your models here.


class Resume(models.Model):
  name = models.CharField(max_length=200)
  file = models.FileField(upload_to='resumes/')
  role = models.CharField(max_length=200,default="Fresher")
  job_description = models.TextField(default="")
  uploaded_at = models.DateTimeField(auto_now_add=True)
  score = models.IntegerField(null=True,blank=True)
  extracted_text = models.TextField(null=True,blank=True)
  found_skills = models.TextField(null=True,blank=True)
  missing_skills = models.TextField(null=True,blank=True)
  jd_skills = models.TextField(null=True,blank=True)
  matching_skills = models.TextField(null=True,blank=True)


  ai_summary = models.TextField(null=True,blank=True)
  ai_mathching_skills = models.TextField(null=True,blank=True)
  ai_missing_skills = models.TextField(null=True,blank=True)
  ai_suggestions = models.TextField(null=True,blank=True)
  

  def __str__(self):
    return self.name
  