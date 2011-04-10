from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from core.models import *
from logging import debug as log
import urllib2, urllib

def index(request):
    return render_to_response('web/index.html', context_instance=RequestContext(request))

def menu(request):
    #Used for XHTML validation testing
    # login(request, authenticate(username='user42', password='user42'))
    template_vars = {}
    template_vars['category_list'] = []
    template_vars['menu_list_bycat'] = {}
    for cat in Category.objects.all():
        template_vars['category_list'].append(cat.__str__())
        item = Menu.objects.filter(category=cat)
        template_vars['menu_list_bycat'][cat.__str__()] = []
        for child in item:
            template_vars['menu_list_bycat'][cat.__str__()].append({ 'item':model_to_dict(child), 'children':MenuItem.objects.filter(item=child) })

    if request.user.is_authenticated():
        delivery = False
        if request.method=="POST":
            if 'delivery' in request.POST and request.POST['delivery'] in (True, 'on', 'true'):
                delivery = True
            order = Order(user=request.user, delivery=delivery)
            order.save()
            for (k,v) in request.POST.iteritems():
                try:
                    itm = int(k)
                    qty = int(v)
                    order.addItem(itm, qty)
                except ValueError as strerror:
                    pass
            messages.success(request, 'Your order '+str(order)+' has been saved, time to checkout')##TODO: Remove for production
            return render_to_response('web/checkout.html', {'order': order, 'phones': Phone.objects.filter(user=request.user.id), 'addresses': Address.objects.filter(user=request.user.id)}, context_instance=RequestContext(request))
    return render_to_response('web/menu.html', template_vars, context_instance=RequestContext(request))

def checkout(request):
    if request.user.is_authenticated():
        if request.method=="POST":
            phone = Phone.objects.get(user=request.user, pk=request.POST.get('phone_number'))
            address = Address.objects.get(user=request.user, pk=request.POST.get('address'))
            orders = Order.objects.filter(user=request.user.id, completed=False).order_by('-date')
            order = orders[0]
            r = call_auth(
                unicode(order.total),
                request.POST.get('card_num'),
                request.POST.get('exp_date'),
                request.POST.get('card_code'),
                address.postalcode,       #if request.POST.get('zip_code') else address.zip_code,
                order.id,
                request.user.first_name,
                request.user.last_name,
                address.address1 +" "+ address.address2,
                address.city, 
                address.state,
                address.country,
                phone.number,
                request.user.email,
                request.user.id,
                request.META['REMOTE_ADDR'],
            )
            if r.split('|')[0] == '1':
                #Sucess, authorized
                transaction_id = (r.split('|')[6])
                messages.success(request, 'Payment '+transaction_id+' Authorized - %s'% (r.split('|')[3]))
                c = call_capture(transaction_id)
                if c.split('|')[0] == '1':
                    #Sucess, payment processed
                    order.completed=True
                    order.save()
                    messages.success(request, 'Payment Processed - %s'% (c.split('|')[3]))
                    return HttpResponseRedirect(reverse('web:index'))
                elif c.split('|')[0] == '2':
                    #Failed, transaction declined
                    messages.error(request, 'Transaction Declined - %s'% (c.split('|')[3]))
                    return HttpResponseRedirect(reverse('web:checkout'))
                else:
                    #Held for Review, transaction error
                    #Failed, transaction error
                    error = "Error Processing Payment - %s" % (c.split('|')[3])
                    messages.error(request, error)
                    return HttpResponseRedirect(reverse('web:checkout'))
            elif r.split('|')[0] == '2':
                #Failed, transaction declined
                messages.error(request, '%s'% (r.split('|')[3]))
                return HttpResponseRedirect(reverse('web:index'))
            else:
                #Held for Review, transaction error
                #Failed, transaction error
                error = "%s - Error Processing Payment" % (r.split('|')[3])
                messages.error(request, error)
                return HttpResponseRedirect(reverse('web:index'))
        else:
            return render_to_response('web/checkout.html', {'phones': Phone.objects.filter(user=request.user.id), 'addresses': Address.objects.filter(user=request.user.id)}, context_instance=RequestContext(request))  
    return render_to_response('web/checkout.html', context_instance=RequestContext(request))



