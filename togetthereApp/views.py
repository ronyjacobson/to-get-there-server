from django.http import *
from .forms import *
from django.shortcuts import get_object_or_404,get_list_or_404, render
import json
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from togetthereApp import forms

DEBUG = True

def index(request):
    return HttpResponse("Hello, world. You're at the ToGetThere index.")

def spByCategoryList(request, category_id):
    sps = list(SP.objects.filter(category = category_id))
    results = [sp.as_json(False) for sp in sps]
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json")

def spView(request, sp_id):
    sp = get_object_or_404(SP,pk=sp_id)
    return HttpResponse(json.dumps(sp.as_json(True), ensure_ascii=False), content_type="application/json")


def addSp(request):
    if (request.method == 'GET') & (DEBUG):
        sp_form = SPForm()
        address_form = AddressForm()
        return render(request, 'ToGetThere/addSP.html', {
            'address_form': address_form,
            'sp_form':sp_form})
    elif request.method == 'POST':
        sp_form = SPForm(request.POST)
        address_form = AddressForm(request.POST)

        if (sp_form.is_valid() and address_form.is_valid()):
            name_from_form = sp_form.cleaned_data['name']
            desc_from_form = sp_form.cleaned_data['desc']
            category_from_form = sp_form.cleaned_data['category']
            lon_from_form = sp_form.cleaned_data['longitude']
            lat_from_form = sp_form.cleaned_data['latitude']
            phone_from_form = sp_form.cleaned_data['phone']
            discount_from_form = sp_form.cleaned_data['discount']
            website_from_form = sp_form.cleaned_data['website']
            city_from_form = address_form.cleaned_data['city']
            street_from_form = address_form.cleaned_data['street']
            streetnum_from_form = address_form.cleaned_data['street_num']
            if (street_from_form.city.pk != city_from_form.pk):
               raise Http404('Street does not match city')
               return


            formAddress, created = Address.objects.get_or_create(
                street_num= streetnum_from_form,
                street= street_from_form,
                city = city_from_form)

            formsp = SP.objects.filter(name= name_from_form, sp_address=formAddress.pk)
            if not formsp.exists():
                formsp = SP.objects.create(
                    name= name_from_form,
                    desc= desc_from_form,
                    sp_address=formAddress,
                    longitude=lon_from_form,
                    latitude=lat_from_form,
                    phone=phone_from_form,
                    discount= discount_from_form,
                    category=category_from_form,
                    website=website_from_form)
                return HttpResponseRedirect(reverse('ToGetThere:spView', args=(formsp.pk,)))
            
            # SP exists: redirect to update
            else:

                return HttpResponseRedirect(reverse('ToGetThere:spView', args=(formsp[0].pk,)))
        
        else:
            raise Http404(str(sp_form.errors) + '\n' + str(address_form.errors) + '\n')


#TODO
def rankSp(request, sp_id):
    reviews = get_list_or_404(Review, sp=sp_id)
    results = [rev.as_json() for rev in reviews]
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json")
   


def spReviews(request, sp_id):
    reviews = get_list_or_404(Review, sp=sp_id)
    results = [rev.as_json() for rev in reviews]
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json")

def spAddReview(request, sp_id):

    if (request.method == 'GET') & (DEBUG):
        form = AddReviewForm()
        return render(request, 'ToGetThere/addReview.html', {'form': form,})
    elif request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            formTitle = form.cleaned_data['title']
            formContent = form.cleaned_data['content']
            formUser = form.cleaned_data['user']
            formSp = SP.objects.get(pk = sp_id)
            review = Review(title = formTitle, content= formContent, user = formUser, sp= formSp)
            review.save()
            return HttpResponseRedirect(reverse('ToGetThere:spView', args=(review.sp.pk,)))
        else:
            raise Http404(form.errors)


def editSP(request, sp_id):
    sp = get_object_or_404(SP, pk = sp_id)
    address = sp.sp_address
    if (request.method == 'GET') & (DEBUG):
        sp_form = SPForm(instance= sp)
        address_form = AddressForm(instance= address)
        return render(request, 'ToGetThere/addSP.html', {
            'address_form': address_form,
            'sp_form':sp_form})

    elif (request.method == 'POST'):
        sp_form = SPForm(request.POST, instance= sp)
        address_form = AddressForm(request.POST, instance= address)

        if (sp_form.is_valid() and address_form.is_valid()):
            city_from_form = address_form.cleaned_data['city']
            street_from_form = address_form.cleaned_data['street']
            if (street_from_form.city.pk != city_from_form.pk):
               raise Http404('Street does not match city, street: '+ str(street_from_form.city.pk)+', city: '+ str(city_from_form.pk))
               return

            editedSP = sp_form.save(commit = False)
            editedAddress = address_form.save()
            editedSP.sp_address = editedAddress
            editedSP.save()
            return HttpResponseRedirect(reverse('ToGetThere:spView', args=(editedSP.pk,)))

        else:
            raise Http404(str(sp_form.errors) + '\n' + str(address_form.errors) + '\n')

def userProfile(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    return HttpResponse(json.dumps(user.as_json(), ensure_ascii=False), content_type="application/json")

def editProfile(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    if (request.method == 'GET') & (DEBUG):
        user_form = UserForm(instance= user)
        return render(request, 'ToGetThere/editProfile.html', {
            'user_form': user_form})

    elif (request.method == 'POST'):
        user_form = UserForm(request.POST, instance= user)
        if user_form.is_valid():
            editedUser = user_form.save()
            return HttpResponseRedirect(reverse('ToGetThere:user_profile', args=(editedUser.pk,)))

        else:
            raise Http404(str(user_form.errors))

def streetByCity(request, city_id):
    streets = get_list_or_404(Street, city_id = city_id)
    results = [street.as_json() for street in streets]
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json")

def cities(request):
    cities = get_list_or_404(City)
    results = [city.as_json() for city in cities]
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json")