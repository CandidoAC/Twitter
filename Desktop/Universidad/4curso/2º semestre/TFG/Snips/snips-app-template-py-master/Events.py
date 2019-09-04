#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Evento import Event
from datetime import datetime
from Database import Database
from apscheduler.schedulers.background import BackgroundScheduler

class Snips(object):
    def __init__(self):
        file=__import__('action-Actions')
        self.usr=""
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Madrid'})
        self.scheduler1 = BackgroundScheduler({'apscheduler.timezone': 'Europe/Madrid'})
        self.Database=Database()
        self.scheduler.start()
        self.scheduler1.start()
        self.Database.connectDB()
        self.Database.createTable()
        self.Database.insertUsers('default')
        self.usr=self.Database.UserActive()
        if(not self.usr):
            self.Database.changeActiveUsers('default')

        LEvent=self.Database.eventActives()
        for e in LEvent:
            if(e.rep):
                Repeticion=e.when[e.when.index(' ')+1:]
                veces=int(e.when[:e.when.index(' ')])
                if(not e.fecha is None):
                    date=e.fecha
                else:
                    fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    date=datetime.strptime(fecha,"%Y-%m-%d %H:%M:%S")

                if(Repeticion=='dia'):
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion cada '+str(veces)+' dias,'+e.med+','+e.user,year=date.year,month=date.month,day=str(date.day)+'/'+str(veces),hour=date.hour,minute=date.minute, replace_existing=True, args=['default',e,True])
                elif(Repeticion=='mes'):
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion '+str(veces)+' meses ,'+e.med+','+e.user,year=date.year,month=str(date.month)+'/'+str(veces),day=date.day,hour=date.hour,minute=date.minute, replace_existing=True, args=['default',e,True]) 
                elif(Repeticion=='semana'):
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion' +str(veces)+' semanas,'+e.med+','+e.user,year=date.year,month=date.month,day=str(date.day)+'/'+str(7*veces),hour=date.hour,minute=date.minute, replace_existing=True, args=['default',e,True]) 
                elif(Repeticion=='hora'):
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion '+str(veces)+' horas,'+e.med+','+e.user,year=date.year,month=date.month,day=date.day,hour=str(date.hour)+'/'+str(veces),minute=date.minute, replace_existing=True, args=['default',e,True]) 
                elif(Repeticion=='desayuno'):#HORA-1
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion Desayuno'+','+e.med+','+e.userr,year=date.year,month=date.month,day=date.day,hour='8/1',minute=0, replace_existing=True, args=['default',e,True]) 
                elif(Repeticion=='comida'):#HORA-1
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion Comida'+','+e.med+','+e.user,year=date.year,month=date.month,day=date.day,hour='13/1',minute=0, replace_existing=True, args=['default',e,True]) 
                elif(Repeticion=='cena'): #HORA-1
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion Cena'+','+e.med+','+e.user,year=date.year,month=date.month,day=date.day,hour='20/1',minute=0, replace_existing=True, args=['default',e,True]) 
                else:
                    self.scheduler.add_job(file.recordatorio, 'cron',id='Repeticion semanal cada '+Repeticion+','+e.med+','+e.user,day_of_week=self.dia_sem(Repeticion),year=date.year,month=date.month,day=date.day,hour=date.hour,minute=date.minute, replace_existing=True, args=['default',e,True]) 
                
                if(datetime.strptime(e.fecha,"%Y-%m-%d %H:%M:%S")>datetime.now()):  
                    self.scheduler1.add_job(file.recordatorioTomar, 'interval', seconds=20,id='fecha evento:'+e.fecha+'recordando tomar '+e.med+' a '+e.user,args=[e,'default'])
            else:
                if(not e.fecha is None):
                    date=e.fecha
                else:
                    fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    date=datetime.strptime(fecha,"%Y-%m-%d %H:%M:%S")
                if(datetime.strptime(e.fecha,"%Y-%m-%d %H:%M:%S")<datetime.now()):
                    self.scheduler.add_job(file.recordatorio, 'date', run_date=date,id=e.fecha+','+e.med+','+e.user,args=['default',e,False])
                else:
                    self.scheduler1.add_job(file.recordatorioTomar, 'interval', seconds=20,id='recordando tomar '+e.med+' a '+e.user,args=[e,'default'])
    def dia_sem(self,i):
        switcher={
            'Lunes':0,
            'Martes':1,
            'Miercoles':2,
            'Jueves':3,
            'Viernes':4,
            'Sabado':5,
            'Domingo':6
            }
        return switcher.get(i,str(i))
                
    def addEvent(self,event):
        self.Database.insertEvent(datetime.now(),event)

    def addUser(self,user):
        self.Database.insertUsers(user)

    def existUser(self,user):   
        return self.Database.ExistsUser(user)

    def Incrementar(self,event):
        self.Database.IncrementarVeces(event)

    def FinishEvent(self,e):
        self.Database.FinishedEvent(e)

    def insertUsers(self,User):
        self.Database.insertUsers(User)

    def changeActiveUsers(self,User):
        self.Database.changeActiveUsers(User)
        self.usr=User

    def NingunaVez(self,e):
        self.Database.NingunaVeces(e)
    
    def UserActive(self):
        self.Database.UserActive()

    def eventActive(self,e):
        if(e.rep):
            self.Database.EventIsActive(e.med,None,e.user,e.rep,e.when[e.when.index(' ')+1:],int(e.when[:e.when.index(' ')]))
        else:
            self.Database.EventIsActive(e.med,e.fecha,e.user,e.rep,None,None)

    def borrarEvento(self,e):
        if(e.rep):
            self.Database.deleteEvent(e.med,None,e.user,e.rep,e.when[e.when.index(' ')+1:],int(e.when[:e.when.index(' ')]))
        else:
            self.Database.deleteEvent(e.med,e.fecha,e.user,e.rep,None,None)