#---------------------------Authorize.net---------------------------#
#---Credit to---http://stackoverflow.com/questions/1637902/python-django-which-authorize-net-library-should-i-use---#
URL = 'https://test.authorize.net/gateway/transact.dll'
API = {'x_login':'9Evr7R3bd',
'x_tran_key':'62Fn32JMXZuW39hg', 'x_method':'CC', 'x_type':'AUTH_ONLY',
'x_delim_data':'TRUE', 'x_duplicate_window':'10', 'x_delim_char':'|',
'x_relay_response':'FALSE', 'x_version':'3.1'}

def call_auth(amount, card_num, exp_date, card_code, zip_code, orderid, first_name, last_name, address, city, state, country, phone, email, userid, request_ip):
    #---Call authorize.net and get a result dict back---#
    payment_post = API
    payment_post['x_amount'] = amount
    payment_post['x_card_num'] = card_num
    payment_post['x_exp_date'] = exp_date
    payment_post['x_card_code'] = card_code
    payment_post['x_zip'] = zip_code
    payment_post['x_invoice_num'] = orderid
    payment_post['x_first_name'] = first_name
    payment_post['x_last_name'] = last_name
    payment_post['x_address'] = address
    payment_post['x_city'] = city
    payment_post['x_state'] = state
    payment_post['x_country'] = country
    payment_post['x_phone'] = phone
    payment_post['x_email'] = email
    payment_post['x_cust_id'] = userid
    payment_post['x_customer_ip'] = request_ip
    payment_post['x_merchant_descriptor'] = str('Dine and Dash')
    payment_post['x_description'] = str('Online Order')
    payment_request = urllib2.Request(URL, urllib.urlencode(payment_post))
    r = urllib2.urlopen(payment_request).read()
    return r

def call_capture(transaction_id): # r.split('|')[6] we get back from the first call, trans_id
    capture_post = API
    capture_post['x_type'] = 'PRIOR_AUTH_CAPTURE'
    capture_post['x_trans_id'] = transaction_id
    capture_request = urllib2.Request(URL, urllib.urlencode(capture_post))
    r = urllib2.urlopen(capture_request).read()
    return r
#---------------------------Authorize.net---------------------------#

def register(request):
    next = reverse('core:index')
    if 'next' in request.GET and request.GET['next'].strip() != '':
        next = request.GET['next']

    errors = {}
    fields = { 'uname':'', 'passwd':'', 'fname':'', 'lname':'', 'email':'', 'notes':'' }
    if request.method == 'POST':
        contact = None
        fields['uname'] = request.POST['username'].strip()
        fields['passwd'] = request.POST['password']
        fields['fname'] = request.POST['first_name'].strip()
        fields['lname'] = request.POST['last_name'].strip()
        fields['email'] = request.POST['email'].strip()
        fields['notes'] = request.POST['notes'][0:2000]
        
        if len(fields['uname']) < 4:
            errors['username'] = 'Usernames must be atleast 4 characters long'
        elif len(fields['uname']) != len(fields['uname'].strip(' ,.<>{}[]:;"\'!@#$%^&*()')):
            errors['username'] = 'Usernames may not contain spaces or any of ,.<>{}[]:;"\'!@#$%^&*()'
        elif User.objects.filter(username=fields['uname']).count() != 0:
            errors['username'] = 'That username is already taken'
        #Password
        if len(fields['passwd']) < 8:
            errors['password'] = 'Passwords mush be at least 8 characters long'
        #First name
        if len(fields['fname']) <= 0:
            errors['fname'] = 'I know you must have a first name'
        #Last name
        if len(fields['lname']) <= 0:
            errors['lname'] = 'I know you must have a last name'
        #Email
        try:
            validate_email(fields['email'])
        except ValidationError, err:
            errors['email'] = str(err.messages[0])

        if len(errors) == 0:
            try:
                contact = UserProfile.objects.create_user(fields['uname'], fields['email'], fields['passwd'])
                contact.user.first_name = fields['fname']
                contact.user.last_name = fields['lname']
                contact.notes = fields['notes']
            except IntegrityError:
                errors['username'] = fields['uname'] + ' is not a valid username!'
            #Account created, lets login
            if contact is not None:
                contact.save()
                user = authenticate(username=fields['uname'], password=fields['passwd'])
                login(request, user)
                messages.success(request, 'You have been registered as ' + fields['uname'] + '.')
                return HttpResponseRedirect(reverse('web:profile') + '?next=' + next)
    return render_to_response('web/register.html', { 'errors':errors, 'auth_next':next, 'fields':fields }, context_instance=RequestContext(request))

