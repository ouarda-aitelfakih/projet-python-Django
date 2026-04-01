import calendar
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Holiday
from .forms import HolidayForm

@login_required
def holiday_list(request):
    # Récupérer le mois et l'année depuis l'URL (ex: ?month=3&year=2025)
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    # Navigation mois précédent / suivant
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    # Générer le calendrier du mois
    cal = calendar.monthcalendar(year, month)

    # Récupérer les holidays du mois
    holidays = Holiday.objects.filter(
        start_date__year=year,
        start_date__month=month
    ).order_by('start_date')

    # Créer un dict {jour: holiday} pour colorer les jours
    holiday_days = {}
    for h in Holiday.objects.all():
        start = h.start_date
        end = h.end_date if h.end_date else h.start_date
        current = start
        while current <= end:
            if current.year == year and current.month == month:
                holiday_days[current.day] = h
            current = date(current.year, current.month, current.day)
            # Passer au jour suivant
            import datetime
            current += datetime.timedelta(days=1)

    # Tous les holidays pour le tableau
    all_holidays = Holiday.objects.all().order_by('start_date')

    context = {
        'cal': cal,
        'month': month,
        'year': year,
        'month_name': calendar.month_name[month],
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'holiday_days': holiday_days,
        'holidays': all_holidays,
        'today': today,
    }
    return render(request, 'holiday/holiday_list.html', context)

@login_required
def holiday_create(request):
    form = HolidayForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('holiday_list')
    return render(request, 'holiday/holiday_form.html', {
        'form': form,
        'title': 'Ajouter un jour férié'
    })

@login_required
def holiday_update(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    form = HolidayForm(request.POST or None, instance=holiday)
    if form.is_valid():
        form.save()
        return redirect('holiday_list')
    return render(request, 'holiday/holiday_form.html', {
        'form': form,
        'title': 'Modifier un jour férié'
    })

@login_required
def holiday_delete(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.delete()
        return redirect('holiday_list')
    return render(request, 'holiday/holiday_confirm_delete.html', {'holiday': holiday})