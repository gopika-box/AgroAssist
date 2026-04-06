from django.shortcuts import render
from .utils.model_loader import predict_disease
from django.core.files.storage import FileSystemStorage

# Create your views here.

def disease_predict(request):
    context = {}
    
    # Define the list once here
    supported_plants = [
        'Apple', 'Blueberry', 'Cherry', 'Corn', 'Grape', 'Orange', 
        'Peach', 'Pepper', 'Potato', 'Raspberry', 'Soybean', 
        'Squash', 'Strawberry', 'Tomato'
    ]
    
    # Default context so the sidebar shows even before upload
    context['supported_plants'] = supported_plants

    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)

        predicted_class, confidence, remedy = predict_disease(image_path)

        # Update context with results
        context.update({
            'prediction': predicted_class,
            'confidence': confidence,
            'remedy': remedy,
            'image_url': fs.url(filename),
        })
        
    return render(request, 'farmers/plant_upload.html', context)