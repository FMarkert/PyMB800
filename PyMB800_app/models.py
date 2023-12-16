from django.db import models

class BaseQuestion(models.Model):
    id = models.IntegerField(primary_key=True)
    src = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    question_text = models.TextField()
    comment = models.TextField(blank=True, null=True)
    casestudy = models.TextField(blank=True, null=True)


class MultipleChoice(BaseQuestion):
    items = models.JSONField()
    correct_answer = models.JSONField()
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer
    
class DropDown(BaseQuestion):
    items = models.JSONField()
    correct_answer = models.JSONField()
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer

class DragDropOrder(BaseQuestion):
    items = models.JSONField()
    correct_answer = models.JSONField()
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer
    
class DragDropPairs(BaseQuestion):
    pairs = models.JSONField()
    def generate_correct_answers(self):  # Erzeuge eine Liste mit den korrekten Antworten basierend auf den Paaren
        return [self.pairs]
    def check_answer(self, user_answer):
        return user_answer == self.pairs
