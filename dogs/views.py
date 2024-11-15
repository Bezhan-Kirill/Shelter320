from django.shortcuts import render


from dogs.models import Category, Dog

def index(request):
    context = {
        'objects_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


def categories(request):
        context = {
            'objects_list': Category.objects.all(),
            'title': 'Питомник - Все наши поролы'
        }
        return render(request, 'dogs/categories.html', context)

def category_dogs(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собваки породы - {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html')