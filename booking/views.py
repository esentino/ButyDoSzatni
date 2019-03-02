import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse

from booking.models import Room, Reservation

def search(request):
    if request.method == 'GET':
        result = Room.objects.all()
        name = request.GET.get('name')
        capacity = request.GET.get('capacity')
        projector = request.GET.get('projector')
        date = request.GET.get('date')
        current_date = None
        if name is not None:
            result = result.filter(name=name)
        if capacity is not None:
            result = result.filter(capacity__gte=capacity)
        if projector is not None:
            result = result.filter(projector=True)
        if date is not None:
            current_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        rooms = []
        for room in result:
            if current_date is None:
                rooms.append(room)
            else:
                reservations = room.reservation_set.filter(date = current_date)
                if len(reservations) == 0:
                    rooms.append(room)


        ctx= {'rooms':rooms}
        return render(request, 'search.html', context=ctx)



def add_reservation(request, room_id):
    if request.method == 'POST':
        date = request.POST.get('date')
        current_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        comment = request.POST.get('comment')
        today = datetime.date.today()
        reservations = Reservation.objects.filter(date=date).filter(room=room_id)
        if len(reservations) > 0:
            return HttpResponse("Sala jest zajęta na dany dzień")
        if current_date < today:
            return HttpResponse("Na cebulaka tylko do przodu rezerwujemy")
        new_reservation = Reservation()
        new_reservation.date =current_date
        new_reservation.room_id=room_id
        new_reservation.comment=comment
        new_reservation.save()
        return redirect(reverse('main-page'))

def room(request, id):
    current_room = get_object_or_404(Room, pk=id)
    today = datetime.date.today()
    reservations = Reservation.objects.filter(room=current_room, date__gte=today).order_by('date')
    # reservations = current_room.reservation_set.filter(date__gte=today)
    ctx = {
        'room': current_room,
        'reservations': reservations
    }
    return TemplateResponse(request, 'room_details.html', context=ctx)

def delete_room(request, id):
    try:
        room = Room.objects.get(pk=id)
        room.delete()
        return redirect('main-page')
    except ObjectDoesNotExist:
        return HttpResponse('Nie ma takiej sali to jej Ci nie usunę')

def modify_room(request, id):
    # room = Room.objects.get(pk=id)
    room = get_object_or_404(Room, pk=id)
    if request.method == 'GET':

        ctx = {
            'room': room
        }
        return TemplateResponse(request, 'modify_room.html',
                                context=ctx)
    elif request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        room.name = name
        room.capacity = capacity
        if projector is not None:
            room.projector = True
        else:
            room.projector = False
        room.save()
        return redirect(reverse('main-page'))

def add_room(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'add_room.html')
    elif request.method == 'POST':
        # Pobranie danych z formularza
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        # Tworzenie nowego pokoju
        new_room = Room()
        new_room.name = name
        new_room.capacity = capacity
        if projector is not None:
            new_room.projector = True
        else:
            new_room.projector = False
        # Zapis do bazy danych pokoju
        new_room.save()
        return redirect(reverse('main-page'))

def strona_glowna(request):
    rooms = Room.objects.all()
    ctx={
        "rooms": rooms
    }
    return TemplateResponse(request, 'main.html', context=ctx)

def strona_test(request):
    return TemplateResponse(request, 'base.html')

