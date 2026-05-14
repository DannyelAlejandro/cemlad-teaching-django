# 🚀 Setup Guide - Frontend Developers

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos)
2. [Configuración Inicial del Backend](#backend-setup)
3. [Proyectos Frontend](#proyectos-frontend)
4. [Testing & Debugging](#testing)
5. [Deployment](#deployment)

---

## <a name="requisitos"></a>✅ Requisitos Previos

### Backend (Django)
- Python 3.8+
- pip (package manager)
- MySQL o MariaDB
- Git

### Frontend (Elije uno)
- Node.js 16+ + npm/yarn/pnpm
- Git

---

## <a name="backend-setup"></a>⚙️ Configuración Inicial del Backend

### 1️⃣ Clonar Repositorio

```bash
git clone <tu-repo-url>
cd learning
```

### 2️⃣ Crear Entorno Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Django
APP_SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion
APP_DEBUG=true
APP_LANGUAGE_CODE=es-es
APP_TIME_ZONE=America/Bogota

# Base de datos MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=learning
DB_USERNAME=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

### 5️⃣ Ejecutar Migraciones

```bash
python manage.py migrate
```

### 6️⃣ Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 7️⃣ Cargar Datos Iniciales (Opcional)

Crear archivo `fixtures.json` con productos iniciales:

```json
{
  "products": [
    {
      "name": "Laptop Dell XPS 13",
      "code": "SKU001",
      "price": 1299.99
    },
    {
      "name": "Mouse Logitech MX Master",
      "code": "SKU002",
      "price": 99.99
    },
    {
      "name": "Teclado Mecánico Corsair",
      "code": "SKU003",
      "price": 149.99
    },
    {
      "name": "Monitor LG 27\"",
      "code": "SKU004",
      "price": 329.99
    },
    {
      "name": "Cable USB-C",
      "code": "SKU005",
      "price": 29.99
    }
  ]
}
```

### 8️⃣ Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

**Verificar que esté funcionando:**
```
http://localhost:8000/
http://localhost:8000/api/docs/  (Swagger UI)
```

---

## <a name="proyectos-frontend"></a>🎨 Proyectos Frontend

### 🔵 React + TypeScript (Recomendado)

#### Crear Proyecto

```bash
npx create-react-app cemlad-frontend --template typescript
cd cemlad-frontend
npm install axios
```

#### Crear archivo `.env.local`

```env
REACT_APP_API_URL=http://localhost:8000
```

#### Estructura de Carpetas

```
src/
├── api/
│   └── cemlad.ts          # Cliente HTTP
├── components/
│   ├── ProductList.tsx
│   ├── ShoppingCart.tsx
│   └── Checkout.tsx
├── hooks/
│   ├── useCart.ts
│   ├── useProducts.ts
│   └── usePayment.ts
├── pages/
│   ├── Home.tsx
│   ├── Products.tsx
│   └── Cart.tsx
├── types/
│   └── index.ts           # Interfaces TypeScript
├── App.tsx
└── index.tsx
```

#### Ejemplo de Hook Personalizado

```typescript
// src/hooks/useProducts.ts
import { useState, useEffect } from 'react';
import { api, Product } from '../api/cemlad';

export function useProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    api.getProducts()
      .then(setProducts)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { products, loading, error };
}
```

#### Ejecutar Desarrollo

```bash
npm start
```

---

### 🟢 Vue 3 + TypeScript

#### Crear Proyecto

```bash
npm init vue@latest cemlad-frontend
cd cemlad-frontend
npm install axios
npm run dev
```

#### Estructura de Carpetas

```
src/
├── api/
│   └── cemlad.ts
├── components/
│   ├── ProductList.vue
│   ├── ShoppingCart.vue
│   └── Checkout.vue
├── composables/
│   ├── useCart.ts
│   ├── useProducts.ts
│   └── usePayment.ts
├── views/
│   ├── HomeView.vue
│   ├── ProductsView.vue
│   └── CartView.vue
├── types/
│   └── index.ts
├── App.vue
└── main.ts
```

---

### 🔴 Angular

#### Crear Proyecto

```bash
ng new cemlad-frontend
cd cemlad-frontend
ng add @angular/material  # Opcional: UI Framework
```

#### Estructura de Carpetas

```
src/
├── app/
│   ├── services/
│   │   └── cemlad.service.ts
│   ├── components/
│   │   ├── product-list/
│   │   ├── shopping-cart/
│   │   └── checkout/
│   ├── pages/
│   │   ├── home/
│   │   ├── products/
│   │   └── cart/
│   ├── models/
│   │   └── index.ts
│   └── app.component.ts
└── environments/
    ├── environment.ts
    └── environment.prod.ts
```

#### Configurar Entorno

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

---

### ⚫ Svelte

#### Crear Proyecto

```bash
npm create vite@latest cemlad-frontend -- --template svelte
cd cemlad-frontend
npm install
npm run dev
```

---

## <a name="testing"></a>🧪 Testing & Debugging

### Probar Endpoints con Postman

1. Descarga [Postman](https://www.postman.com/downloads/)
2. Importar colección: [Archivo Postman Collection](#postman-collection)

#### Crear Producto

```
POST http://localhost:8000/products
Content-Type: application/json

{
  "name": "Producto Prueba",
  "code": "TEST001",
  "price": 99.99
}
```

#### Listar Productos

```
GET http://localhost:8000/products
```

#### Crear Carrito

```
POST http://localhost:8000/carts
Content-Type: application/json

{
  "customer_id": 1,
  "status": "ACT",
  "total": 0.0
}
```

#### Agregar Producto al Carrito

```
POST http://localhost:8000/carts/1/products
Content-Type: application/json

{
  "product_id": 1
}
```

#### Procesar Pago

```
POST http://localhost:8000/carts/1/pay
Content-Type: application/json

{
  "payment_method": "CASH"
}
```

### Swagger UI

Acceder a la documentación interactiva:

```
http://localhost:8000/api/docs/
```

Aquí puedes:
- ✅ Ver todos los endpoints
- ✅ Probar endpoints directamente
- ✅ Ver esquemas de request/response
- ✅ Descargar OpenAPI spec

### Console/DevTools del Navegador

```javascript
// En la consola del navegador (Frontend)

// Obtener todos los productos
fetch('http://localhost:8000/products')
  .then(r => r.json())
  .then(console.log);

// Crear carrito
fetch('http://localhost:8000/carts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    customer_id: 1,
    status: 'ACT',
    total: 0.0
  })
})
  .then(r => r.json())
  .then(console.log);
```

### Debugging con VS Code

#### Configurar Debugger para Chrome

`.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/src",
      "sourceMaps": true
    }
  ]
}
```

#### Breakpoints

1. Abre DevTools (F12)
2. Ve a la pestaña "Sources"
3. Encuentra tu archivo .ts
4. Haz clic en el número de línea para agregar breakpoint

---

## <a name="deployment"></a>🚀 Deployment

### Backend (Django)

#### Preparar para Producción

```bash
# Generar requirements.txt
pip freeze > requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear datos de respaldo
python manage.py dumpdata > backup.json
```

#### Opciones de Hosting

- **Heroku**: [deploy-to-heroku.md](#)
- **PythonAnywhere**: [pythonanywhere-setup.md](#)
- **DigitalOcean**: [digitalocean-setup.md](#)
- **AWS**: [aws-setup.md](#)

### Frontend

#### React

```bash
# Build para producción
npm run build

# Servir localmente (simular producción)
npm install -g serve
serve -s build

# Opciones de hosting
# - Netlify (npm install -D netlify-cli)
# - Vercel (npm i -g vercel && vercel)
# - GitHub Pages
# - AWS S3 + CloudFront
```

#### Vue 3

```bash
# Build
npm run build

# Preview build
npm run preview
```

#### Angular

```bash
# Build
ng build --configuration production

# Servir
npm install -g http-server
http-server -c-1 -o dist/cemlad-frontend/
```

---

## 📚 Recursos Útiles

### Documentación Oficial

- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [React Documentation](https://react.dev/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Angular Documentation](https://angular.io/)

### Tutoriales

- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [React TypeScript Handbook](https://react-typescript-cheatsheet.netlify.app/)
- [Vue Awesome](https://github.com/vuejs/awesome-vue)

### Herramientas

- [Postman](https://www.postman.com/) - API Testing
- [VS Code](https://code.visualstudio.com/) - Editor
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - API Documentation
- [Git](https://git-scm.com/) - Version Control

---

## 🐛 Troubleshooting

### CORS Error

**Problema:** `Access to XMLHttpRequest blocked by CORS policy`

**Solución en Django:**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5173",  # Vite
]
```

### Port Already in Use

```bash
# Cambiar puerto Django
python manage.py runserver 8001

# Cambiar puerto frontend (React)
PORT=3001 npm start
```

### Database Connection Error

```bash
# Verificar MySQL está corriendo
# Linux/Mac
brew services list

# Windows
Get-Service | where {$_.Name -like "*MySQL*"}

# Verificar credenciales en .env
```

### Module Not Found

```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
npm install
```

---

## ✨ Próximos Pasos

1. ✅ Descarga este guía
2. ✅ Configura el backend
3. ✅ Prueba endpoints en Swagger UI
4. ✅ Elige tu framework frontend
5. ✅ Comienza a desarrollar
6. ✅ Prueba localmente
7. ✅ Deploy a producción

---

## 📞 Soporte

- **Documentación API**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Ejemplos Frontend**: [FRONTEND_EXAMPLES.md](FRONTEND_EXAMPLES.md)
- **Swagger UI**: http://localhost:8000/api/docs/
- **GitHub Issues**: [Link a Issues](#)

---

**Última actualización:** 2026-05-06  
**Mantenedor:** CEMLAD Team
