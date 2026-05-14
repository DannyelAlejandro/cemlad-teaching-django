# 🎨 Integración Frontend - Ejemplos de Código

## 📋 Tabla de Contenidos

1. [React Hooks + TypeScript](#react)
2. [Vue 3 + TypeScript](#vue3)
3. [Angular](#angular)
4. [Svelte](#svelte)
5. [HTML Vanilla + Fetch](#vanilla)

---

## <a name="react"></a>🔵 React Hooks + TypeScript

### 1. Servicio de API (api/cemlad.ts)

```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Types
export interface Product {
  id: number;
  name: string;
  code: string;
  price: number;
}

export interface CartItem {
  product_id: number;
  product_name: string;
  price: number;
}

export interface Cart {
  id: number;
  customer_id: number;
  status: 'ACT' | 'PAID' | 'CANC';
  total: number;
  products: CartItem[];
}

// API Service
class CemladAPI {
  private baseURL = API_BASE_URL;

  // PRODUCTS
  async getProducts(): Promise<Product[]> {
    const response = await fetch(`${this.baseURL}/products`);
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
  }

  async getProduct(id: number): Promise<Product> {
    const response = await fetch(`${this.baseURL}/products/${id}`);
    if (!response.ok) throw new Error('Product not found');
    return response.json();
  }

  async createProduct(data: Omit<Product, 'id'>): Promise<Product> {
    const response = await fetch(`${this.baseURL}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create product');
    return response.json();
  }

  async updateProduct(id: number, data: Partial<Product>): Promise<Product> {
    const response = await fetch(`${this.baseURL}/products/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update product');
    return response.json();
  }

  async deleteProduct(id: number): Promise<void> {
    const response = await fetch(`${this.baseURL}/products/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete product');
  }

  // CARTS
  async getCarts(): Promise<Cart[]> {
    const response = await fetch(`${this.baseURL}/carts`);
    if (!response.ok) throw new Error('Failed to fetch carts');
    return response.json();
  }

  async getCart(id: number): Promise<Cart> {
    const response = await fetch(`${this.baseURL}/carts/${id}`);
    if (!response.ok) throw new Error('Cart not found');
    return response.json();
  }

  async createCart(customerId: number): Promise<Cart> {
    const response = await fetch(`${this.baseURL}/carts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_id: customerId,
        status: 'ACT',
        total: 0.0,
      }),
    });
    if (!response.ok) throw new Error('Failed to create cart');
    return response.json();
  }

  async addProductToCart(cartId: number, productId: number): Promise<Cart> {
    const response = await fetch(`${this.baseURL}/carts/${cartId}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId }),
    });
    if (!response.ok) throw new Error('Failed to add product to cart');
    return response.json();
  }

  async removeProductFromCart(cartId: number, productId: number): Promise<Cart> {
    const response = await fetch(`${this.baseURL}/carts/${cartId}/products/${productId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to remove product from cart');
    return response.json();
  }

  async processPayment(cartId: number, paymentMethod: 'CASH' | 'CARD'): Promise<{ message: string }> {
    const response = await fetch(`${this.baseURL}/carts/${cartId}/pay`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ payment_method: paymentMethod }),
    });
    if (!response.ok) throw new Error('Failed to process payment');
    return response.json();
  }
}

export const api = new CemladAPI();
```

### 2. Hook personalizado (hooks/useCart.ts)

```typescript
import { useState, useCallback } from 'react';
import { Cart, Product } from '../api/cemlad';
import { api } from '../api/cemlad';

export function useCart(customerId: number) {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createCart = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const newCart = await api.createCart(customerId);
      setCart(newCart);
      return newCart;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [customerId]);

  const loadCart = useCallback(async (cartId: number) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getCart(cartId);
      setCart(data);
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  const addProduct = useCallback(
    async (productId: number) => {
      if (!cart) {
        setError('No cart selected');
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const updated = await api.addProductToCart(cart.id, productId);
        setCart(updated);
        return updated;
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    },
    [cart]
  );

  const removeProduct = useCallback(
    async (productId: number) => {
      if (!cart) {
        setError('No cart selected');
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const updated = await api.removeProductFromCart(cart.id, productId);
        setCart(updated);
        return updated;
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    },
    [cart]
  );

  const checkout = useCallback(
    async (paymentMethod: 'CASH' | 'CARD') => {
      if (!cart) {
        setError('No cart selected');
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const result = await api.processPayment(cart.id, paymentMethod);
        // Actualizar estado del carrito a PAID
        setCart({ ...cart, status: 'PAID' });
        return result;
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    },
    [cart]
  );

  return {
    cart,
    loading,
    error,
    createCart,
    loadCart,
    addProduct,
    removeProduct,
    checkout,
  };
}
```

### 3. Componente Shopping Cart (components/ShoppingCart.tsx)

```typescript
import React, { useEffect } from 'react';
import { useCart } from '../hooks/useCart';
import { api, Product } from '../api/cemlad';

interface ShoppingCartProps {
  customerId: number;
  cartId?: number;
}

export function ShoppingCart({ customerId, cartId }: ShoppingCartProps) {
  const [products, setProducts] = React.useState<Product[]>([]);
  const { cart, loading, error, createCart, loadCart, addProduct, removeProduct, checkout } =
    useCart(customerId);

  // Cargar productos disponibles
  useEffect(() => {
    api.getProducts().then(setProducts);
  }, []);

  // Inicializar carrito
  useEffect(() => {
    if (cartId) {
      loadCart(cartId);
    } else {
      createCart();
    }
  }, [cartId, createCart, loadCart]);

  if (!cart) return <div>Inicializando carrito...</div>;

  return (
    <div className="shopping-cart">
      <h1>Carrito de Compras</h1>

      {error && <div className="error">{error}</div>}

      {/* Productos Disponibles */}
      <section className="available-products">
        <h2>Productos Disponibles</h2>
        <ul>
          {products.map((product) => (
            <li key={product.id}>
              <span>{product.name}</span>
              <span>${product.price}</span>
              <button onClick={() => addProduct(product.id)} disabled={loading}>
                Agregar
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* Productos en el Carrito */}
      <section className="cart-items">
        <h2>Items en el Carrito ({cart.products.length})</h2>
        {cart.products.length === 0 ? (
          <p>El carrito está vacío</p>
        ) : (
          <>
            <ul>
              {cart.products.map((item) => (
                <li key={item.product_id}>
                  <span>{item.product_name}</span>
                  <span>${item.price}</span>
                  <button onClick={() => removeProduct(item.product_id)} disabled={loading}>
                    Eliminar
                  </button>
                </li>
              ))}
            </ul>
            <div className="cart-total">
              <strong>Total: ${cart.total.toFixed(2)}</strong>
            </div>
          </>
        )}
      </section>

      {/* Pago */}
      <section className="checkout">
        <h2>Pago</h2>
        <button
          onClick={() => checkout('CASH')}
          disabled={loading || cart.products.length === 0}
        >
          Pagar con Efectivo
        </button>
        <button
          onClick={() => checkout('CARD')}
          disabled={loading || cart.products.length === 0}
        >
          Pagar con Tarjeta
        </button>
      </section>

      {/* Estado */}
      <div className="cart-status">
        <p>Estado del carrito: <strong>{cart.status}</strong></p>
        <p>Cargando: {loading ? 'Sí' : 'No'}</p>
      </div>
    </div>
  );
}
```

---

## <a name="vue3"></a>🟢 Vue 3 + TypeScript (Composition API)

### 1. Composable (composables/useCart.ts)

```typescript
import { ref, computed } from 'vue';
import { Cart, Product } from '../api/cemlad';
import { api } from '../api/cemlad';

export function useCart(customerId: number) {
  const cart = ref<Cart | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const createCart = async () => {
    loading.value = true;
    error.value = null;
    try {
      cart.value = await api.createCart(customerId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      loading.value = false;
    }
  };

  const loadCart = async (cartId: number) => {
    loading.value = true;
    error.value = null;
    try {
      cart.value = await api.getCart(cartId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      loading.value = false;
    }
  };

  const addProduct = async (productId: number) => {
    if (!cart.value) return;
    loading.value = true;
    error.value = null;
    try {
      cart.value = await api.addProductToCart(cart.value.id, productId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      loading.value = false;
    }
  };

  const removeProduct = async (productId: number) => {
    if (!cart.value) return;
    loading.value = true;
    error.value = null;
    try {
      cart.value = await api.removeProductFromCart(cart.value.id, productId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      loading.value = false;
    }
  };

  const checkout = async (paymentMethod: 'CASH' | 'CARD') => {
    if (!cart.value) return;
    loading.value = true;
    error.value = null;
    try {
      const result = await api.processPayment(cart.value.id, paymentMethod);
      if (cart.value) cart.value.status = 'PAID';
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      loading.value = false;
    }
  };

  const cartTotal = computed(() => cart.value?.total ?? 0);
  const itemCount = computed(() => cart.value?.products.length ?? 0);

  return {
    cart,
    loading,
    error,
    cartTotal,
    itemCount,
    createCart,
    loadCart,
    addProduct,
    removeProduct,
    checkout,
  };
}
```

### 2. Componente ShoppingCart (components/ShoppingCart.vue)

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useCart } from '../composables/useCart';
import { api, type Product } from '../api/cemlad';

interface Props {
  customerId: number;
  cartId?: number;
}

const props = defineProps<Props>();

const products = ref<Product[]>([]);
const { cart, loading, error, createCart, loadCart, addProduct, removeProduct, checkout } =
  useCart(props.customerId);

onMounted(async () => {
  // Cargar productos disponibles
  products.value = await api.getProducts();

  // Inicializar carrito
  if (props.cartId) {
    await loadCart(props.cartId);
  } else {
    await createCart();
  }
});

const handleCheckout = async (method: 'CASH' | 'CARD') => {
  await checkout(method);
};
</script>

<template>
  <div class="shopping-cart">
    <h1>Carrito de Compras</h1>

    <div v-if="error" class="error">{{ error }}</div>

    <!-- Productos Disponibles -->
    <section class="available-products">
      <h2>Productos Disponibles</h2>
      <ul>
        <li v-for="product in products" :key="product.id">
          <span>{{ product.name }}</span>
          <span>${{ product.price }}</span>
          <button @click="addProduct(product.id)" :disabled="loading">
            Agregar
          </button>
        </li>
      </ul>
    </section>

    <!-- Productos en el Carrito -->
    <section v-if="cart" class="cart-items">
      <h2>Items en el Carrito ({{ cart.products.length }})</h2>
      <div v-if="cart.products.length === 0">
        <p>El carrito está vacío</p>
      </div>
      <div v-else>
        <ul>
          <li v-for="item in cart.products" :key="item.product_id">
            <span>{{ item.product_name }}</span>
            <span>${{ item.price }}</span>
            <button @click="removeProduct(item.product_id)" :disabled="loading">
              Eliminar
            </button>
          </li>
        </ul>
        <div class="cart-total">
          <strong>Total: ${{ cart.total.toFixed(2) }}</strong>
        </div>
      </div>
    </section>

    <!-- Pago -->
    <section v-if="cart" class="checkout">
      <h2>Pago</h2>
      <button
        @click="handleCheckout('CASH')"
        :disabled="loading || cart.products.length === 0"
      >
        Pagar con Efectivo
      </button>
      <button
        @click="handleCheckout('CARD')"
        :disabled="loading || cart.products.length === 0"
      >
        Pagar con Tarjeta
      </button>
    </section>

    <!-- Estado -->
    <div v-if="cart" class="cart-status">
      <p>Estado del carrito: <strong>{{ cart.status }}</strong></p>
      <p>Cargando: {{ loading ? 'Sí' : 'No' }}</p>
    </div>
  </div>
</template>

<style scoped>
.shopping-cart {
  max-width: 1200px;
  margin: 0 auto;
}

section {
  margin: 2rem 0;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}

button {
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 4px;
}
</style>
```

---

## <a name="angular"></a>🔴 Angular

### 1. Servicio (services/cemlad.service.ts)

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../environments/environment';

export interface Product {
  id: number;
  name: string;
  code: string;
  price: number;
}

export interface CartItem {
  product_id: number;
  product_name: string;
  price: number;
}

export interface Cart {
  id: number;
  customer_id: number;
  status: 'ACT' | 'PAID' | 'CANC';
  total: number;
  products: CartItem[];
}

@Injectable({
  providedIn: 'root',
})
export class CemladService {
  private apiUrl = environment.apiUrl || 'http://localhost:8000';
  private cartSubject = new BehaviorSubject<Cart | null>(null);

  public cart$ = this.cartSubject.asObservable();

  constructor(private http: HttpClient) {}

  // PRODUCTS
  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/products`);
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/products/${id}`);
  }

  createProduct(data: Omit<Product, 'id'>): Observable<Product> {
    return this.http.post<Product>(`${this.apiUrl}/products`, data);
  }

  updateProduct(id: number, data: Partial<Product>): Observable<Product> {
    return this.http.patch<Product>(`${this.apiUrl}/products/${id}`, data);
  }

  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/products/${id}`);
  }

  // CARTS
  getCarts(): Observable<Cart[]> {
    return this.http.get<Cart[]>(`${this.apiUrl}/carts`);
  }

  getCart(id: number): Observable<Cart> {
    return this.http.get<Cart>(`${this.apiUrl}/carts/${id}`);
  }

  createCart(customerId: number): Observable<Cart> {
    return this.http.post<Cart>(`${this.apiUrl}/carts`, {
      customer_id: customerId,
      status: 'ACT',
      total: 0.0,
    });
  }

  addProductToCart(cartId: number, productId: number): Observable<Cart> {
    return this.http.post<Cart>(`${this.apiUrl}/carts/${cartId}/products`, {
      product_id: productId,
    });
  }

  removeProductFromCart(cartId: number, productId: number): Observable<Cart> {
    return this.http.delete<Cart>(
      `${this.apiUrl}/carts/${cartId}/products/${productId}`
    );
  }

  processPayment(cartId: number, paymentMethod: 'CASH' | 'CARD'): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(
      `${this.apiUrl}/carts/${cartId}/pay`,
      { payment_method: paymentMethod }
    );
  }

  // Helper para actualizar el carrito observable
  updateCart(cart: Cart): void {
    this.cartSubject.next(cart);
  }

  getCartValue(): Cart | null {
    return this.cartSubject.value;
  }
}
```

### 2. Componente ShoppingCart (shopping-cart.component.ts)

```typescript
import { Component, OnInit } from '@angular/core';
import { CemladService, Product, Cart } from '../services/cemlad.service';

