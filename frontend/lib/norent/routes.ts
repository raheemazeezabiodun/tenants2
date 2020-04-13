import { createRoutesForSite } from "../util/route-util";
import { createDevRouteInfo } from "../dev/routes";

function createLocalizedRouteInfo(prefix: string) {
  return {
    /** The home page. */
    home: `${prefix}/`,
  };
}

export const NorentRoutes = createRoutesForSite(createLocalizedRouteInfo, {
  /**
   * Example pages used in integration tests, and other
   * development-related pages.
   */
  dev: createDevRouteInfo("/dev"),
});
