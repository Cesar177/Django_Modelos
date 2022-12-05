from django.db import models
import datetime

# Create your models here.
# Vamos a crear 4 modelos
# 1. Person
# 2. Student
# 3. Teacher
# 4. ClassRoom

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    born_date = models.DateField()


    class Meta:
        abstract = True


class ClassRoom(models.Model):
    name = models.CharField(max_length=2)
    start_time = models.TimeField()

    def __str__(self):
        return self.name + " - " + str(self.start_time)

    class Meta:
        db_table = 'classrooms'



class Student(Person):
    classroom_id = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    grade_lab = models.FloatField(default=0.0)
    grade_exam = models.FloatField(default=0.0)
    grade_final = models.FloatField(default=0.0)

    class Meta:
        db_table = 'students'

class StudentProxy(Student):
    class Meta:
        ordering = ["-id"]
        proxy = True

    def average(self):
        return self.grade_exam*0.1 + self.grade_lab*0.6 + self.grade_final*0.3



class Teacher(Person):
    salary = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)

    class Meta:
        db_table = 'teachers'

class TeacherProxy(Teacher):
    class Meta:
        proxy = True
    
    def get_bonnus(self):
        return self.salary + self.rating*100


# Tarea
class Evaluacion(models.Model):
    hour_and_date = models.DateTimeField(default=datetime.datetime.now())
    course = models.CharField(max_length=30)
    evaluator = models.CharField(max_length=50)

    class Meta:
        abstract = True

class Examen_Final(Evaluacion):
    duration_of_the_exam = models.IntegerField(default=0)
    number_of_questions = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    class Meta:
        db_table = "final_examens"

    def score_for_question(self):
        return self.number_of_questions / self.total_score
    
class Proyecto(Evaluacion):
    project_topic = models.CharField(max_length=100)
    number_of_groups = models.IntegerField(default=0)

    class Meta:
        db_table = "proyects"


class ProyectoProxy(Proyecto):
    class Meta:
        ordering = ['project_topic']
        proxy = True