@Component({
  selector: 'app-shopping-cart',
  templateUrl: './shopping-cart.component.html',
  styleUrls: ['./shopping-cart.component.css'],
})
export class ShoppingCartComponent implements OnInit {
  products: Product[] = [];
  cart: Cart | null = null;
  loading = false;
  error: string | null = null;
  customerId = 100;

  constructor(private cemladService: CemladService) {}

  ngOnInit(): void {
    this.loadProducts();
    this.createCart();
    this.cemladService.cart$.subscribe((cart) => {
      this.cart = cart;
    });
  }

  loadProducts(): void {
    this.loading = true;
    this.cemladService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error loading products';
        this.loading = false;
      },
    });
  }

  createCart(): void {
    this.loading = true;
    this.cemladService.createCart(this.customerId).subscribe({
      next: (cart) => {
        this.cemladService.updateCart(cart);
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error creating cart';
        this.loading = false;
      },
    });
  }

  addProduct(productId: number): void {
    if (!this.cart) return;
    this.loading = true;
    this.cemladService.addProductToCart(this.cart.id, productId).subscribe({
      next: (updatedCart) => {
        this.cemladService.updateCart(updatedCart);
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error adding product';
        this.loading = false;
      },
    });
  }

  removeProduct(productId: number): void {
    if (!this.cart) return;
    this.loading = true;
    this.cemladService.removeProductFromCart(this.cart.id, productId).subscribe({
      next: (updatedCart) => {
        this.cemladService.updateCart(updatedCart);
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error removing product';
        this.loading = false;
      },
    });
  }

  checkout(paymentMethod: 'CASH' | 'CARD'): void {
    if (!this.cart) return;
    this.loading = true;
    this.cemladService.processPayment(this.cart.id, paymentMethod).subscribe({
      next: (result) => {
        if (this.cart) {
          this.cart.status = 'PAID';
          this.cemladService.updateCart(this.cart);
        }
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error processing payment';
        this.loading = false;
      },
    });
  }
}
```

### 3. Template (shopping-cart.component.html)

```html
<div class="shopping-cart">
  <h1>Carrito de Compras</h1>

  <div *ngIf="error" class="alert alert-danger">{{ error }}</div>

  <!-- Productos Disponibles -->
  <section class="available-products">
    <h2>Productos Disponibles</h2>
    <ul>
      <li *ngFor="let product of products">
        <span>{{ product.name }}</span>
        <span>${{ product.price }}</span>
        <button (click)="addProduct(product.id)" [disabled]="loading">
          Agregar
        </button>
      </li>
    </ul>
  </section>

  <!-- Productos en el Carrito -->
  <section class="cart-items" *ngIf="cart">
    <h2>Items en el Carrito ({{ cart.products.length }})</h2>
    <div *ngIf="cart.products.length === 0">
      <p>El carrito está vacío</p>
    </div>
    <div *ngIf="cart.products.length > 0">
      <ul>
        <li *ngFor="let item of cart.products">
          <span>{{ item.product_name }}</span>
          <span>${{ item.price }}</span>
          <button (click)="removeProduct(item.product_id)" [disabled]="loading">
            Eliminar
          </button>
        </li>
      </ul>
      <div class="cart-total">
        <strong>Total: ${{ cart.total | number : '1.2-2' }}</strong>
      </div>
    </div>
  </section>

  <!-- Pago -->
  <section class="checkout" *ngIf="cart">
    <h2>Pago</h2>
    <button
      (click)="checkout('CASH')"
      [disabled]="loading || cart.products.length === 0"
    >
      Pagar con Efectivo
    </button>
    <button
      (click)="checkout('CARD')"
      [disabled]="loading || cart.products.length === 0"
    >
      Pagar con Tarjeta
    </button>
  </section>

  <!-- Estado -->
  <div class="cart-status" *ngIf="cart">
    <p>Estado del carrito: <strong>{{ cart.status }}</strong></p>
    <p>Cargando: {{ loading ? 'Sí' : 'No' }}</p>
  </div>
