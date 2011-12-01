from django.shortcuts import render_to_response, get_object_or_404
from portal.models import Documento
from portal.models import LoginForm
from portal.models import RegistroArticulo, RegistroArticuloForm
from portal.models import Equipo, EquipoForm
from portal.models import Interesado, InteresadoForm
from portal.models import TipoDocumento, TipoDocumentoForm
from django.template import RequestContext
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404

@login_required(login_url='/ingreso/')
def index(request):
    return render_to_response('index.html')

def ingreso(request):
	if request.method == 'POST':
		formu = LoginForm(request.POST)
		loginuser = request.POST['userform']
		loginpass = request.POST['passform']
		loginaccess = authenticate(username=loginuser,password=loginpass)
		if loginaccess is not None:
			if loginaccess.is_active:
				login(request,loginaccess)
				return HttpResponseRedirect('/')
			else:
				return render_to_response('noactivo.html')
		else:
			return render_to_response('nousuario.html')
	else:
		formu = LoginForm(auto_id=True)
	return render_to_response('ingreso.html',{'formu':formu},context_instance=RequestContext(request))

#view of persons, documents and equipment
@login_required(login_url='/ingreso/')
def equipos(request):
	datos = Equipo.objects.all()
	return render_to_response('equipos.html',{'datos':datos})
	
@login_required(login_url='/ingreso/')
def equiposeditar(request, equipo_id):
	dato = get_object_or_404(Equipo, pk=equipo_id)
	if request.method == 'POST':
		formulario = EquipoForm(request.POST)
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre']
			dato.nombre = nombre
			dato.save()
			return HttpResponseRedirect('/produccion/equipos/')
	else:
		formulario = EquipoForm(instance=dato)
	return render_to_response('equiposeditar.html',{'formulario':formulario},context_instance=RequestContext(request))
	
#view of persons, documents and equipment
@login_required(login_url='/ingreso/')
def interesados(request):
	datos = Interesado.objects.all()
	return render_to_response('interesados.html',{'datos':datos})
	
@login_required(login_url='/ingreso/')
def (request, interesado_id):
	dato = get_object_or_404(Equipo, pk= interesado_id)
	if request.method == 'POST':
		formulario = EquipoForm(request.POST)
		if formulario.is_valid():
			nombre = formulario.cleaned_data['nombre']
			dato.nombre = nombre
			dni = formulario.cleaned_data['dni']
			dato.dni = dni
			oficina = formulario.cleaned_data['oficina']
			dato.oficina = oficina
			dato.save()
			return HttpResponseRedirect('/produccion/interesados/')
	else:
		formulario = EquipoForm(instance=dato)
	return render_to_response('interesadoseditar.html',{'formulario':formulario},context_instance=RequestContext(request))
	
	
def documentos(request):
	datos = Documento.objects.all().order_by('-id')
	return render_to_response('documentos.html',{'datos':datos})

def registroarticuloformu(request):
	if request.method == 'POST':
		formulario = RegistroArticuloForm(request.POST)
		if formulario.is_valid():
			detalle = formulario.cleaned_data['detalle']
			cantidad = formulario.cleaned_data['cantidad']
			fregistro = formulario.cleaned_data['fregistro']
			tipo = formulario.cleaned_data['tipo']
			precio = formulario.cleaned_data['precio']
			preciototal = formulario.cleaned_data['preciototal']
			articulo = formulario.cleaned_data['articulo']
			usuario = request.user
			guardarregistro = RegistroArticulo(detalle=detalle,cantidad=cantidad,fregistro=fregistro,tipo=tipo,precio=precio,preciototal=preciototal,articulo=articulo,usuario=usuario)
			guardarregistro.save()
			return HttpResponseRedirect('/')
	else:
		formulario = RegistroArticuloForm(auto_id=True)
	return render_to_response('registroarticuloform.html',{'formulario':formulario},context_instance=RequestContext(request))
