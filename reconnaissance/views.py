# Import des modules Django
from django.shortcuts import render 

from .forms import FacialRecognitionForm #formulaire pour le nom de l etudiant et leur image
from django.shortcuts import redirect
from django.contrib import messages

import numpy as np
from .models import RecognitionResult #un modele pour stocker l image et le nom et resultat pour la verification de l etudiant
from reconnaissance.calcule_embading import compare_images_with_label,extract_face #les deux fonctions de cnn et traitement d images


from mtcnn import MTCNN #un modele de l extraction de visage depuis une image
from django.contrib.auth import authenticate, login


#vue pour l interface login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
           
            return redirect('select_class')
        else:
            
            return render(request, 'login.html', {'error_message': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    else:
        return render(request, 'login.html')

#//////////////////////////////////////////////////////////////////


#vue pour l inerface pour selectionner la class et semester

from .forms import SelectClassForm
from django.urls import reverse
    
def select_class(request):
    if request.method == 'POST':
        form = SelectClassForm(request.POST)
        if form.is_valid():
            selected_class = form.cleaned_data['selected_class']
            selected_semester = form.cleaned_data['selected_semester']
           
            url = reverse('facial_recognition', kwargs={'selected_class': selected_class,'selected_semester':selected_semester})
            
            return redirect(url)
    else:
        form = SelectClassForm()
    return render(request, 'select_class.html', {'form': form})



#////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import base64
from django.core.files.base import ContentFile
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FacialRecognitionForm
from .models import RecognitionResult

from mtcnn import MTCNN

def facial_recognition(request, selected_class, selected_semester):
    valid_classes = ['MIP', 'BCG']
    if selected_class not in valid_classes:
        messages.error(request, "Invalid class selection.")
        return redirect('select_class')

    if request.method == 'POST':
        form = FacialRecognitionForm(request.POST, request.FILES)
        if form.is_valid():
            
            if selected_class == "MIP":
                if selected_semester == "S1":
                    embeddings_data = np.load(r'reconnaissance\fichier de projet\mip\s1_mip.npy', allow_pickle=True)
                elif selected_semester == "S2":
                    embeddings_data = np.load(r"reconnaissance\fichier de projet\mip\s2_mip.npy", allow_pickle=True)
            elif selected_class == "BCG":
                if selected_semester == "S1":
                    embeddings_data = np.load(r'reconnaissance\fichier de projet\bcg\s1_bcg.npy', allow_pickle=True)
                elif selected_semester == "S2":
                    embeddings_data = np.load(r'reconnaissance\fichier de projet\bcg\s2_bcg.npy', allow_pickle=True)
            
            embeddings = embeddings_data.item().get('embeddings')
            labels = embeddings_data.item().get("labels")

          
            label = form.cleaned_data['label']

            
            captured_image_data = request.POST.get('captured_image')
            if captured_image_data:
                format, imgstr = captured_image_data.split(';base64,')
                ext = format.split('/')[-1]
                image = ContentFile(base64.b64decode(imgstr), name='captured_image.' + ext)
                print("Captured image processed") 
            else:
              
                image = form.cleaned_data['image']
                print("Uploaded image processed") 

            print(type(image))

          
            if np.isin(label, labels):
               
                face = extract_face(image, MTCNN(), (160, 160))
                similarity_score = compare_images_with_label(embeddings, labels, face, label)

             
                recognition_result = RecognitionResult(label=label, image=image, similarity_score=similarity_score)
                recognition_result.save()

                
                return redirect('result_page')
            else:
                messages.error(request, "Label not found.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = FacialRecognitionForm()

    return render(request, 'facial_recognition.html', {'form': form})


#//////////////////////////////////////////////////////////////////////////////////////////////////


#vue pour la page result
def result_page(request):
    
    latest_result = RecognitionResult.objects.latest('id')  #
    if latest_result.similarity_score >= 0.5:
        admission_status = "L'étudiant est admis."
    else:
        admission_status = "L'étudiant n'est pas admis."
    return render(request, 'result_page.html', {'latest_result': latest_result,'admission_status': admission_status})


##################################################################################################33
import numpy as np
from .forms import ImporterRepertoireForm
from reconnaissance.x import load_faces,calculate_embeddings_with_labels,save_embeddings_and_labels
from django.conf import settings
import os

import zipfile



from django.http import JsonResponse

def importer_repertoire(request):
    if request.method == 'POST':
        form = ImporterRepertoireForm(request.POST, request.FILES)
        if form.is_valid():
            selected_class = form.cleaned_data['selected_class']
            selected_semester = form.cleaned_data['selected_semester']
            repertoire = request.FILES['repertoire']
            try:
                # Créer un répertoire temporaire pour extraire le contenu du fichier ZIP
                temp_dir = r'C:\hello\reconnaissance\tester'
                os.makedirs(temp_dir, exist_ok=True)
                print(temp_dir)
                # Enregistrer le fichier ZIP sur le système de fichiers
                repertoire_path = os.path.join(temp_dir, repertoire.name)
                with open(repertoire_path, 'wb+') as destination:
                    for chunk in repertoire.chunks():
                        destination.write(chunk)
                print(repertoire_path)
                
                with zipfile.ZipFile(repertoire_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                
                os.remove(repertoire_path)
                index_point= repertoire.name.rfind('.')
                if index_point==-1:
                    ok=repertoire.name
                else:
                    ok=repertoire.name[:index_point]
               
                print(ok)
                temp_dir = f'C:\\hello\\reconnaissance\\tester\\{ok}'
               
                X,Y = load_faces(temp_dir)
               
             
                messages.success(request, "Répertoire importé avec succès.")
                
                X_emb, label = calculate_embeddings_with_labels(X, Y)
                
                
                chemin = os.path.join(settings.MEDIA_ROOT, 'reconnaissance', 'new_data', 'nouveau.npy')
                
                # Sauvegarder les embeddings et les labels
                save_embeddings_and_labels(X_emb, label, chemin)
                
                if selected_class=="MIP":
                  if selected_semester == "S1":
                      path1=r'reconnaissance\fichier de projet\mip\s1_mip.npy'
                      os.remove(path1)
                      chemin1 = os.path.join(settings.MEDIA_ROOT, 'reconnaissance', 'fichier de projet', 'MIP.npy')
                      save_embeddings_and_labels(X_emb, label, chemin1)
                    
                    
                    
                  elif selected_semester == "S2":
                      path1=r'reconnaissance\fichier de projet\mip\s2_mip.npy'
                      os.remove(path1)
                      chemin1 = os.path.join(settings.MEDIA_ROOT, 'reconnaissance', 'fichier de projet', 'MIP.npy')
                      save_embeddings_and_labels(X_emb, label, chemin1)

                elif selected_class=="BCG":
                  if selected_semester== "S1":
                      path1=r'reconnaissance\fichier de projet\bcg\s1_bcg.npy'
                      os.remove(path1)
                      chemin1 = os.path.join(settings.MEDIA_ROOT, 'reconnaissance', 'fichier de projet', 'MIP.npy')
                      save_embeddings_and_labels(X_emb, label, chemin1)

                    

                  elif selected_semester == "S2":
                      path1=r'reconnaissance\fichier de projet\bcg\s2_bcg.npy'
                      os.remove(path1)
                      chemin1 = os.path.join(settings.MEDIA_ROOT, 'reconnaissance', 'fichier de projet', 'MIP.npy')
                      save_embeddings_and_labels(X_emb, label, chemin1)

                    

            
                
                return JsonResponse({'progress': 100})
                
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
                
    else:
        form = ImporterRepertoireForm()
    
    return render(request, 'importer_repertoire.html', {'form': form})