</div>
```

---

## <a name="svelte"></a>⚫ Svelte

### Componente ShoppingCart (ShoppingCart.svelte)

```svelte
<script>
  import { onMount } from 'svelte';
  import { api } from '../api/cemlad.js';

  export let customerId = 100;
  export let cartId = undefined;

  let products = [];
  let cart = null;
  let loading = false;
  let error = null;

  onMount(async () => {
    try {
      // Cargar productos
      products = await api.getProducts();

      // Inicializar carrito
      if (cartId) {
        cart = await api.getCart(cartId);
      } else {
        cart = await api.createCart(customerId);
      }
    } catch (err) {
      error = 'Error loading data';
    }
  });

  async function addProduct(productId) {
    if (!cart) return;
    loading = true;
    try {
      cart = await api.addProductToCart(cart.id, productId);
    } catch (err) {
      error = 'Error adding product';
    } finally {
      loading = false;
    }
  }

  async function removeProduct(productId) {
    if (!cart) return;
    loading = true;
    try {
      cart = await api.removeProductFromCart(cart.id, productId);
    } catch (err) {
      error = 'Error removing product';
    } finally {
      loading = false;
    }
  }

  async function checkout(paymentMethod) {
    if (!cart) return;
    loading = true;
    try {
      await api.processPayment(cart.id, paymentMethod);
      cart.status = 'PAID';
      cart = cart; // Trigger reactivity
    } catch (err) {
      error = 'Error processing payment';
    } finally {
      loading = false;
    }
  }
