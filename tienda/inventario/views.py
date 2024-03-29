from django import dispatch
from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
from django.template import loader
from .models import Producto,Venta
from django.contrib.auth.models import User
from .forms import productoForm,ventaForm
from django.views.generic import View,TemplateView,CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse

class claseIndex(View):
    
    def get(self, request):
        print(self.http_method_names) 
        return render(request,'inventario/home.html')

class claseProductos(View):
    form_class = productoForm
    template_name='inventario/productos.html'
    
    def get(self, request):
        form =self.form_class(request.POST)
        context={'form': form}
        return render(request,self.template_name,context)
  
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            context={'form': form}
            return redirect('inventario:claseIndex')
        return render(request,self.template_name,context)

class homeTemplate(TemplateView):
   template_name = "inventario/home.html"

# class productoList(TemplateView):
#    template_name = "inventario/productos.html"


class productoList(ListView):
 model=Producto
 template_name='inventario/productos.html'
 form_class=productoForm

class productoCreate(CreateView):
 model=Producto
 template_name='inventario/productoCreate.html'
 form_class=productoForm
 success_url=reverse_lazy('inventario:productoList')

class productoUpdate(UpdateView):
   model=Producto
   template_name='inventario/productoUpdate.html'
   form_class=productoForm
   success_url = reverse_lazy('inventario:productoList')

class productoDelete(DeleteView):
  model=Producto
  context_object_name='producto'
  template_name='inventario/productoDelete.html'
  success_url=reverse_lazy('inventario:productoList')

#Modeleo Ventas
class ventaCreate(CreateView):
    model=Venta
    template_name='inventario/ventaCreate.html'
    form_class=ventaForm
    success_url=reverse_lazy('inventario:ventaList')

    def form_valid(self, form):
        form.instance.vendedor=self.request.user
        return super().form_valid(form)

        
# class ventaList(ListView):
#     model=Venta
#     template_name='inventario/ventas.html'
#     form_class=ventaForm
#     context_object_name='ventas'
#     def get_form_kwargs(self):
#         kwargs=super(ventaList, self).get_form_kwargs()
#         kwargs['vendedor']=self.request.user
#         return kwargs

def ventaList(request):
    context = {}
    context['ventas'] = Venta.objects.filter(vendedor=request.user)
    return render(request, 'inventario/ventas.html', context)

class ventaUpdate(UpdateView):
    model=Venta
    template_name='inventario/ventaUpdate.html'
    form_class=ventaForm
    success_url = reverse_lazy('inventario:ventaList')

class ventaDelete(DeleteView):
    model=Venta
    context_object_name='venta'
    template_name='inventario/ventaDelete.html'
    success_url=reverse_lazy('accounts:login')

import json
def search(request):
    slug= request.GET.get('nombre')
    print(slug)
    productos=Producto.objects.filter(nombre=slug)
    print(productos)
    productos=[producto_serializer(productos) for productos in productos]
    print(productos)
    return render(request,'inventario/productos.html',context=json.dumps(productos),content_type='application/json')

def producto_serializer(producto):
    return {'nombre':producto.nombre}