/* ***** TEST EN MERCADO LIBRE ***** */
import { expect, test } from '@playwright/test';

// El usuario crea una cuenta nueva
/* test('Create New Account', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');
  
  const registerButton = page.locator('a:has-text("Crea tu cuenta")');
  await expect(registerButton).toBeVisible();
  await registerButton.click();

  await page.pause();

  await expect(page.locator('h1[class="hub-card__title"]')).toContainText('Completa los datos para crear tu cuenta');

  const addEmailButton = page.locator('button[class="andes-button hub-item__button andes-button--medium andes-button--loud"]');
  await expect(addEmailButton).toBeVisible();
  await addEmailButton.click();

  await page.pause();

  await expect(page.locator('h1[class="enter-email-card__title"]')).toContainText('Ingresa tu e-mail');

  const emailInput = page.locator('input[class="andes-form-control__field"]');
  await expect(emailInput).toBeVisible();
  await emailInput.fill('congcod256@gmail.com');

  const termsCheckbox = page.locator('input[class="andes-checkbox__input"]');
  await expect(termsCheckbox).toBeVisible();
  await termsCheckbox.check();

  const continueButton = page.locator('button[class="andes-button enter-email-card__submit andes-button--large andes-button--loud andes-button--full-width"]');
  await expect(continueButton).toBeVisible();
  await continueButton.click();

  await page.pause();

  const addNameButton = page.locator('button[class="andes-button hub-item__button andes-button--medium andes-button--loud"]');
  await expect(addNameButton).toBeVisible();
  await addNameButton.click();

  await page.pause();

  await expect(page.locator('h2[class="andes-typography kyc-light-card__title andes-typography--type-title andes-typography--size-m andes-typography--color-primary andes-typography--weight-regular"]')).toContainText('Elige un nombre para ti o para tu negocio');

  const nameInput = page.locator('input[id="firstName"]');
  await expect(nameInput).toBeVisible();
  await nameInput.fill('Aranzazu Jimena');

  const lastNameInput = page.locator('input[id="lastName"]');
  await expect(lastNameInput).toBeVisible();
  await lastNameInput.fill('Messa Sanchez');

  const continueButton2 = page.locator('button[class="andes-button kyc-light-card__action andes-button--large andes-button--loud"]');
  await expect(continueButton2).toBeVisible();
  await continueButton2.click();

  await page.pause();

  const validatePhoneButton = page.locator('button[class="andes-button hub-item__button andes-button--medium andes-button--loud"]');
  await expect(validatePhoneButton).toBeVisible();
  await validatePhoneButton.click();

  await page.pause();

  await expect(page.locator('h1[class="registration-input-phone__title"]')).toContainText('Ingresa tu teléfono');
  
  const phoneInput = page.locator('input[class="andes-form-control__field"]');
  await expect(phoneInput).toBeVisible();
  await phoneInput.fill('3461099207');

  const continueButton3 = page.locator('button[class="andes-button registration-input-phone__continue andes-button--large andes-button--loud"]');
  await expect(continueButton3).toBeVisible();
  // await continueButton3.click();

  await page.pause();
}); */

// El usuario registra un correo no valido
/* test('Register Invalid Email', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');

  const registerButton = page.locator('a:has-text("Crea tu cuenta")');
  await expect(registerButton).toBeVisible();
  await registerButton.click();

  await page.pause();

  const addEmailButton = page.locator('button[class="andes-button hub-item__button andes-button--medium andes-button--loud"]');
  await expect(addEmailButton).toBeVisible();
  await addEmailButton.click();

  await page.pause();

  const emailInput = page.locator('input[class="andes-form-control__field"]');
  await expect(emailInput).toBeVisible();
  await emailInput.fill('email-invalido');

  const termsCheckbox = page.locator('input[class="andes-checkbox__input"]');
  await expect(termsCheckbox).toBeVisible();
  await termsCheckbox.check();

  const continueButton = page.locator('button[class="andes-button enter-email-card__submit andes-button--large andes-button--loud andes-button--full-width"]');
  await expect(continueButton).toBeVisible();
  await continueButton.click();

  await page.pause();

  const adviceMessage = page.locator('span[id="enter-email-input-message"]');
  await expect(adviceMessage).toContainText('Usa el formato nombre@ejemplo.com.');

  await page.pause();
}); */

// El usuario se registra y ya tenía una cuenta registrada
test('Register with Existing Account', async ({ page }) => {
  await page.goto('https://www.mercadolibre.com.mx/');

  const registerButton = page.locator('a:has-text("Crea tu cuenta")');
  await expect(registerButton).toBeVisible();
  await registerButton.click();

  await page.pause();

  const addEmailButton = page.locator('button[class="andes-button hub-item__button andes-button--medium andes-button--loud"]');
  await expect(addEmailButton).toBeVisible();
  await addEmailButton.click();

  await page.pause();

  const emailInput = page.locator('input[class="andes-form-control__field"]');
  await expect(emailInput).toBeVisible();
  await emailInput.fill('cesarvillalobosolmos.01@gmail.com');

  const termsCheckbox = page.locator('input[class="andes-checkbox__input"]');
  await expect(termsCheckbox).toBeVisible();
  await termsCheckbox.check();

  const continueButton = page.locator('button[class="andes-button enter-email-card__submit andes-button--large andes-button--loud andes-button--full-width"]');
  await expect(continueButton).toBeVisible();
  await continueButton.click();

  await page.pause();

  // await page.pause();
});
