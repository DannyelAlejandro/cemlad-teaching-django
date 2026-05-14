# 📚 CEMLAD API REST - Documentación Completa

## 🎯 Descripción General

API REST desarrollada en **Django REST Framework** para gestionar:
- ✅ Productos (CRUD completo)
- ✅ Carrito de compras
- ✅ Procesamiento de pagos (Efectivo/Tarjeta)
- ✅ Respuestas tipificadas con DTOs

**Versión:** 1.0.0  
**Base URL:** `http://localhost:8000`

---

## 📖 Acceso a Documentación Interactiva

### Swagger UI (Recomendado)
```
http://localhost:8000/api/docs/
```
- Interfaz interactiva
- Prueba endpoints directamente
- Visualiza esquema completo

### ReDoc
```
http://localhost:8000/api/redoc/
```
- Vista alternativa más limpia
- Mejor para lectura

### Schema OpenAPI 3.0
```
http://localhost:8000/api/schema/
```
- Formato JSON puro
- Para integraciones programáticas

---

## 🏗️ Estructura de Respuestas

### ✅ Respuesta Exitosa (200/201)
```json
{
  "id": 1,
  "name": "Laptop Dell XPS",
  "code": "SKU001",
  "price": 1299.99
}
```

### ❌ Respuesta de Error (400/404)
```json
{
  "error": "Product not found"
}
```

---

## 📦 PRODUCTOS

### 🔹 GET - Listar Todos los Productos

**Endpoint:**
```
GET /products
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "Laptop Dell XPS",
    "code": "SKU001",
    "price": 1299.99
  },
  {
    "id": 2,
    "name": "Mouse Logitech",
    "code": "SKU002",
    "price": 29.99
  }
]
```

---

### 🔹 POST - Crear Nuevo Producto

**Endpoint:**
```
POST /products
```

**Request:**
```json
{
  "name": "Laptop Dell XPS",
  "code": "SKU001",
  "price": 1299.99
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "name": "Laptop Dell XPS",
  "code": "SKU001",
  "price": 1299.99
}
```

**Códigos de Error:**
- `400`: Datos inválidos
- `500`: Error del servidor

---

### 🔹 GET - Obtener Producto por ID

**Endpoint:**
```
GET /products/{product_id}
```

**Parámetros:**
- `product_id` (int, requerido): ID del producto