def delete(request):
    # Used for XHTML validation testing
    # login(request, authenticate(username='user42', password='user42'))
    next = reverse('core:index')
    if 'next' in request.GET and request.GET['next'].strip() != '':
        next = request.GET['next']

    template_vars = { 'auth_next':next }
    if not request.user.is_authenticated():
        raise Http404
    elif request.method == 'POST':
        if request.user.check_password(request.POST['password']):
            request.user.is_active = False
            request.user.save()
            messages.error(request, request.user.username + ' has been deleted!')
            logout(request)
            return HttpResponseRedirect(next)
        else:
            template_vars['errors'] = 'That password was incorrect!'
    return render_to_response('web/delete.html', template_vars, context_instance=RequestContext(request))

#Profile page view
def profile(request):
    #Used for XHTML validation testing
    # profile = get_object_or_404(UserProfile, pk=1)
    profile = UserProfile.objects.filter(pk=request.user.id)
    change = { 'phones':[], 'addresses':[]}
    errors = {'phones':{}, 'addresses':{}}

    if profile.count() > 0:
        profile = profile[0]
    else:
        messages.info(request, 'You need to login/register to have a profile.')
        return HttpResponseRedirect(reverse('web:register'))

    if request.method == 'POST':
        #Lets do the simple stuff first
        from copy import deepcopy
        u = deepcopy(profile)
        u.user.first_name = request.POST['first_name'].strip()
        u.user.last_name = request.POST['last_name'].strip()
        u.user.email = request.POST['email'].strip()
        u.notes = request.POST['notes']
        #Name
        if len(u.user.first_name) > 0:
            profile.user.first_name = u.user.first_name
        else:
            errors['name'] = 'Enter your first and last names'
        if len(u.user.last_name) > 0:
            profile.user.last_name = u.user.last_name
        else:
            errors['name'] = 'Enter your first and last names'
        #Email
        try:
            validate_email(request.POST['email'])
            profile.user.email = request.POST['email']
        except ValidationError, err:
            errors['email'] = str(err.messages[0])
        #Notes
        profile.notes = request.POST['notes']
        profile.save()
        profile = u

        #Now a little harder
        #Deletes the user selected phones and addresses
        Phone.objects.filter(user=request.user.id, id__in=request.POST.getlist('removephone')).delete()
        Address.objects.filter(user=request.user.id, id__in=request.POST.getlist('removeaddress')).delete()

        #Update Existing Phone Numbers
        for phone in request.POST.getlist('existingphone'):
            try:
                pid = Phone.objects.get(pk=int(phone), user=request.user)
                pid.description_id = request.POST['phone' + str(pid.id) + 'description']
                pid.number = request.POST['phone' + str(pid.id) + 'number']
                pid.full_clean()
                pid.number = pid.cleaned_data.get('number')
                pid.save()
            except ValidationError, err:
                pid = Phone.objects.get(pk=int(phone), user=request.user)
                pid.description_id = request.POST['phone' + str(pid.id) + 'description']
                pid.number = request.POST['phone' + str(pid.id) + 'number']
                change['phones'].append(pid)
                errors['phones'][pid.id] = str(err.message_dict['__all__'][0])
            #These should never occur, unless the user is playing with the form, pass silently
            except Phone.DoesNotExist, err:
                pass
            except PhoneCategory.DoesNotExist, err:
                pass

        #Update Existing Addresses
        for address in request.POST.getlist('existingaddress'):
            try:
                pid = Address.objects.get(pk=int(address), user=request.user)
                pid.description_id = request.POST['address' + str(pid.id) + 'description']
                pid.address1 = request.POST['address' + str(pid.id) + 'address1']
                pid.address2 = request.POST['address' + str(pid.id) + 'address2']
                pid.buzzcode = request.POST['address' + str(pid.id) + 'buzzcode']
                pid.city = request.POST['address' + str(pid.id) + 'city']
                pid.state = request.POST['address' + str(pid.id) + 'state']
                pid.country = request.POST['address' + str(pid.id) + 'country']
                pid.postalcode = request.POST['address' + str(pid.id) + 'postalcode']
                pid.drivernotes = request.POST['address' + str(pid.id) + 'drivernotes']
                pid.full_clean()
                pid.save()
            except ValidationError, err:
                pid = Address.objects.get(pk=int(address), user=request.user)
                pid.description_id = request.POST['address' + str(pid.id) + 'description']
                pid.address1 = request.POST['address' + str(pid.id) + 'address1']
                pid.address2 = request.POST['address' + str(pid.id) + 'address2']
                pid.buzzcode = request.POST['address' + str(pid.id) + 'buzzcode']
                pid.city = request.POST['address' + str(pid.id) + 'city']
                pid.state = request.POST['address' + str(pid.id) + 'state']
                pid.country = request.POST['address' + str(pid.id) + 'country']
                pid.postalcode = request.POST['address' + str(pid.id) + 'postalcode']
                pid.drivernotes = request.POST['address' + str(pid.id) + 'drivernotes']
                change['addresses'].append(pid)
                errors['addresses'][pid.id] = str(err.message_dict['__all__'][0])
                messages.error(request, 'Error validating your ' + pid.description.description.lower() + ' address')
            except Address.DoesNotExist, err:
                messages.error(request, 'Address?')
            except AddressCategory.DoesNotExist, err:
                messages.error(request, 'AddressCategory?')

        #Add new Phones/Addresses
        newphones = zip(request.POST.getlist('newphonenumber'), request.POST.getlist('newphonedescription'))
        newaddresses = zip(request.POST.getlist('newaddress1'), request.POST.getlist('newaddress2'), request.POST.getlist('newbuzzcode'), request.POST.getlist('newcity'), request.POST.getlist('newstate'), request.POST.getlist('newcountry'), request.POST.getlist('newpostalcode'), request.POST.getlist('newdrivernotes'), request.POST.getlist('newaddressdescription'))
        #Add New Phone Numbers
        for (number, desc) in newphones:
            try:
                pid = Phone(user=request.user, description_id=desc, number=number)
                pid.full_clean()
                pid.save()
            except ValidationError, err:
                messages.error(request, 'Error validating your new phone number')
            except Phone.DoesNotExist, err:
                messages.error(request, 'Phony?')
            except PhoneCategory.DoesNotExist, err:
                messages.error(request, 'PhoneCategory?')

        #Add New Addresses
        for (line1, line2, buzz, city, state, country, postalcode, notes, desc) in newaddresses:
            try:
                pid = Address(user=request.user, description_id=desc, address1=line1, address2=line2, buzzcode=buzz, city=city, state=state, country=country, postalcode=postalcode, drivernotes=notes)
                pid.full_clean()
                pid.save()
            except ValidationError, err:
                messages.error(request, 'Error validating your new address')
            except Phone.DoesNotExist, err:
                messages.error(request, 'Address?')
            except AddressCategory.DoesNotExist, err:
                messages.error(request, 'AddressCategory?')
        messages.success(request, 'Your profile has been saved')
        #endif POST

    #Set the initial template variables, update as needed
    template_vars = { 'auth_next':reverse('core:index'), 'profile': profile, 'phones': Phone.objects.filter(user=request.user.id), 'addresses': Address.objects.filter(user=request.user.id), 'phonecategories': PhoneCategory.objects.all(), 'addresscategories': AddressCategory.objects.all(), 'errors': errors }
    #Phones
    for phone in change['phones']:
        for ph in template_vars['phones']:
            if ph.id == phone.id:
                ph.description = phone.description
                ph.number = phone.number
    #Addresses
    for address in change['addresses']:
        for add in template_vars['addresses']:
            if add.id == address.id:
                add.description = address.description
                add.address1 = address.address1
                add.address2 = address.address2
                add.buzzcode = address.buzzcode
                add.city = address.city
                add.state = address.state
                add.country = address.country
                add.postalcode = address.postalcode
                add.drivernotes = address.drivernotes
    return render_to_response('web/profile.html', template_vars, context_instance=RequestContext(request))

def previous(request):
    #Used for XHTML validation testing
    # login(request, authenticate(username='user42', password='user42'))
    if not request.user.is_authenticated():
        messages.info(request, 'You need to login/register to have a past order.')
        return HttpResponseRedirect(reverse('web:register'))
    else:
        orders = Order.objects.filter(user=request.user.id, completed=True).order_by('-date')
        items = OrderItem.objects.filter(order__user=request.user.id)
        return render_to_response('web/previous.html', {'orders':orders, 'items':items}, context_instance=RequestContext(request))

def directions(request):
    return render_to_response('web/directions.html', context_instance=RequestContext(request))

def nameserv(request):
    if 'uname' in request.GET and User.objects.filter(username=request.GET['uname']).count() == 1:
        return HttpResponse(1)
    else:
        return HttpResponse(0)
