# Boca Reservas — producto propio

## Objetivo
Administrar partidos, socios autorizados, preferencias de sectores, estado de solicitudes y alertas. El pago de entradas se realiza exclusivamente en Boca Socios.

## Referencia pública
Entradas Boca Juniors anuncia asociación de cuentas, preferencias por sector, reservas, notificación Telegram/push y posterior pago al club. Este proyecto no copia código privado ni asume acceso a APIs internas.

## Diferenciadores
- Estado visible por partido: sin sesión, esperando apertura, disponible, selección pendiente, reserva confirmada, pago pendiente, error.
- Trazabilidad con marca de tiempo y evidencia de confirmación.
- Avisos de prueba claramente diferenciados de los reales.
- Prevención de duplicados y control de vencimientos.
- Separación estricta del proyecto Market Scale Profit.

## Fases y puertas de validación
1. **Notificación**: entrega de Telegram (verificada 2026-10-30).
2. **Disponibilidad**: identificar datos oficiales o atributos permitidos; no deducir disponibilidad únicamente de píxeles verdes.
3. **Sesión**: acceso autorizado y persistente, con recuperación manual si vence.
4. **Selección**: confirmar sector y asiento mediante interfaz oficial, sin saltar colas, CAPTCHA ni límites.
5. **Reserva**: evidencia emitida por Boca Socios (ID, estado y vencimiento); una entrada en carrito por sí sola no implica reserva.
6. **Continuidad**: proceso separado y aprobado en Render; monitoreo a cadencia compatible con el sitio; sin activar infraestructura paga sin autorización.
7. **Producción**: prueba real de extremo a extremo, notificaciones y mecanismos de parada.

## Lo que NO está implementado
No existe aún conexión validada al inventario de Boca, navegador persistente en la nube ni reserva automática. El servicio Render actual solo atiende notificaciones y diagnósticos.
