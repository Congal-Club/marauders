/* ***** TEST EN MERCADO LIBRE ***** */
import { expect, test } from '@playwright/test';

// Intentar agregar producto al carrito sin seleccionar variantes
test('Test add products without select variants', async ({ page }) => {
  await page.goto('https://articulo.mercadolibre.com.mx/MLM-2138323925-playera-camiseta-oversize-acid-wash-hombre-mujer-gym-casual-_JM');

  const productTitle = page.locator('h1[class="ui-pdp-title"]');
  await expect(productTitle).toContainText('Playera Camiseta Oversize Acid Wash Hombre Mujer Gym Casual');

  const addToCartButton = page.locator('button[class="andes-button andes-spinner__icon-base ui-pdp-action--secondary ui-pdp-action-secondary--disabled andes-button--quiet"]');
  await page.pause();

  await addToCartButton.click();
  await page.pause();

  const firstVariant = page.locator('p[class="ui-pdp-variations__label ui-pdp-color--BLACK ui-pdp-color--RED"]').nth(0);
  await expect(firstVariant).toContainText('Diseño De La Tela:');
  const secondVariant = page.locator('p[class="ui-pdp-variations__label ui-pdp-color--BLACK ui-pdp-color--RED"]').nth(1);
  await expect(secondVariant).toContainText('Diseño Impreso:');
  const thirdVariant = page.locator('p[class="ui-pdp-variations__label ui-pdp-color--BLACK ui-pdp-color--RED"]').nth(2);
  await expect(thirdVariant).toContainText('Talla:');

  await page.pause();
});

// Selección de variantes antes de agregar al carrito
test('Select variants before add to cart', async ({ page }) => {
  await page.goto('https://articulo.mercadolibre.com.mx/MLM-2138323925-playera-camiseta-oversize-acid-wash-hombre-mujer-gym-casual-_JM');

  const firstVariantToSelect = page.locator('a[aria-label="Lisa, Boton 2 de 2"]');
  await firstVariantToSelect.click();
  await page.pause();

  const secondVariantToSelect = page.locator('a[aria-label="Sin Estampado, Boton 2 de 2"]');
  await secondVariantToSelect.click();
  await page.pause();

  const thirdVariantToSelect = page.locator('a[aria-label="XL, XG, Boton 4 de 4"]');
  await thirdVariantToSelect.click();
  await page.pause();

  const addToCartButton = page.locator('button[class="andes-button andes-spinner__icon-base ui-pdp-action--secondary andes-button--quiet"]');
  await page.pause();

  await addToCartButton.click();
  await page.pause();

  const needAccountTitle = page.locator('h1[class="center-card__title"]');
  await expect(needAccountTitle).toContainText('¡Hola! Para agregar al carrito, ingresa a tu cuenta');

  await page.pause();
});

// Selección de variantes antes de intentar comprar
test('Select variants before buy', async ({ page }) => {
  await page.goto('https://articulo.mercadolibre.com.mx/MLM-2138323925-playera-camiseta-oversize-acid-wash-hombre-mujer-gym-casual-_JM');

  const firstVariantToSelect = page.locator('a[aria-label="Lisa, Boton 2 de 2"]');
  await firstVariantToSelect.click();
  await page.pause();

  const secondVariantToSelect = page.locator('a[aria-label="Sin Estampado, Boton 2 de 2"]');
  await secondVariantToSelect.click();
  await page.pause();

  const thirdVariantToSelect = page.locator('a[aria-label="XL, XG, Boton 4 de 4"]');
  await thirdVariantToSelect.click();
  await page.pause();

  const buyButton = page.locator('button[class="andes-button andes-spinner__icon-base ui-pdp-action--primary andes-button--loud"]');
  await page.pause();

  await buyButton.click();
  await page.pause();

  const needAccountTitle = page.locator('h1[class="center-card__title"]');
  await expect(needAccountTitle).toContainText('¡Hola! Para comprar, ingresa a tu cuenta');

  await page.pause();
});