**Ejemplo:**
```
GET /products/1
```

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Laptop Dell XPS",
  "code": "SKU001",
  "price": 1299.99
}
```

**Códigos de Error:**
- `404`: Producto no encontrado

---

### 🔹 PUT/PATCH - Actualizar Producto

**Endpoint:**
```
PUT /products/{product_id}
PATCH /products/{product_id}
```

**Diferencia:**
- `PUT`: Reemplaza todos los campos (completo)
- `PATCH`: Actualiza solo los campos enviados (parcial)

**Request:**
```json
{
  "name": "Laptop Dell XPS 15",
  "price": 1399.99
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Laptop Dell XPS 15",
  "code": "SKU001",
  "price": 1399.99
}
```

---

### 🔹 DELETE - Eliminar Producto

**Endpoint:**
```
DELETE /products/{product_id}
```

**Respuesta (204):**
- Sin contenido (eliminado exitosamente)

**Códigos de Error:**
- `404`: Producto no encontrado
- `400`: No se pudo eliminar

---

## 🛒 CARRITO DE COMPRAS

### 🔹 GET - Listar Todos los Carritos

**Endpoint:**
```
GET /carts
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "customer_id": 100,
    "status": "ACT",
    "total": 1329.98,
    "products": [
      {
        "product_id": 1,
        "product_name": "Laptop Dell XPS",
        "price": 1299.99
      },
      {
        "product_id": 2,
        "product_name": "Mouse Logitech",
        "price": 29.99
      }
    ]
  }
]
```

---

### 🔹 POST - Crear Nuevo Carrito

**Endpoint:**
```
POST /carts
```

**Request:**
```json
{
  "customer_id": 100,
  "status": "ACT",
  "total": 0.0
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "customer_id": 100,
  "status": "ACT",
  "total": 0.0,
  "products": []
}
```

---

### 🔹 GET - Obtener Carrito por ID

**Endpoint:**
```
GET /carts/{cart_id}
```

**Parámetros:**
- `cart_id` (int, requerido): ID del carrito

**Respuesta (200):**
```json
{
  "id": 1,
  "customer_id": 100,
  "status": "ACT",
  "total": 1329.98,
  "products": [
    {
      "product_id": 1,
      "product_name": "Laptop Dell XPS",
      "price": 1299.99
    },
    {
      "product_id": 2,
      "product_name": "Mouse Logitech",
      "price": 29.99
    }
  ]
}
```

---

### 🔹 POST - Agregar Producto al Carrito

**Endpoint:**
```
POST /carts/{cart_id}/products
```

**Parámetros:**
- `cart_id` (int, requerido): ID del carrito

**Request:**
```json
{
  "product_id": 2
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "customer_id": 100,
  "status": "ACT",
  "total": 1329.98,
  "products": [
    {
      "product_id": 1,
      "product_name": "Laptop Dell XPS",
      "price": 1299.99
    },
    {
      "product_id": 2,
      "product_name": "Mouse Logitech",
      "price": 29.99
    }
  ]
}
```

---

### 🔹 DELETE - Eliminar Producto del Carrito

**Endpoint:**
```
DELETE /carts/{cart_id}/products/{product_id}
```

**Parámetros:**
- `cart_id` (int, requerido): ID del carrito
- `product_id` (int, requerido): ID del producto a eliminar

**Respuesta (200):**
```json
{
  "id": 1,
  "customer_id": 100,
  "status": "ACT",
  "total": 1299.99,
  "products": [
    {
      "product_id": 1,
      "product_name": "Laptop Dell XPS",
      "price": 1299.99
    }
  ]
}
```

---

## 💳 PAGOS

### 🔹 POST - Procesar Pago del Carrito

**Endpoint:**
```
POST /carts/{cart_id}/pay
```

**Parámetros:**
- `cart_id` (int, requerido): ID del carrito a pagar

**Request:**
```json
{
  "payment_method": "CASH"
}
```

**Métodos de Pago Válidos:**
- `CASH`: Pago en efectivo
- `CARD`: Pago con tarjeta

**Respuesta (200):**
```json
{
  "message": "Pago procesado exitosamente con CASH"
}
```

**Códigos de Error:**
- `400`: Método de pago inválido o carrito no encontrado

---

## 🔄 Valores de Estado

| Estado | Descripción |
|--------|-------------|
| `ACT` | Activo - Carrito en construcción |
| `PAID` | Pagado - Pago completado |
| `CANC` | Cancelado - Carrito cancelado |

---

## 🛠️ Ejemplos de Uso

### cURL

#### Listar Productos
```bash
curl -X GET http://localhost:8000/products
```

#### Crear Producto
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "code": "SKU001",
    "price": 1299.99
  }'
```

#### Obtener Producto
```bash
curl -X GET http://localhost:8000/products/1
```

#### Actualizar Producto
```bash
curl -X PATCH http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1199.99
  }'
```

#### Eliminar Producto
```bash
curl -X DELETE http://localhost:8000/products/1
```

#### Crear Carrito
```bash
curl -X POST http://localhost:8000/carts \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 100,
    "status": "ACT",
    "total": 0.0
  }'
```

#### Agregar Producto al Carrito
```bash
curl -X POST http://localhost:8000/carts/1/products \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1
  }'
```

#### Procesar Pago
```bash
curl -X POST http://localhost:8000/carts/1/pay \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "CASH"
  }'
```

---

### JavaScript/Fetch

#### Listar Productos
```javascript
fetch('http://localhost:8000/products')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### Crear Producto
```javascript
fetch('http://localhost:8000/products', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Laptop',
    code: 'SKU001',
    price: 1299.99
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

#### Crear Carrito y Agregar Productos
```javascript
// 1. Crear carrito
const cart = await fetch('http://localhost:8000/carts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    customer_id: 100,
    status: 'ACT',
    total: 0.0
  })
}).then(r => r.json());

const cartId = cart.id;

// 2. Agregar producto
await fetch(`http://localhost:8000/carts/${cartId}/products`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ product_id: 1 })
});

