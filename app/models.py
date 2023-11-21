# from django.db import models
from djongo import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.db.models.signals import post_save
from mail_notification.connection import MailConfig
from django.core.mail import send_mail


class CommonFields(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=138)
    
    class Meta:
        abstract = True


driver_and_hospital_status=(("pending",'PENDING'),("approved","APPROVED"),("rejected","REJECTED"))

class USER_Entry(CommonFields):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    phone_number = models.CharField(max_length=200)
    emergency_phone_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    user_type = models.CharField(max_length=20, default='user')
    location = models.JSONField((dict))


class Driver_Entry(CommonFields):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    name = models.CharField(max_length=200)
    hospital_name = models.CharField(max_length=200)
    license = models.ImageField(upload_to='users/driving', null=True, blank=True)
    vehicle_num = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=255)
    id_card = models.ImageField(upload_to='ID/driving', null=True, blank=True)
    hospital_license = models.ImageField(upload_to='hospital_license/driving', null=True, blank=True)
    status = models.CharField(choices=driver_and_hospital_status,max_length=100,blank=True, null=True,default="pending")
    user_type = models.CharField(max_length=20, default='driver')

class Hospital(CommonFields):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    license_img = models.ImageField(upload_to='users/hospital/', null=True, blank=True)
    landline = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    no_of_ambulances=models.CharField(max_length=3)
    established = models.CharField(max_length=255)
    supervisor_id_card=models.ImageField(upload_to='hospital_license/hospital/', null=True, blank=True)
    status = models.CharField(choices=driver_and_hospital_status,max_length=100,blank=True, null=True,default="pending")
    hospital_name = models.CharField(max_length=200)
    user_type = models.CharField(max_length=20, default='hospital')
    location = models.JSONField((dict))






@receiver(post_save, sender=Hospital)
def on_change(sender, instance: Hospital, **kwargs):
    email = instance.email
    if instance.status == 'approved':
        mail_subject='Congartulations Your Account Is Activated'
        
        demo=MailConfig(mail_user="harikishansuri1998@gmail.com",password="mita ypfc xjel khyy")
        demo.content_subtype='html'
        demo.send_mail(to_mail=email,subject=mail_subject,body='Congartulations Your Account Is Activated ,you can activate your now' )
        demo.close_conn()

    elif instance.status == 'rejected':
        mail_subject='Your Account Is Rejected'
        demo=MailConfig(mail_user="harikishansuri1998@gmail.com",password="mita ypfc xjel khyy")
        demo.content_subtype='html'
        demo.send_mail(to_mail=email,subject=mail_subject,body='Your Account Is Rejected' )
        demo.close_conn()


@receiver(post_save, sender=Driver_Entry)
def on_change(sender, instance: Driver_Entry, **kwargs):
    email = instance.email
    if instance.status == 'approved':
        mail_subject='Congartulations Your Account Is Activated'
        
        demo=MailConfig(mail_user="harikishansuri1998@gmail.com",password="mita ypfc xjel khyy")
        demo.content_subtype='html'
        demo.send_mail(to_mail=email,subject=mail_subject,body='Congartulations Your Account Is Activated ,you can activate your now' )
        demo.close_conn()

    elif instance.status == 'rejected':
        mail_subject='Your Account Is Rejected'
        demo=MailConfig(mail_user="harikishansuri1998@gmail.com",password="mita ypfc xjel khyy")
        demo.content_subtype='html'
        demo.send_mail(to_mail=email,subject=mail_subject,body='Your Account Is Rejected' )
        demo.close_conn()

 










