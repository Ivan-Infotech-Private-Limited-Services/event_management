import django
from django.http import JsonResponse
from .models import *
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def OrganizersView(request):
    if request.method == 'GET':
        data = json.loads(serializers.serialize("json", organizers.objects.all()))
        f=[]
        for i in data:
          f.append(i['fields'])
        return JsonResponse(f, safe=False, status=200)
    elif request.method == 'POST':
       try:
          body = json.loads(request.body.decode("utf-8"))
          newrecord = organizers.objects.create(
            name=body['name'],
            email=body['email'],
            phone = body['phone'],
            website = body['website'],
            image_url = body['image_url'],
         )
          data = json.loads(serializers.serialize('json', [newrecord]))
          return JsonResponse({"message": "Organizer created successfully","data":data[0]['fields']}, status=201)
       except django.db.utils.IntegrityError:
         return JsonResponse({"message":"UNIQUE constraint failed"}, status = 400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def OrganizersViewTwo(request, id):
   if request.method == 'PUT':
      body = json.loads(request.body.decode("utf-8"))
      organizers.objects.filter(pk=id).update(
         name=body['name'],
         email=body['email'],
         phone = body['phone'],
         website = body['website'],
         image_url = body['image_url'],
      )
      newrecord = organizers.objects.filter(pk=id)
      data = json.loads(serializers.serialize('json', newrecord))
      return JsonResponse({"message": "Organizer updated successfully","data":data[0]['fields']}, status=201)
   elif request.method == 'GET':
      newrecord = organizers.objects.filter(pk=id)
      data = json.loads(serializers.serialize('json', newrecord))
      return JsonResponse(json.loads(data[0]['fields']), safe=False, status=200)
   else:
      return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def EventView(request):
   if request.method == 'GET':
        data = json.loads(serializers.serialize("json", events.objects.all()))
        f=[]
        for i in data:
          f.append(i['fields'])
        return JsonResponse(f, safe=False, status=200)
   elif request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        newrecord = events.objects.create(
            name=body['name'],
            description=body['description'],
            organizer = body['organizer'],
            start_date_time = body['start_date_time'],
            end_date_time = body['end_date_time'],
            location = body['location'],
            image_url = body['image_url'],
        )
        data = json.loads(serializers.serialize('json', [newrecord]))
        return JsonResponse({"message": "Event created successfully","data":data[0]['fields']}, status=201)
   else:
        return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def EventViewTwo(request, id):
   if request.method == 'PUT':
      body = json.loads(request.body.decode("utf-8"))
      events.objects.filter(pk=id).update(
         name=body['name'],
         description=body['description'],
         organizer = body['organizer'],
         start_date_time = body['start_date_time'],
         end_date_time = body['end_date_time'],
         location = body['location'],
         image_url = body['image_url'],
      )
      newrecord = events.objects.filter(pk=id)
      data = json.loads(serializers.serialize('json', newrecord))
      return JsonResponse({"message": "Event updated successfully","data":data[0]['fields']}, status=201)
   elif request.method == 'GET':
      newrecord = events.objects.filter(pk=id)
      data = json.loads(serializers.serialize('json', newrecord))
      return JsonResponse(json.loads(data[0]['fields']), safe=False, status=200)
   else:
      return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def TicketsView(request):
   if request.method == 'GET':
        data = json.loads(serializers.serialize("json", tickets.objects.all()))
        f=[]
        for i in data:
          f.append(i['fields'])
        return JsonResponse(f, safe=False, status=200)
   elif request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        newrecord = tickets.objects.create(
            event=body['event'],
            ticket_type=body['ticket_type'],
            price = body['price'],
            discount_price = body['discount_price'],
            stock_count = body['stock_count'],
            availability_status = body['availability_status'],
        )
        data = json.loads(serializers.serialize('json', [newrecord]))
        return JsonResponse({"message": "Ticket created successfully","data":data[0]['fields']}, status=201)
   else:
       return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def TicketsViewTwo(request, id):
   if request.method == 'PUT':
      body = json.loads(request.body.decode("utf-8"))
      tickets.objects.filter(pk=id).update(
         event=body['event'],
         ticket_type=body['ticket_type'],
         price = body['price'],
         discount_price = body['discount_price'],
         stock_count = body['stock_count'],
         availability_status = body['availability_status'],
      )
      newrecord = tickets.objects.filter(pk=id)
      data = json.loads(serializers.serialize('json', newrecord))
      return JsonResponse({"message": "Ticket updated successfully","data":data[0]['fields']}, status=201)
   elif request.method == 'GET':
      newrecord = tickets.objects.filter(pk=id)
      data = json.loads(serializers.serialize('json', newrecord))
      return JsonResponse(json.loads(data[0]['fields']), safe=False, status=200)
   else:
      return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def Force_Delete(request, id):
    if request.method == 'DELETE':
        organizer = organizers.objects.get(pk=id)
        has_children_event = events.objects.filter(organizer=organizer).exists()
        
        if not has_children_event:
            organizers.objects.filter(pk=id).delete()
            newrecord = organizers.objects.all()
            data = json.loads(serializers.serialize('json', newrecord))
            return JsonResponse({"message": "Organizer deleted successfully", "data": data[0]['fields']}, safe=False, status=204)
        
        else:
            event_list = events.objects.filter(organizer=organizer)
            for event in event_list:
                has_children_ticket = tickets.objects.filter(event=event).exists()
                
                if has_children_ticket:
                    ticket_list = tickets.objects.filter(event=event)
                    
                    for ticket in ticket_list:
                        ticket.delete()
                event.delete()
            organizers.objects.filter(pk=id).delete()
            
            newrecord = organizers.objects.all()
            data = json.loads(serializers.serialize('json', newrecord))
            return JsonResponse({"message": "Organizer and all associated events and tickets deleted successfully", "data": data[0]['fields']}, safe=False, status=204)