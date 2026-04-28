from django.db import models
class LearningList(models.Model):
    name = models.CharField(max_length=100)
    CATEGORY_CHOICES = [
        ('book', 'Book'),
        ('course' , 'Course'),
        ('skill', 'Skill'),
        ('video' , 'Video'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    
class LearningItem(models.Model):
        learning_list = models.ForeignKey(LearningList,on_delete=models.CASCADE)
        title = models.CharField(max_length=200)
        url = models.URLField(blank=True)
        weight = models.IntegerField(default=3)
        is_active = models.BooleanField(default=False)
        is_done = models.BooleanField(default=False)

        def __str__(self):
            return self.title
         
class SpinResult(models.Model) :
            item = models.ForeignKey(LearningItem,on_delete=models.CASCADE)
            spun_at = models.DateTimeField(auto_now_add=True)
            OUTCOME_CHOICES = [
                ('in_progress' , 'In_Progress'),
                ('completed' , 'Completed'),
                ('skipped' , 'Skipped'),
            ]

            outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, default='in_progress')
            skip_reason = models.TextField(blank=True)
