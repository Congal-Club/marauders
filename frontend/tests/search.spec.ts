// /* ***** TEST EN MERCADO LIBRE ***** */
// import { expect, test } from '@playwright/test';

// // Búsqueda general
// test('General Search', async ({ page }) => {
//   await page.goto('https://www.mercadolibre.com.mx/');
//   await expect(page).toHaveTitle(/Mercado Libre México/);

//   const searchInput = page.locator("input[name='as_word']");
//   await expect(searchInput).toBeVisible();

//   await searchInput.fill('xbox');
//   await page.keyboard.press('Enter');

//   await expect(page.locator('h1[class="ui-search-breadcrumb__title"]')).toContainText('Xbox');
//   await expect(page.locator('ol[class="ui-search-layout ui-search-layout--stack shops__layout"]')).toBeVisible();

//   await page.pause();
// });

// // Búsqueda de un producto en especifico
// test('Specific Product Search', async ({ page }) => {
//   await page.goto('https://www.mercadolibre.com.mx/');
//   await expect(page).toHaveTitle(/Mercado Libre México/);

//   const searchInput = page.locator("input[name='as_word']");
//   await expect(searchInput).toBeVisible();

//   await searchInput.fill('xbox one');
//   await page.keyboard.press('Enter');

//   await expect(page.locator('h1[class="ui-search-breadcrumb__title"]')).toContainText('Xbox one');

//   const firstProduct = page.locator('h2[class="poly-box poly-component__title"]').first();
//   await expect(firstProduct).toBeVisible();

//   const productLink = firstProduct.locator('a');
//   await expect(productLink).toBeVisible();

//   await productLink.click();
//   await expect(page.locator('h1[class="ui-pdp-title"]')).toContainText('Consola Xbox Series S All Digital 512gb Color Blanco');

//   await page.pause();
// });

// // Búsqueda con filtros avanzados
// test('Advanced Search', async ({ page }) => {
//   await page.goto('https://www.mercadolibre.com.mx/');
//   await expect(page).toHaveTitle(/Mercado Libre México/);

//   const searchInput = page.locator("input[name='as_word']");
//   await expect(searchInput).toBeVisible();

//   await searchInput.fill('play station');
//   await page.keyboard.press('Enter');

//   await expect(page.locator('h1[class="ui-search-breadcrumb__title"]')).toContainText('Play station');

//   const filtersContainer = page.locator('section[class="ui-search-filter-groups"]');
//   await expect(filtersContainer).toBeVisible();

//   const filterByFreeSend = filtersContainer.locator('div[class="ui-search-filter-dl"]').nth(1);
//   await expect(filterByFreeSend).toBeVisible();

//   const freeSendButton = filterByFreeSend.locator('button');
//   await freeSendButton.click();

//   await page.pause();

//   const filterByCondition = filtersContainer.locator('div[class="ui-search-filter-dl"]').nth(5);
//   const linkForNewProducts = filterByCondition.locator('a').nth(0);
//   await linkForNewProducts.click();

//   await page.pause();

//   const filterByDiscount = filtersContainer.locator('div[class="ui-search-filter-dl"]').nth(8);
//   const mostDiscountLink = filterByDiscount.locator('a').last();
//   await mostDiscountLink.click();

//   await page.pause();

//   const filtersApplied = page.locator('section[class="ui-search-applied-filters"]');
//   await expect(filtersApplied).toBeVisible();
//   await expect(filtersApplied.locator('a')).toHaveCount(2);

//   await page.pause();
// });

// // Búsqueda de productos relacionados
// test('Related Products Search', async ({ page }) => {
//   await page.goto('https://www.mercadolibre.com.mx/');
//   await expect(page).toHaveTitle(/Mercado Libre México/);

//   const searchInput = page.locator("input[name='as_word']");
//   await expect(searchInput).toBeVisible();

//   await searchInput.fill('laptop gamer');
//   await page.keyboard.press('Enter');

//   await expect(page.locator('h1[class="ui-search-breadcrumb__title"]')).toContainText('Laptop gamer');

//   const firstProduct = page.locator('li[class="ui-search-layout__item shops__layout-item"]').first();
//   await firstProduct.click();

//   await expect(page.locator('h2[class="ui-recommendations-title-link"]')).toBeVisible();
//   await expect(page.locator('h2[class="ui-recommendations-title-link"]')).toContainText('Productos relacionados');

//   const relatedProductsContainer = page.locator('div[class="andes-carousel-snapped andes-carousel-snapped--scroll-hidden"]');
//   const firstRelatedProduct = relatedProductsContainer.locator('div[class="andes-carousel-snapped__slide andes-carousel-snapped__slide--spacing-12"]').first();
//   await firstRelatedProduct.click();

//   await page.pause();
// });
