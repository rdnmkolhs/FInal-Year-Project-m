from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Attendance
import json

@csrf_exempt
def add_student_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        name = data.get('name')

        obj, created = Student.objects.get_or_create(student_id=student_id, defaults={'name': name})
        if not created:
            obj.name = name
            obj.save()
        return JsonResponse({'status': 'success', 'message': 'Student synced'})

@csrf_exempt
def mark_attendance_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')

            student = Student.objects.get(student_id=student_id)
            Attendance.objects.create(student=student)

            return JsonResponse({'status': 'success', 'name': student.name})
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