</script>

<div class="shopping-cart">
  <h1>Carrito de Compras</h1>

  {#if error}
    <div class="alert alert-danger">{error}</div>
  {/if}

  <!-- Productos Disponibles -->
  <section class="available-products">
    <h2>Productos Disponibles</h2>
    <ul>
      {#each products as product (product.id)}
        <li>
          <span>{product.name}</span>
          <span>${product.price}</span>
          <button on:click={() => addProduct(product.id)} disabled={loading}>
            Agregar
          </button>
        </li>
      {/each}
    </ul>
  </section>

  <!-- Productos en el Carrito -->
  {#if cart}
    <section class="cart-items">
      <h2>Items en el Carrito ({cart.products.length})</h2>
      {#if cart.products.length === 0}
        <p>El carrito está vacío</p>
      {:else}
        <ul>
          {#each cart.products as item (item.product_id)}
            <li>
              <span>{item.product_name}</span>
              <span>${item.price}</span>
              <button on:click={() => removeProduct(item.product_id)} disabled={loading}>
                Eliminar
              </button>
            </li>
          {/each}
        </ul>
        <div class="cart-total">
          <strong>Total: ${cart.total.toFixed(2)}</strong>
        </div>
      {/if}
    </section>

    <!-- Pago -->
    <section class="checkout">
      <h2>Pago</h2>
      <button
        on:click={() => checkout('CASH')}
        disabled={loading || cart.products.length === 0}
      >
        Pagar con Efectivo
      </button>
      <button
        on:click={() => checkout('CARD')}
        disabled={loading || cart.products.length === 0}
      >
        Pagar con Tarjeta
      </button>
    </section>

    <!-- Estado -->
    <div class="cart-status">
      <p>Estado del carrito: <strong>{cart.status}</strong></p>
      <p>Cargando: {loading ? 'Sí' : 'No'}</p>
    </div>
  {/if}
</div>

<style>
  .shopping-cart {
    max-width: 1200px;
    margin: 0 auto;
  }

  section {
    margin: 2rem 0;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    border-bottom: 1px solid #eee;
  }

  button {
    padding: 0.5rem 1rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .alert-danger {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 0.75rem;
    border-radius: 4px;
  }
</style>
```

---

## <a name="vanilla"></a>🟡 HTML Vanilla + Fetch

### HTML (index.html)

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CEMLAD - Carrito de Compras</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f5f5f5;
        padding: 20px;
      }

      .container {
        max-width: 1200px;
        margin: 0 auto;
      }

      h1 {
        margin-bottom: 20px;
        color: #333;
      }

      h2 {
        margin-top: 20px;
        margin-bottom: 15px;
        color: #555;
        font-size: 1.5em;
      }

      section {
        background: white;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }

      ul {
        list-style: none;
      }

      li {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px;
        border-bottom: 1px solid #eee;
      }

      li:last-child {
        border-bottom: none;
      }

      button {
        padding: 8px 16px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
      }

      button:hover {
        background-color: #0056b3;
      }

      button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
      }

      .alert {
        padding: 15px;
        margin: 15px 0;
        border-radius: 4px;
        display: none;
      }

      .alert.show {
        display: block;
      }

      .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
      }

      .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
      }

      .cart-total {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 2px solid #007bff;
        font-size: 1.2em;
        text-align: right;
      }

      .cart-status {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 4px;
        margin-top: 20px;
      }

      .loading {
        opacity: 0.6;
        pointer-events: none;
      }

      .spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #007bff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
      }

      @keyframes spin {
        0% {
          transform: rotate(0deg);
        }
        100% {
          transform: rotate(360deg);
        }
      }

      .flex-item {
        flex: 1;
      }

      .action-buttons {
        display: flex;
        gap: 10px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>🛒 Carrito de Compras - CEMLAD API</h1>

      <!-- Alertas -->
      <div id="alert" class="alert"></div>

      <!-- Productos Disponibles -->
      <section>
        <h2>Productos Disponibles</h2>
        <ul id="products-list"></ul>
      </section>

      <!-- Carrito de Compras -->
      <section>
        <h2>Items en el Carrito (<span id="cart-count">0</span>)</h2>
        <div id="cart-empty" style="text-align: center; color: #999;">
          El carrito está vacío
        </div>
        <ul id="cart-items" style="display: none;"></ul>
        <div id="cart-total" class="cart-total" style="display: none;">
          Total: $<span id="total-amount">0.00</span>
        </div>
      </section>

      <!-- Pago -->
      <section id="checkout-section" style="display: none;">
        <h2>Pago</h2>
        <div class="action-buttons">
          <button onclick="checkout('CASH')">💵 Pagar con Efectivo</button>
          <button onclick="checkout('CARD')">💳 Pagar con Tarjeta</button>
        </div>
      </section>

      <!-- Estado -->
      <section class="cart-status" id="cart-status" style="display: none;">
        <p>Estado del carrito: <strong id="cart-state">ACT</strong></p>
        <p>ID del carrito: <strong id="cart-id">-</strong></p>
      </section>
    </div>

    <script src="app.js"></script>
  </body>
</html>
```

### JavaScript (app.js)

```javascript
const API_URL = 'http://localhost:8000';
const CUSTOMER_ID = 100;

let state = {
  cart: null,
  products: [],
  loading: false,
};

// Utilidades
function showAlert(message, type = 'danger') {
  const alertEl = document.getElementById('alert');
  alertEl.textContent = message;
  alertEl.className = `alert show alert-${type}`;
  setTimeout(() => {
    alertEl.classList.remove('show');
  }, 5000);
}

function setLoading(isLoading) {
  state.loading = isLoading;
  document.querySelectorAll('button').forEach((btn) => {
    btn.disabled = isLoading;
  });
}

// API Calls
async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    showAlert(error.message || 'Error de conexión');
    throw error;
  }
}

// Cargar productos
async function loadProducts() {
  setLoading(true);
  try {
    state.products = await apiCall('/products');
    renderProducts();
  } finally {
    setLoading(false);
  }
}

// Crear carrito
async function createCart() {
  setLoading(true);
  try {
    state.cart = await apiCall('/carts', {
      method: 'POST',
      body: JSON.stringify({
        customer_id: CUSTOMER_ID,
        status: 'ACT',
        total: 0.0,
      }),
    });
    renderCart();
  } finally {
    setLoading(false);
  }
}

// Agregar producto al carrito
async function addProductToCart(productId) {
  if (!state.cart) return;
  setLoading(true);
  try {
    state.cart = await apiCall(`/carts/${state.cart.id}/products`, {
      method: 'POST',
      body: JSON.stringify({ product_id: productId }),
    });
    renderCart();
    showAlert('Producto agregado', 'success');
  } finally {
    setLoading(false);
  }
}

// Eliminar producto del carrito
async function removeProductFromCart(productId) {
  if (!state.cart) return;
  setLoading(true);
  try {
    state.cart = await apiCall(`/carts/${state.cart.id}/products/${productId}`, {
      method: 'DELETE',
    });
    renderCart();
    showAlert('Producto eliminado', 'success');
  } finally {
    setLoading(false);
  }
}

// Procesar pago
async function checkout(paymentMethod) {
  if (!state.cart) return;
  setLoading(true);
  try {
    const result = await apiCall(`/carts/${state.cart.id}/pay`, {
      method: 'POST',
      body: JSON.stringify({ payment_method: paymentMethod }),
    });
    state.cart.status = 'PAID';
    renderCart();
    showAlert(`Pago procesado: ${result.message}`, 'success');
  } finally {
    setLoading(false);
  }
}

// Renderizar
function renderProducts() {
  const list = document.getElementById('products-list');
  list.innerHTML = state.products
    .map(
      (product) => `
    <li>
      <span class="flex-item">${product.name}</span>
      <span>$${product.price.toFixed(2)}</span>
      <button onclick="addProductToCart(${product.id})">Agregar</button>
    </li>
  `
    )
    .join('');
}

function renderCart() {
  if (!state.cart) return;

  const cartCount = document.getElementById('cart-count');
  const cartEmpty = document.getElementById('cart-empty');
  const cartItems = document.getElementById('cart-items');
  const cartTotal = document.getElementById('cart-total');
  const checkoutSection = document.getElementById('checkout-section');
  const cartStatus = document.getElementById('cart-status');

  cartCount.textContent = state.cart.products.length;

  if (state.cart.products.length === 0) {
    cartEmpty.style.display = 'block';
    cartItems.style.display = 'none';
    cartTotal.style.display = 'none';
    checkoutSection.style.display = 'none';
  } else {
    cartEmpty.style.display = 'none';
    cartItems.style.display = 'block';
    cartTotal.style.display = 'block';
    checkoutSection.style.display = 'block';

    cartItems.innerHTML = state.cart.products
      .map(
        (item) => `
      <li>
        <span class="flex-item">${item.product_name}</span>
        <span>$${item.price.toFixed(2)}</span>
        <button onclick="removeProductFromCart(${item.product_id})">Eliminar</button>
      </li>
    `
      )
      .join('');

    document.getElementById('total-amount').textContent = state.cart.total.toFixed(2);
  }

  // Actualizar estado
  cartStatus.style.display = 'block';
  document.getElementById('cart-state').textContent = state.cart.status;
  document.getElementById('cart-id').textContent = state.cart.id;
}

// Inicializar
async function init() {
  await loadProducts();
  await createCart();
}

// Ejecutar al cargar
window.addEventListener('DOMContentLoaded', init);
```

---

## 📌 Resumen

| Framework | Complejidad | Recomendado Para |
|-----------|------------|-----------------|
| React | Media-Alta | Aplicaciones grandes, escalables |
| Vue 3 | Media | Proyecto de mediano tamaño |
| Angular | Alta | Aplicaciones empresariales |
| Svelte | Baja-Media | Proyectos rápidos, reactivos |
| Vanilla | Baja | Prototipos, demos rápidas |

---

**Última actualización:** 2026-05-06
