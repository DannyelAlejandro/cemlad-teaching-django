from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    """
    Serializer para productos del catálogo.
    
    Se utiliza tanto para listar productos como para crear nuevos.
    """
    id = serializers.IntegerField(
        read_only=True,
        help_text="ID único del producto (auto-generado)"
    )
    name = serializers.CharField(
        max_length=255,
        help_text="Nombre del producto (máximo 255 caracteres)"
    )
    code = serializers.CharField(
        max_length=50,
        help_text="Código SKU único del producto (máximo 50 caracteres)"
    )
    price = serializers.FloatField(
        help_text="Precio unitario del producto en formato decimal"
    )


class ProductResponseSerializer(serializers.Serializer):
    """Respuesta de producto con todos los campos."""
    id = serializers.IntegerField(help_text="ID único del producto")
    name = serializers.CharField(help_text="Nombre del producto")
    code = serializers.CharField(help_text="Código SKU del producto")
    price = serializers.FloatField(help_text="Precio unitario")


class CartProductSerializer(serializers.Serializer):
    """
    Serializer para productos dentro de un carrito.
    
    Incluye información de la cantidad implícita en el carrito.
    """
    product_id = serializers.IntegerField(
        help_text="ID del producto agregado al carrito"
    )
    product_name = serializers.CharField(
        max_length=255,
        read_only=True,
        help_text="Nombre del producto (información de lectura)"
    )
    price = serializers.FloatField(
        read_only=True,
        help_text="Precio unitario del producto al momento de agregarle (información de lectura)"
    )


class CartSerializer(serializers.Serializer):
    """
    Serializer para carrito de compras.
    
    Representa un carrito con sus productos y estado.
    """
    id = serializers.IntegerField(
        read_only=True,
        help_text="ID único del carrito (auto-generado)"
    )
    customer_id = serializers.IntegerField(
        help_text="ID del cliente propietario del carrito"
    )
    status = serializers.CharField(
        max_length=10,
        help_text="Estado del carrito: ACT (Activo), PAID (Pagado), CANC (Cancelado)"
    )
    total = serializers.FloatField(
        help_text="Total del carrito (suma de todos los productos)"
    )
    products = ProductSerializer(
        many=True,
        read_only=True,
        help_text="Lista de productos en el carrito"
    )


class CartCreateSerializer(serializers.Serializer):
    """Serializer para crear un nuevo carrito."""
    customer_id = serializers.IntegerField(
        help_text="ID del cliente propietario del carrito"
    )
    status = serializers.CharField(
        max_length=10,
        default="ACT",
        help_text="Estado inicial del carrito (por defecto: ACT)"
    )
    total = serializers.FloatField(
        default=0.0,
        help_text="Total inicial del carrito (por defecto: 0.0)"
    )


class CartAddProductSerializer(serializers.Serializer):
    """Serializer para agregar un producto a un carrito."""
    product_id = serializers.IntegerField(
        help_text="ID del producto a agregar al carrito"
    )


class CartPaySerializer(serializers.Serializer):
    """Serializer para procesar el pago de un carrito."""
    payment_method = serializers.ChoiceField(
        choices=['CASH', 'CARD'],
        help_text="Método de pago: CASH (Efectivo) o CARD (Tarjeta)"
    )


class PaymentResponseSerializer(serializers.Serializer):
    """Respuesta del procesamiento de pago."""
    message = serializers.CharField(
        help_text="Mensaje con el resultado del pago"
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Respuesta estándar de error."""
    error = serializers.CharField(
        help_text="Mensaje descriptivo del error"
    )
