/* ***** TEST EN MERCADO LIBRE ***** */
import { expect, test } from '@playwright/test';

// El usuario encuentra la sección de ofertas en la página principal
test('Find Offers Section', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');
  await expect(page).toHaveTitle(/Mercado Libre México/);

  const offersSection = page.locator('a.nav-menu-item-link:has-text("Ofertas")');
  await expect(offersSection).toBeVisible();

  await offersSection.click();
  await expect(page).toHaveURL(/ofertas/);

  const offersTitle = page.locator('h1[class="header_title"]');
  await expect(offersTitle).toContainText('Ofertas');

  await page.pause();
});

// El usuario ingresa una categoría en especifico y explora las ofertas/descuentos
test('Explore Offers by Category', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');
  
  const offersSection = page.locator('a.nav-menu-item-link:has-text("Ofertas")');
  await expect(offersSection).toBeVisible();

  await offersSection.click();

  const category = page.locator('div.andes-carousel-snapped__slide:has(p:has-text("Videojuegos"))');
  await expect(category).toBeVisible();

  await page.pause();

  await category.click();
  await expect(page.locator('h1[class="title"]')).toContainText('Consolas y Videojuegos');

  const firstOffer = page.locator('div[class="andes-card poly-card poly-card--grid-card andes-card--flat andes-card--padding-0 andes-card--animated"]').first();
  await expect(firstOffer).toBeVisible();

  const haveDiscount = firstOffer.locator('s[class="andes-money-amount andes-money-amount--previous andes-money-amount--cents-dot"]');
  await expect(haveDiscount).toBeVisible();

  await page.pause();
});

// El usuario ingresa a las ofertas del día y filtra por una categoría en especifico
test('Filter Daily Offers by Category', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');
  
  const offersSection = page.locator('a.nav-menu-item-link:has-text("Ofertas")');
  await expect(offersSection).toBeVisible();

  await offersSection.click();

  const category = page.locator('div.andes-carousel-snapped__slide:has(p:has-text("Ofertas relámpago"))');
  await expect(category).toBeVisible();

  await page.pause();

  await category.click();
  const asideFilters = page.locator('aside[class="qcat-filters"]');
  await expect(asideFilters).toBeVisible();

  const categoryFilter = asideFilters.locator('div[class="list-filter"]').first();
  await expect(categoryFilter).toBeVisible();

  const firstCategory = categoryFilter.locator('a[class="list-filter__list-element"]').first();
  await expect(firstCategory).toBeVisible();
  
  await page.pause();
  
  await firstCategory.click();
  await expect(page.locator('h1[class="title"]')).toContainText('Accesorios para Vehículos');

  await page.pause();
});

// El usuario encuentra un producto de su interés en la sección de ofertas del día
test('Find Product in Daily Offers', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');
  
  const offersSection = page.locator('a.nav-menu-item-link:has-text("Ofertas")');
  await expect(offersSection).toBeVisible();

  await offersSection.click();

  const category = page.locator('div.andes-carousel-snapped__slide:has(p:has-text("Notebooks"))');
  await expect(category).toBeVisible();

  await page.pause();

  await category.click();
  const firstOffer = page.locator('div[class="andes-card poly-card poly-card--grid-card andes-card--flat andes-card--padding-0 andes-card--animated"]').first();
  await expect(firstOffer).toBeVisible();

  await page.pause();

  await firstOffer.click();
  await expect(page.locator('h1[class="ui-pdp-title"]')).toBeVisible();

  await page.pause();
});
