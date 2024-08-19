from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from marshmallow import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from . import serializers
from products import models

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Vista de login"""
    login_schema = serializers.UserSchema()
    try: 
        user_data = login_schema.loads(request.body)
        #username
        #password
    except ValidationError as err:
        return JsonResponse(
            {
                "success": False,
                "message": err.messages
            },
            status = 404
        )

    username = user_data.get("username")
    password = user_data.get("password")
    
    if username and password:
        #autenticacion
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                status=200,
                data = {"result": "Se ha iniciado sesión."}
            )
        else:
            return JsonResponse(
                status=404,
                data = {"result": "Ha ocurrido un error."}
            )

@csrf_exempt
@require_http_methods(["POST"])
def create_user_view(request):
    """Vista de crear usuario"""
    if request.user.is_authenticated:
        return JsonResponse(
            status = 404, data = {"message": "Debe cerrar sesión para crear un nuevo usuario"}
        )
    else:
        register_user_schema = serializers.UserSchema()
        try: 
            user_data = register_user_schema.loads(request.body)
        except ValidationError as err:
            return JsonResponse(
                {
                    "success": False,
                    "message": err.messages
                },
                status = 404
            )

        username = user_data.get("username")
        password = user_data.get("password")
        
        if User.objects.filter(username__iexact=username).exists():
            return JsonResponse(
                status=404,
                data = {"message": f"No se puede crear el usuario /*{username}*/ por que ya existe."}
            )
        else:
            new_user = User.objects.create_user(
                username= username,
                password= password
            )
            new_user.save()
            
            return JsonResponse(
                status=200,
                data = {"message": f"El usuario /*{username}*/ ha sido creado con éxito."}
            )
        
@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """Vista para cerrar sesion"""
    logout(request)
    return JsonResponse(
        status=200,
        data={"message": "Se ha cerrado la sesión."}
    )
                

def check_authorization(view):
    
    def wrapper(request):
        acces_denied_response = JsonResponse(
            status=403, 
            data = {"result": "Acceso denegado"}
        )
        token_b64 = request.headers.get("Authorization", None)
        if not token_b64:
            return acces_denied_response
        token_ej = token_b64.replace('Basic ', '')
        try:
            decode_token = urlsafe_base64_decode(token_ej).decode('UTF-8').split(':')
        except Exception:
            return acces_denied_response
        
        if len(decode_token) != 2:
            return acces_denied_response
        username = decode_token[0]
        password = decode_token[1]
        #autenticacion
        user = authenticate(request, username = username, password = password)
        if user is None:
            return acces_denied_response

        return view(request)
        
    return wrapper
    
"""
Clonar repo de EasyStart
pyhton3 easystart/django-easystart/setup.py
#ejecutar el comando desde fuera del directorio

-como se llama el proyect
-nombre slug
-dominio
--> Luego generar el proyecto generar docker

docker compose build
docker compose up 

CREA UN PROYECTO EN BASE A EASY START

