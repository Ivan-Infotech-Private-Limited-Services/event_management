from django.db import models

class organizers(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, null=True)
    phone = models.CharField(max_length=50, unique=True, db_index=True, null=True)
    website = models.URLField(null=True)
    image_url = models.URLField()
    def __str__(self):
        return self.name

class events(models.Model):
    name = models.CharField(max_length=50), 
    description = models.TextField(max_length= 250, blank=True)
    organizer = models.ForeignKey(organizers, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    location = models.CharField(max_length=150, null=True)
    image_url = models.URLField()
    def __str__(self):
        return self.name

class tickets(models.Model):
    ticket_type = (
        ('General','General'),
        ('VIP', 'VIP'),
        ('Student', 'Student'),
        ('Complimentary', 'Complimentary')
    )
    availability_status = (
        ('Available', 'Available'),
        ('Sold Out', 'Sold Out'),
        ('Limited', 'Limited')
    )
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    ticket_type =  models.CharField(max_length= 250, blank=True, choices= ticket_type) 
    price = models.FloatField(null=True) 
    discount_price = models.FloatField( blank=True, default=0)
    stock_count = models.IntegerField(null=True)
    availability_status = models.CharField(max_length= 250, blank=True, choices= availability_status)
    def __str__(self):
        return self.name