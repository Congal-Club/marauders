/* ***** TEST EN MERCADO LIBRE ***** */
import { expect, test } from '@playwright/test';

// El usuario inicia sesión
test('User Login', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');

  const registerButton = page.locator('a[data-link-id="login"]');
  await expect(registerButton).toBeVisible();
  await registerButton.click();

  await page.pause();

  await expect(page.locator('h1[class="andes-typography grid-view__title andes-typography--type-title andes-typography--size-xl andes-typography--color-primary andes-typography--weight-regular"]')).toContainText('Ingresa tu e-mail o teléfono para iniciar sesión');

  const emailInput = page.locator('input[name="user_id"]');
  await expect(emailInput).toBeVisible();
  await emailInput.fill('cesarvillalobosolmos.01@gmail.com');

  const continueButton = page.locator('button[class="andes-button login-form__submit login-form__submit--social andes-button--large andes-button--loud"]');
  await expect(continueButton).toBeVisible();
  await continueButton.click();

  await page.pause();
});

// El usuario inicia sesión con una cuenta que no existe
test('User Login with Nonexistent Account', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');

  const registerButton = page.locator('a[data-link-id="login"]');
  await expect(registerButton).toBeVisible();
  await registerButton.click();

  await page.pause();

  await expect(page.locator('h1[class="andes-typography grid-view__title andes-typography--type-title andes-typography--size-xl andes-typography--color-primary andes-typography--weight-regular"]')).toContainText('Ingresa tu e-mail o teléfono para iniciar sesión');

  const emailInput = page.locator('input[name="user_id"]');
  await expect(emailInput).toBeVisible();
  await emailInput.fill('no-existe@gmail.com');

  const continueButton = page.locator('button[class="andes-button login-form__submit login-form__submit--social andes-button--large andes-button--loud"]');
  await expect(continueButton).toBeVisible();
  await continueButton.click();

  await page.pause();

  const captcha = page.locator('div[class="recaptcha__container"]');
  await expect(captcha).toBeVisible();
  await captcha.click();

  await page.pause();
});
