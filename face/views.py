# Import des modules Django
from django.shortcuts import render
from django.http import HttpResponse

# Vue pour la page d'accueil
def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil de notre application de reconnaissance faciale pour les examens !")
# views.py

def scan_student(request):
    if request.method == 'POST':
        # Récupérer l'ID de l'étudiant et la photo soumise par le formulaire
        student_id = request.POST.get('student_id')
        student_photo = request.FILES.get('student_photo')

        # Effectuer le traitement de la photo ici

        # Rediriger vers une autre vue ou afficher un message de succès
        return HttpResponse("Photo soumise avec succès !")

    else:
        # Si la méthode HTTP n'est pas POST, afficher le formulaire
        return render(request, 'scan_student.html')

