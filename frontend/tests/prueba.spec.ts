// import { expect, test } from '@playwright/test';

/* test('Search click', async ({ page }) => {
  await page.goto('https://aguascalientes.tecnm.mx/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/TecNM campus Aguascalientes/);

  // Wait for the page to load completely
  await page.waitForLoadState('networkidle');
  const emailLink = page.locator('a[href*="login.mricosoftonline.com"][title]="Correo Institucional"');

  // Verify the link exists and is visible
  await expect(emailLink).toBeVisible();

  // Since the link opens in a new tab, we need to handle that
  const [newPage] = await Promise.all([
    page.waitForEvent('popup'),
    emailLink.click(),
  ]);

  // Verify the new page url
  expect(newPage.url()).toContain(/.*login\.microsoftonline\.com/);
  await newPage.pause();
}); */

/* test('search click', async ({ page }) => {
  await page.goto('https://amazon.com.mx/');
  await expect(page).toHaveTitle(/Amazon.com.mx: Precios bajos - Envío rápido - Millones de productos/);
  // await page.waitForLoadState('networkidle');
  const searchInput = page.locator("input[id='twotabsearchtextbox']")
  await expect(searchInput).toBeVisible();

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/TecNM campus Aguascalientes/);

  await page.waitForLoadState('networkidle');
  const emailLink = page.locator('a[href*="login.microsoftonline.com"][title="Correo]')

  await expect(emailLink).toBeVisible();
  //Sice the link opens in a new tab, we need to handle that
  const [newPage] = await Promise.all([
    page.waitForEvent('popup'),
    emailLink.click()
  ])

  await expect(newPage).toHaveURL(/.*login\.microsoftonline\.com/);
  await page.pause()
}); */

/* test('search', async ({ page }) => {
  await page.goto('https://amazon.com.mx/');
  await expect(page).toHaveTitle(/Amazon.com.mx: Precios bajos - Envío rápido - Millones de productos/);
  
  const searchInput = page.locator("input[id='twotabsearchtextbox']");
  await expect(searchInput).toBeVisible();
  
  await searchInput.fill('xbox');
  await page.keyboard.press('Enter');

  await expect(page.locator("span[class='a-color-state a-text-bold']")).toContainText('xbox');
  await expect(page.locator("h2[class='a-size-medium-plus a-spacing-none a-color-base a-text-bold']")).toContainText('Resultados');
  await expect(page.locator("div[class='s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_1']")).toBeVisible();
  
  const first = page.locator("div[class='s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_1']")
  await expect(first).toBeVisible();

  await page.pause();
}); */

/* test('search click 2', async ({ page }) => {
  await page.goto('https://www.amazon.com.mx/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Amazon.com.mx: Precios bajos - Envío rápido - Millones de productos/);
  const searchInput = page.locator("input[id='twotabsearchtextbox']");
  await expect(searchInput).toBeVisible();
  await searchInput.fill("xbox")
  await page.keyboard.press('Enter');

  await expect(page.locator("span[class='a-color-state a-text-bold']")).toContainText("xbox")
  await expect(page.locator("h2[class='a-size-medium-plus a-spacing-none a-color-base a-text-bold']")).toContainText("Resultados")
  await expect(page.locator("div[class='s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_1']")).toBeVisible();
  const first = page.locator("div[class='s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_1']").first();
  await expect(first).toBeVisible();
  await first.waitFor({state: 'visible'});
  await expect(first.locator("span[class='a-size-base-plus a-color-base a-text-normal']")).toHaveText("Xbox Consola Series S digital de 512 GB - Robot White - Nacional Edition");
  await first.locator("span[class='a-size-base-plus a-color-base a-text-normal']").click();

  await page.pause()
}); */