vistas__ irian en el directorio apps
utils___ irian los decoradores
frontend ___ irían todos los vistas
"""
    
@check_authorization
def product_list_view(request):
    """Vista para mostrar a lista de productos"""
        
    products_list = models.Product.objects.all()
    product_schema = serializers.ProductSchema()
    
    #paginacion
    paginate_by = 2
    paginator = Paginator(products_list, paginate_by)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    #serializacion del producto a JSON
    result = product_schema.dump(products, many=True)
    data = {
        "products": result,
        "count" : paginator.count,
        "num_pages" : paginator.num_pages,
        "page" : products.number,
    }
    return JsonResponse( status=200, data=data )
        

@require_http_methods(["GET"])
def product_detail_view(request, product_id):
    """Vista para el ver un producto"""
    #obtener token, decodificar y dividir (username, password)
    token_b64 = request.headers.get("Authorization")
    token_ej = token_b64.replace('Basic ', '')
    decode_token = urlsafe_base64_decode(token_ej).decode('UTF-8').split(':')
    username = decode_token[0]
    password = decode_token[1]
    
    #autenticacion
    user = authenticate(request, username = username, password = password)
    if user is not None:
        try:
            product_detail = models.Product.objects.get(pk=product_id)
        except models.Product.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Este producto no existe."
                },
                status = 404
            )

        #serializacion del producto
        product_schema = serializers.ProductSchema()
        result = product_schema.dump(product_detail)
        
        return JsonResponse(status=200,data = result)
    else:
        return JsonResponse( status=404, data = {"result": "El usuario no existe"})
    
@csrf_exempt
@require_http_methods(["POST"])
def product_add_view(request):
    """Vista para agregar un producto"""
    #obtener token, decodificar y dividir (username, password)
    token_b64 = request.headers.get("Authorization")
    token_ej = token_b64.replace('Basic ', '')
    decode_token = urlsafe_base64_decode(token_ej).decode('UTF-8').split(':')
    username = decode_token[0]
    password = decode_token[1]
    
    #autenticacion
    user = authenticate(request, username = username, password = password)
    if user is not None:
        product_schema = serializers.ProductSchema()
        try: 
            product_data = product_schema.loads(request.body, partial=["id"])
        except ValidationError as err:
            return JsonResponse(
                {"success": False, "message": err.messages},
                status = 404
            )
        else: 
            product = models.Product()
            product.name = product_data.get("name")
            product.description = product_data.get("description")
            product.price = product_data.get("price")
            product.available = product_data.get("available")
            product.date = product_data.get("date")
            product.save()
        
            #serializacion del producto a JSON
            # result = product_schema.dump(product)
            data = {
                "message": f"El producto */{product.name}/* ha sido creado con éxito.",
                "id": product.id,
                }
            return JsonResponse(status=200, data = data)
    else:
        return JsonResponse(
            status=404,
            data = {"result": "El usuario no existe"}
        )
                
@csrf_exempt
def product_edit_view(request, product_id):
    """Vista para editar un producto"""
    #obtener token, decodificar y dividir (username, password)
    token_b64 = request.headers.get("Authorization")
    token_ej = token_b64.replace('Basic ', '')
    decode_token = urlsafe_base64_decode(token_ej).decode('UTF-8').split(':')
    username = decode_token[0]
    password = decode_token[1]
    
    #autenticacion
    user = authenticate(request, username = username, password = password)
    if user is not None:
        product_schema = serializers.ProductSchema()
        if request.method == "PUT":
            try:
                product = models.Product.objects.get(pk=product_id)
            except models.Product.DoesNotExist:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Este producto no existe."
                    },
                    status = 404
                )
            try: 
                product_data = product_schema.loads(request.body, partial=["id"])
            except ValidationError as err:
                return JsonResponse(
                    {
                        "success": False,
                        "message": err.messages
                    },
                    status = 404
                )
            #cambios
            product.name = product_data.get("name")
            product.price = product_data.get("price")
            product.description = product_data.get("description")
            product.available = product_data.get("available")
            product.date = product_data.get("date")
            product.save()
            data = {"message": f"El producto */{product.name}/* ha sido editado",}
            
            return JsonResponse(status=200, data=data,)
    else:
        return JsonResponse(
            status=404,
            data = {"result": "El usuario no existe"}
        )

@csrf_exempt
def product_delete_view(request, product_id):
    """Vista para eliminar un producto"""
    #obtener token, decodificar y dividir (username, password)
    token_b64 = request.headers.get("Authorization")
    token_ej = token_b64.replace('Basic ', '')
    decode_token = urlsafe_base64_decode(token_ej).decode('UTF-8').split(':')
    username = decode_token[0]
    password = decode_token[1]
    
    #autenticacion
    user = authenticate(request, username = username, password = password)
    if user is not None:
        if request.method == 'DELETE':
            try:
                product = models.Product.objects.get(pk=product_id)
            except models.Product.DoesNotExist:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Este producto no existe."
                    },
                    status = 404
                )
            product.delete()
            data = {"message": "El producto ha sido eliminado."}
            
            return JsonResponse(status=200, data = data)
    else:
        return JsonResponse(
            status=404,
            data = {"result": "El usuario no existe"}
        )

