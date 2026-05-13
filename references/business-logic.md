# Business Logic Testing

Esto es donde están los mejores bugs. Scanners NO los encuentran.

## Modelar antes de atacar

Para cada flujo crítico, dibujar:
- **Actores** (anónimo, cliente, premium, admin, soporte).
- **Estados** (carrito vacío → pendiente → pagado → enviado → entregado → reembolsado).
- **Transiciones permitidas** entre estados.
- **Trust boundaries** (qué valida frontend vs backend).
- **Inputs influenciables por cliente** en cada paso.

## Patrones de abuse

### Saltarse pagos
- Editar `total` en último paso.
- Cambiar `currency` (`USD` → `XYZ` que vale 0).
- Aplicar mismo coupon N veces (race).
- Modificar `quantity` a negativo (refund).
- Reusar `payment_intent_id` validado.
- Aprobar webhook propio (Stripe/Mercadopago) firmando con secret leakeado o sin verificar firma.

### Reutilizar cupones / promociones
- Race condition en aplicación.
- Reset de cupón al cambiar email asociado.
- Cupones para nuevos usuarios aplicables a cuenta vieja con email modificado.

### Modificar precios
- Backend acepta `price` desde request en vez de leer de catálogo.
- Promo code que multiplica en vez de descontar.

### Escalar privilegios horizontalmente / verticalmente
- Cambiar `role`, `tier`, `isAdmin` en perfil edit (mass assignment).
- Endpoints admin sin auth check (function-level auth — API5).
- Tokens de invitación adivinables.

### Bypass de onboarding / KYC
- Saltar pasos llamando endpoint final directamente.
- Marcar `kyc_verified=true` en mass assignment.
- Subir documento falso si solo se verifica nombre archivo.

### Transferencias ilegítimas
- Race condition (TOCTOU sobre saldo).
- Modificar `from_account_id` en body.
- Negative amount.
- Currency casting.
- Decimal/integer overflow.

### Account recovery abuse
- Reset link enviado a email controlable post-cambio.
- Token reset sin invalidación tras uso.
- MFA omitido en cuenta recuperada.

### Rating / review abuse
- N reviews por cuenta.
- Editar review propio para subir estrellas (sin bound check).
- Review sin compra previa.

## Cómo descubrirlas

1. **Mapear flujos completos** primero (carrito, checkout, recovery, etc.).
2. **Hacer preguntas hostiles**: "¿qué pasa si...?"
3. **Probar en QA con datos de prueba** — NO en prod sin permiso.
4. **Combinar con race conditions** y mass assignment.
5. **Mirar mobile API** por separado — suele tener menos restricciones que web.

## Documentación en informe

Por cada bug de lógica:
- Diagrama del flujo afectado.
- Estado inicial → acción → estado final esperado vs obtenido.
- Impacto cuantificable ("se puede generar pérdida de $X por explotación").
- PoC reproducible paso a paso.
