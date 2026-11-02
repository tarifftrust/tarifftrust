# US duties of a cart, from an e-commerce backend

A small server, with only Node.js and the `tarifftrust` package, that your store's backend calls with
a cart. It looks each SKU's customs fields up in your catalog and estimates the cart as one US import
declaration, so the fees count once.

```bash
npm install tarifftrust
TARIFFTRUST_API_KEY=tarifftrust_... node server.mjs
curl -X POST localhost:3000/duties -d '{"lines":[{"sku":"TEE-001","quantity":10}]}'
```

This is an integration example, not an installed plugin. Three rules hold on any platform:

- **Keep the key on the server**, never in a theme, a storefront script or a mobile app.
- **Take the customs fields from your catalog**, never from the shopper. A product description cannot
  establish an HTS code, and a retail price is not a customs value.
- **Show `null` as unknown.** Only show a final duty when `duty` is not null, and keep
  `publication_id` with the order: it names the tariff data of the estimate.

## Where the customs fields live

| Platform | HTS code and origin | Customs value |
| --- | --- | --- |
| Shopify | `harmonizedSystemCode` and `countryCodeOfOrigin` of the `InventoryItem`, in the Admin API | The declared value of the goods: a metafield of yours, or `unitCost` when it is what you declare |
| WooCommerce | Custom product meta of yours, read with `$product->get_meta()` | The same, in another meta |
| Medusa, Spree, Saleor, BigCommerce, Adobe Commerce | Variant or product metadata, or custom attributes | The same |

## Calling it from WooCommerce

A sketch for your theme or plugin: `tarifftrust_duties_url` is where you run this server.

```php
add_action('woocommerce_cart_calculate_fees', function ($cart) {
    $lines = [];
    foreach ($cart->get_cart() as $item) {
        $lines[] = ['sku' => $item['data']->get_sku(), 'quantity' => $item['quantity']];
    }
    $response = wp_remote_post(tarifftrust_duties_url(), [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => wp_json_encode(['lines' => $lines]),
        'timeout' => 20,
    ]);
    $body = json_decode(wp_remote_retrieve_body($response), true);
    // Unknown is never zero: without a duty, say so rather than charging nothing.
    if (is_array($body) && isset($body['duty'])) {
        $cart->add_fee('Estimated US duty', (float) $body['duty']);
    }
});
```
