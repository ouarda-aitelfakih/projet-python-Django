from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import TimeTable
from school.decorators import admin_required, teacher_required
from subjects.models import Subject
from teacher.models import Teacher

@login_required
def timetable_list(request):
    import json
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    hours = ['08:00', '09:00', '10:00', '11:00', '12:00', 
             '13:00', '14:00', '15:00', '16:00', '17:00']

    # Organiser par jour pour le tableau liste
    timetable_by_day = {}
    for day in days:
        timetable_by_day[day] = TimeTable.objects.filter(
            day=day).select_related('subject', 'teacher')

    # Organiser par jour ET heure pour la grille
    grid = {}
    for day in days:
        grid[day] = {}
        for hour in hours:
            grid[day][hour] = None

    all_entries = TimeTable.objects.all().select_related('subject', 'teacher')
    for entry in all_entries:
        hour_key = entry.start_time.strftime('%H:00')
        if hour_key in hours:
            grid[entry.day][hour_key] = entry

    # JSON pour export
    data = []
    for t in all_entries:
        data.append({
            'id': t.pk,
            'day': t.day,
            'subject': t.subject.name,
            'teacher': f"{t.teacher.first_name} {t.teacher.last_name}",
            'start_time': str(t.start_time),
            'end_time': str(t.end_time),
            'room': t.room,
        })

    return render(request, 'timetable/list_timetable.html', {
        'timetable_by_day': timetable_by_day,
        'days': days,
        'hours': hours,
        'grid': grid,
        'timetable_json': json.dumps(data, ensure_ascii=False, indent=2),
    })

@teacher_required
def timetable_create(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    error = None

    if request.method == 'POST':
        day = request.POST.get('day')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room = request.POST.get('room', '')

        if start_time >= end_time:
            error = "L'heure de fin doit être après l'heure de début !"
        else:
            TimeTable.objects.create(
                day=day,
                subject_id=subject_id,
                teacher_id=teacher_id,
                start_time=start_time,
                end_time=end_time,
                room=room
            )
            return redirect('timetable_list')

    return render(request, 'timetable/add_timetable.html', {
        'subjects': subjects,
        'teachers': teachers,
        'error': error,
        'days': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
    })

@teacher_required
def timetable_update(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    error = None

    if request.method == 'POST':
        day = request.POST.get('day')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room = request.POST.get('room', '')

        if start_time >= end_time:
            error = "L'heure de fin doit être après l'heure de début !"
        else:
            timetable.day = day
            timetable.subject_id = subject_id
            timetable.teacher_id = teacher_id
            timetable.start_time = start_time
            timetable.end_time = end_time
            timetable.room = room
            timetable.save()
            return redirect('timetable_list')

    return render(request, 'timetable/edit_timetable.html', {
        'timetable': timetable,
        'subjects': subjects,
        'teachers': teachers,
        'error': error,
        'days': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
    })

@admin_required
def timetable_delete(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        return redirect('timetable_list')
    return render(request, 'timetable/timetable_confirm_delete.html', {'timetable': timetable})

# Vue JSON pour Visual Timetabling (bonus)
@login_required
def timetable_json(request):
    import json
    timetables = TimeTable.objects.all().select_related('subject', 'teacher')
    data = []
    for t in timetables:
        data.append({
            'id': t.pk,
            'day': t.day,
            'subject': t.subject.name,
            'teacher': f"{t.teacher.first_name} {t.teacher.last_name}",
            'start_time': str(t.start_time),
            'end_time': str(t.end_time),
            'room': t.room,
        })

    response = JsonResponse(data, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 2
    })
    # ← Cette ligne force le téléchargement
    response['Content-Disposition'] = 'attachment; filename="timetable.json"'
    return response