// 3. Procesar pago
const payment = await fetch(`http://localhost:8000/carts/${cartId}/pay`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ payment_method: 'CASH' })
}).then(r => r.json());

console.log(payment.message);
```

---

### TypeScript/Axios

```typescript
import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Crear cliente HTTP
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interfaces
interface Product {
  id: number;
  name: string;
  code: string;
  price: number;
}

interface Cart {
  id: number;
  customer_id: number;
  status: string;
  total: number;
  products: any[];
}

// Listar productos
async function getProducts(): Promise<Product[]> {
  const response = await apiClient.get('/products');
  return response.data;
}

// Crear producto
async function createProduct(data: Omit<Product, 'id'>): Promise<Product> {
  const response = await apiClient.post('/products', data);
  return response.data;
}

// Crear carrito
async function createCart(customerId: number): Promise<Cart> {
  const response = await apiClient.post('/carts', {
    customer_id: customerId,
    status: 'ACT',
    total: 0.0
  });
  return response.data;
}

// Agregar producto al carrito
async function addProductToCart(cartId: number, productId: number): Promise<Cart> {
  const response = await apiClient.post(`/carts/${cartId}/products`, {
    product_id: productId
  });
  return response.data;
}

// Procesar pago
async function processPayment(cartId: number, method: 'CASH' | 'CARD'): Promise<{ message: string }> {
  const response = await apiClient.post(`/carts/${cartId}/pay`, {
    payment_method: method
  });
  return response.data;
}

// Uso
(async () => {
  try {
    // Obtener productos
    const products = await getProducts();
    console.log('Productos:', products);

    // Crear carrito
    const cart = await createCart(100);
    console.log('Carrito creado:', cart);

    // Agregar producto
    const updatedCart = await addProductToCart(cart.id, products[0].id);
    console.log('Carrito actualizado:', updatedCart);

    // Procesar pago
    const payment = await processPayment(cart.id, 'CASH');
    console.log('Pago procesado:', payment.message);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

---

## 📊 Modelos de Datos

### Product
```typescript
interface Product {
  id: number;        // ID único (auto-generado)
  name: string;      // Nombre del producto
  code: string;      // Código SKU único
  price: number;     // Precio unitario
}
```

### Cart
```typescript
interface Cart {
  id: number;          // ID único (auto-generado)
  customer_id: number; // ID del cliente
  status: string;      // ACT, PAID, CANC
  total: number;       // Total del carrito
  products: CartProduct[]; // Lista de productos
}

interface CartProduct {
  product_id: number;   // ID del producto
  product_name: string; // Nombre del producto
  price: number;        // Precio al momento de agregar
}
```

### Payment
```typescript
interface Payment {
  message: string; // Mensaje del resultado del pago
}
```

---

## ⚠️ Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| `200` | OK | Solicitud exitosa |
| `201` | Created | Recurso creado exitosamente |
| `204` | No Content | Operación exitosa sin contenido |
| `400` | Bad Request | Solicitud inválida |
| `404` | Not Found | Recurso no encontrado |
| `500` | Server Error | Error del servidor |

---

## 🔧 Configuración para Frontend

### CORS (Si es necesario)
Si tu frontend está en otro dominio, asegúrate de que CORS esté configurado.

**En settings.py:**
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]
```

---

## 📝 Notas para Frontend

1. **Tipificación:** Todos los endpoints retornan DTOs tipificados
2. **Validaciones:** El servidor realiza validaciones básicas
3. **IDs:** Son integers auto-generados por la base de datos
4. **Decimales:** Los precios usan punto decimal (1299.99)
5. **Estado del carrito:** Solo puede ser ACT, PAID, CANC

---

## 🚀 Próximos Pasos

- [ ] Implementar autenticación y autorización
- [ ] Agregar paginación a listados
- [ ] Implementar filtros y búsqueda
- [ ] Agregar validaciones más robustas
- [ ] Implementar caché
- [ ] Agregar rate limiting
- [ ] Implementar webhooks para eventos

---

**Última actualización:** 2026-05-06  
**Versión API:** 1.0.0  
**Maintainer:** CEMLAD Team
