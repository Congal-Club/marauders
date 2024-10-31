import { expect, test } from '@playwright/test';

test('Search click', async ({ page }) => {
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
});
