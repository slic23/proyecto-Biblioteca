from datetime import datetime, date, timedelta

# Fecha y hora actual
ahora = datetime.now()
print(ahora)  # 2026-02-13 15:30:45.123456

# Solo fecha actual
hoy = date.today()
print(hoy)  # 2026-02-13

# Crear fechas manualmente
fecha_evento = datetime(2026, 3, 1, 18, 0)
print(fecha_evento)  # 2026-03-01 18:00:00

# Sumar días
manana = hoy + timedelta(days=1)
print(manana)  # 2026-02-14

# Restar fechas → timedelta
diferencia = fecha_evento - ahora
print(diferencia)  # 16 days, 2:29:15.123456

# Acceder a días y segundos de timedelta
print(diferencia.days)  # 16
print(diferencia.seconds)  # 88755 (horas*3600 + minutos*60 + segundos)


"""
fecha_creacion = models.DateTimeField(auto_now_add=True)  # Se pone solo al crear, nunca cambia
fecha_modificacion = models.DateTimeField(auto_now=True)  # Se actualiza cada vez que se guarda el objeto

"""