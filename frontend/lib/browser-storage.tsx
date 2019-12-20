import { BaseBrowserStorageSchema, BrowserStorage, createUpdateBrowserStorage } from "./browser-storage-base";

const SCHEMA_VERSION = 1;

const SESSION_STORAGE_KEY = `tenants2_v${SCHEMA_VERSION}`;

export type BrowserStorageSchema = BaseBrowserStorageSchema & {
  /** The latest street address a user entered in the app.*/
  latestAddress?: string,

  /** The latest borough a user entered in the app. */
  latestBorough?: string,
};

const DEFAULT_BROWSER_STORAGE: BrowserStorageSchema = {
  _version: SCHEMA_VERSION,
};

/**
 * Stores data browser-side using `window.sessionStorage`.
 * The data won't be available server-side and this functionality shouldn't
 * be relied upon for mission-critical tasks, since the user may be in
 * compatibility mode or not have JS enabled in their browser.
 * 
 * That said, it can be used for progressively enhancing a site to make
 * it a bit easier to use. It's also more privacy-preserving than using
 * a session cookie, as even the most transient session cookies expire on
 * browser close, while `window.sessionStorage` expires on the closing of
 * a browser *tab*, reducing the likelihood that someone on a public/shared
 * computer accidentally leaks personal data.
 */
export const browserStorage = new BrowserStorage(DEFAULT_BROWSER_STORAGE, SESSION_STORAGE_KEY);

export const UpdateBrowserStorage = createUpdateBrowserStorage(browserStorage);

export function updateAddressFromBrowserStorage<T extends {address: string, borough: string}>(value: T): T {
  let address = browserStorage.get('latestAddress') || '';
  let borough = browserStorage.get('latestBorough') || '';
  if (!value.address && address && !value.borough && borough) {
    value = {...value, address, borough};
  }
  return value;
}
