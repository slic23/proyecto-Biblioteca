from catalog.models import Reservation, lector
from django.contrib.auth.models import User

print("--- Debugging Reservations ---")
all_res = Reservation.objects.all()
print(f"Total reservations: {all_res.count()}")

pending_res = Reservation.objects.filter(estado__exact="pendiente")
print(f"Pending reservations (exact match 'pendiente'): {pending_res.count()}")

# Check values of 'estado' for all reservations to see if there are case/whitespace issues
for r in all_res:
    print(f"Reservation {r.pk}: estado='{r.estado}' (User: {r.usuario_reservador})")

print("--- End Debug ---")
