from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from api.serializers import (
    ProductSerializer, CartSerializer, CartAddProductSerializer, 
    CartPaySerializer, PaymentResponseSerializer, ErrorResponseSerializer,
    ProductResponseSerializer, CartCreateSerializer
)

from api.dto.cart_response_dto import CartResponseDTO
from api.dto.payment_response_dto import PaymentResponseDTO
from api.dto.product_response_dto import ProductResponseDTO
from api.services.cart_service import CartService
from api.services.product_service import ProductService

product_service = ProductService()
cart_service = CartService()

# ============================================================================
# HOME / WELCOME ENDPOINT
# ============================================================================

@extend_schema(
    tags=['System'],
    responses={
        200: OpenApiResponse(
            response={'type': 'object', 'properties': {'message': {'type': 'string'}}},
            description='API is running successfully'
        )
    },
    summary='Welcome - Health Check',
    description='Verifica que la API está activa y funcionando correctamente.'
)
@api_view(['GET'])
def home(request):
    """
    Welcome endpoint for CEMLAD API.
    
    Returns a welcome message to verify API is running.
    """
    request.accepted_renderer = JSONRenderer()
    return Response({"message": "Welcome to the CEMLAD API!"}, status=status.HTTP_200_OK)


# ============================================================================
# PRODUCT ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Products'],
    summary='List and Create Products',
    description='Obtiene la lista completa de productos o crea un nuevo producto.',
    methods=['GET'],
    responses={
        200: OpenApiResponse(
            response=ProductResponseSerializer(many=True),
            description='Lista de todos los productos disponibles'
        ),
    },
)
@extend_schema(
    tags=['Products'],
    methods=['POST'],
    request=ProductSerializer,
    responses={
        201: OpenApiResponse(
            response=ProductResponseSerializer,
            description='Producto creado exitosamente',
            examples=[
                OpenApiExample(
                    'Success',
                    value={'id': 1, 'name': 'Laptop', 'code': 'SKU001', 'price': 999.99}
                )
            ]
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Falló la creación del producto',
            examples=[
                OpenApiExample(
                    'Error',
                    value={'error': 'Failed to create product'}
                )
            ]
        ),
    },
)
@api_view(['GET', 'POST'])
def product_list_create(request):
    """
    List all products or create a new product.
    
    GET: Retrieve all products
    POST: Create a new product
    
    **Ejemplo Request (POST):**
    ```json
    {
        "name": "Laptop Dell XPS",
        "code": "SKU001",
        "price": 1299.99
    }
    ```
    """
    if request.method == 'GET':
        products = product_service.get_all_products()
        product_data = [(ProductResponseDTO(p)).to_dict() for p in products]
        
        request.accepted_renderer = JSONRenderer()
        return Response(product_data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        product_data = request.data
        created_product = product_service.create_product(product_data)
        
        if created_product:
            response_data = (ProductResponseDTO(created_product)).to_dict()
            request.accepted_renderer = JSONRenderer()
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to create product"}, status=status.HTTP_400_BAD_REQUEST)
        

@extend_schema(
    tags=['Products'],
    summary='Retrieve Product Details',
    description='Obtiene los detalles de un producto específico por su ID.',
    parameters=[
        OpenApiParameter(
            name='product_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID único del producto a recuperar',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            response=ProductResponseSerializer,
            description='Detalles del producto',
            examples=[
                OpenApiExample(
                    'Success',
                    value={'id': 1, 'name': 'Laptop', 'code': 'SKU001', 'price': 999.99}
                )
            ]
        ),
        404: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Producto no encontrado',
            examples=[
                OpenApiExample(
                    'Not Found',
                    value={'error': 'Product not found'}
                )
            ]
        ),
    },
)
@extend_schema(
    tags=['Products'],
    methods=['PATCH', 'PUT'],
    request=ProductSerializer,
    responses={
        200: OpenApiResponse(
            response=ProductResponseSerializer,
            description='Producto actualizado exitosamente'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Falló la actualización del producto'
        ),
    },
)
@extend_schema(
    tags=['Products'],
    methods=['DELETE'],
    responses={
        204: OpenApiResponse(
            description='Producto eliminado exitosamente'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Falló la eliminación del producto'
        ),
    },
)
@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def product_detail_update_delete(request, product_id):
    """
    Retrieve, update, or delete a product.
    
    GET: Retrieve a product by ID
    PATCH/PUT: Update a product (parcial o completo)
    DELETE: Delete a product
    
    Path parameters:
        product_id (int): The ID of the product
        
    **Ejemplo Request (PUT/PATCH):**
    ```json
    {
        "name": "Laptop Dell XPS Updated",
        "code": "SKU001",
        "price": 1199.99
    }
    ```
    """
    if request.method == 'GET':
        product = product_service.get_product_by_id(product_id)
        if product:
            response_data = (ProductResponseDTO(product)).to_dict()
            request.accepted_renderer = JSONRenderer()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method in ['PATCH', 'PUT']:
        product_data = request.data
        updated_product = product_service.update_product(product_id, product_data)
        
        if updated_product:
            response_data = (ProductResponseDTO(updated_product)).to_dict()
            request.accepted_renderer = JSONRenderer()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to update product"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        success = product_service.delete_product(product_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Failed to delete product"}, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# CART ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Carts'],
    summary='List and Create Shopping Carts',
    description='Obtiene la lista completa de carritos o crea un nuevo carrito de compras.',
    methods=['GET'],
    responses={
        200: OpenApiResponse(
            response=CartSerializer(many=True),
            description='Lista de todos los carritos disponibles'
        ),
    },
)
@extend_schema(
    tags=['Carts'],
    methods=['POST'],
    request=CartCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=CartSerializer,
            description='Carrito creado exitosamente',
            examples=[
                OpenApiExample(
                    'Success',
                    value={
                        'id': 1,
                        'customer_id': 100,
                        'status': 'ACT',
                        'total': 0.0,
                        'products': []
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Falló la creación del carrito'
        ),
    },
)
@api_view(['GET', 'POST'])
def cart_list_create(request):
    """
    List all carts or create a new cart.
    
    GET: Retrieve all shopping carts
    POST: Create a new shopping cart
    
    **Ejemplo Request (POST):**
    ```json
    {
        "customer_id": 100,
        "status": "ACT",
        "total": 0.0
    }
    ```
    """
    if request.method == 'GET':
        carts = cart_service.get_all_carts()
        cart_data = [CartResponseDTO(c).to_dict() for c in carts]
        
        request.accepted_renderer = JSONRenderer()
        return Response(cart_data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        cart_data = request.data
        created_cart = cart_service.create_cart(cart_data)
        
        if created_cart:
            response_data = CartResponseDTO(created_cart).to_dict()
            request.accepted_renderer = JSONRenderer()
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to create cart"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Carts'],
    summary='Retrieve Shopping Cart Details',
    description='Obtiene los detalles de un carrito específico incluyendo productos.',
    parameters=[
        OpenApiParameter(
            name='cart_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID único del carrito a recuperar',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            response=CartSerializer,
            description='Detalles del carrito',
            examples=[
                OpenApiExample(
                    'Success',
                    value={
                        'id': 1,
                        'customer_id': 100,
                        'status': 'ACT',
                        'total': 2299.98,
                        'products': [
                            {'product_id': 1, 'product_name': 'Laptop', 'price': 999.99},
                            {'product_id': 2, 'product_name': 'Mouse', 'price': 29.99}
                        ]
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Carrito no encontrado'
        ),
    },
)
@api_view(['GET'])
def cart_detail(request, cart_id):
    """
    Retrieve a specific cart by ID.
    
    Path parameters:
        cart_id (int): The ID of the cart
    """
    if request.method == 'GET':
        cart = cart_service.get_cart_by_id(cart_id)
        
        if cart:
            response_data = CartResponseDTO(cart).to_dict()
            request.accepted_renderer = JSONRenderer()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=['Carts'],
    summary='Get Cart Products',
    description='Obtiene la lista de productos en un carrito específico.',
    parameters=[
        OpenApiParameter(
            name='cart_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID del carrito',
            required=True
        )
    ],
    methods=['GET'],
    responses={
        200: OpenApiResponse(
            response=CartSerializer,
            description='Lista de productos en el carrito',
            examples=[
                OpenApiExample(
                    'Success',
                    value={
                        'id': 1,
                        'customer_id': 100,
                        'status': 'ACT',
                        'total': 1029.98,
                        'products': [
                            {'product_id': 1, 'product_name': 'Laptop', 'price': 999.99},
                            {'product_id': 2, 'product_name': 'Mouse', 'price': 29.99}
                        ]
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Carrito no encontrado'
        ),
    },
)
@extend_schema(
    tags=['Carts'],
    summary='Add Product to Shopping Cart',
    description='Agrega un producto específico al carrito de compras indicado.',
    parameters=[
        OpenApiParameter(
            name='cart_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID del carrito',
            required=True
        )
    ],
    methods=['POST'],
    request=CartAddProductSerializer,
    responses={
        200: OpenApiResponse(
            response=CartSerializer,
            description='Carrito actualizado con el nuevo producto',
            examples=[
                OpenApiExample(
                    'Success',
                    value={
                        'id': 1,
                        'customer_id': 100,
                        'status': 'ACT',
                        'total': 1029.98,
                        'products': [
                            {'product_id': 1, 'product_name': 'Laptop', 'price': 999.99},
                            {'product_id': 2, 'product_name': 'Mouse', 'price': 29.99}
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Falló agregar el producto al carrito'
        ),
    },
)
@api_view(['GET', 'POST'])
def cart_add_get_products(request, cart_id):
    """
    Get products in a cart or add a product to a cart.
    
    GET: Retrieve all products in the specified cart
    POST: Add a new product to the cart
    
    Path parameters:
        cart_id (int): The ID of the cart
    
    **Ejemplo Request (POST):**
    ```json
    {
        "product_id": 2
    }
    ```
    """
    if request.method == 'GET':
        products = cart_service.get_products_in_cart(cart_id)
        
        if products is not None:
            products_data = [ProductResponseDTO(cp.product).to_dict() for cp in products]
            request.accepted_renderer = JSONRenderer()
            return Response(products_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_cart = cart_service.add_product_to_cart(cart_id, product_id)
        
        if updated_cart:
            response_data = CartResponseDTO(updated_cart).to_dict()
            request.accepted_renderer = JSONRenderer()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to add product to cart"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Carts'],
    summary='Remove Product from Shopping Cart',
    description='Elimina un producto específico del carrito de compras.',
    parameters=[
        OpenApiParameter(
            name='cart_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID del carrito',
            required=True
        ),
        OpenApiParameter(
            name='product_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID del producto a eliminar',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            response=CartSerializer,
            description='Carrito actualizado sin el producto eliminado'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Falló eliminar el producto del carrito'
        ),
    },
)
@api_view(['DELETE'])
def cart_remove_product(request, cart_id, product_id):
    """
    Remove a product from a cart.
    
    Path parameters:
        cart_id (int): The ID of the cart
        product_id (int): The ID of the product to remove
    """
    if request.method == 'DELETE':
        updated_cart = cart_service.remove_product_from_cart(cart_id, product_id)
        
        if updated_cart:
            response_data = CartResponseDTO(updated_cart).to_dict()
            request.accepted_renderer = JSONRenderer()
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to remove product from cart"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Payments'],
    summary='Process Cart Payment',
    description='Procesa el pago del carrito usando el método de pago especificado (Efectivo o Tarjeta).',
    parameters=[
        OpenApiParameter(
            name='cart_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID del carrito a pagar',
            required=True
        )
    ],
    request=CartPaySerializer,
    responses={
        200: OpenApiResponse(
            response=PaymentResponseSerializer,
            description='Pago procesado exitosamente',
            examples=[
                OpenApiExample(
                    'Success',
                    value={'message': 'Pago procesado exitosamente con CASH'}
                )
            ]
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Falló procesar el pago',
            examples=[
                OpenApiExample(
                    'Error',
                    value={'error': 'Invalid payment method or cart not found'}
                )
            ]
        ),
    },
)
@api_view(['POST'])
def cart_pay(request, cart_id):
    """
    Procesar el pago de un carrito.
    
    Path parameters:
        cart_id (int): ID del carrito a pagar
    
    **Ejemplo Request:**
    ```json
    {
        "payment_method": "CASH"
    }
    ```
    
    Métodos de pago válidos:
    - CASH: Pago en efectivo
    - CARD: Pago con tarjeta
    """
    if request.method == 'POST':
        payment_method = request.data.get('payment_method')
        
        if not payment_method:
            return Response(
                {"error": "payment_method is required. Valid values: CASH, CARD"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_result = cart_service.process_payment(cart_id, payment_method)
        
        if payment_result is None:
            return Response(
                {"error": "Invalid payment method or cart not found"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response_dto = PaymentResponseDTO(payment_result.get('message'))
        response_data = response_dto.to_dict()
        
        request.accepted_renderer = JSONRenderer()
        return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_200_OK)