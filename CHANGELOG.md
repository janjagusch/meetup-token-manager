# Changelog

## 0.2.0

- Removed Redis dependency. Users can now define their own token cache by inherting from `TokenCache`.
- Provided three token caches: `TokenCacheFile`, `TokenCacheGCS` and `TokenCacheRedis`.
- Changed the `Token` class.
- Introduced `TokenManager` class.
- Renamed project to `meetup-token-manager`.
- Added `utils.request_token` function to easily authenticate and get first token.
- Removed tests.

## 0.1.0

- Initial implementation.
