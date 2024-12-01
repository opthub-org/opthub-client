# Changelog

## [0.7.0](https://github.com/opthub-org/opthub-client/compare/v0.6.3...v0.7.0) (2024-12-01)


### Features

* improve design of trials history ([09d1508](https://github.com/opthub-org/opthub-client/commit/09d150832fbfcc5198ad5899cdc6df72d77cc0b7))

## [0.6.3](https://github.com/opthub-org/opthub-client/compare/v0.6.2...v0.6.3) (2024-12-01)


### Bug Fixes

* show error messages if use opt show trails -d. ([#158](https://github.com/opthub-org/opthub-client/issues/158)) ([6502d19](https://github.com/opthub-org/opthub-client/commit/6502d199b9ba68a1d61f2c4b1c27693624c932b4))

## [0.6.2](https://github.com/opthub-org/opthub-client/compare/v0.6.1...v0.6.2) (2024-11-16)


### Bug Fixes

* Remove Self to support Python 3.10 ([9eb04e4](https://github.com/opthub-org/opthub-client/commit/9eb04e470066ecaede8f997de991343edf00725c))

## [0.6.1](https://github.com/opthub-org/opthub-client/compare/v0.6.0...v0.6.1) (2024-11-16)


### Bug Fixes

* Add TypeVar to support versions earlier than Python 3.12 ([079a42d](https://github.com/opthub-org/opthub-client/commit/079a42d671e7b8cdac032c7ef0b1fe4142dbeffb))

## [0.6.0](https://github.com/opthub-org/opthub-client/compare/v0.5.2...v0.6.0) (2024-11-12)


### Features

* Exponential-backoff policy for evaluation and score polling. ([1194301](https://github.com/opthub-org/opthub-client/commit/1194301074ae5802bd35369b049944d2d2fc9fd5))

## [0.5.2](https://github.com/opthub-org/opthub-client/compare/v0.5.1...v0.5.2) (2024-11-12)


### Bug Fixes

* error when the competition does not exist. ([7bee324](https://github.com/opthub-org/opthub-client/commit/7bee3249dc1237438cbad733b27b41853f3ef791))

## [0.5.1](https://github.com/opthub-org/opthub-client/compare/v0.5.0...v0.5.1) (2024-09-26)


### Bug Fixes

* JWT decode error ([eaae41d](https://github.com/opthub-org/opthub-client/commit/eaae41d7d8fad60291223915a61fde52d7ddfbd5))
* remote messages error ([56fd494](https://github.com/opthub-org/opthub-client/commit/56fd494fcf10c4a1701a27c5273486f1c564b440))

## [0.5.0](https://github.com/opthub-org/opthub-client/compare/v0.4.0...v0.5.0) (2024-09-06)


### Features

* Add a client library for the OptHub public REST API. ([#141](https://github.com/opthub-org/opthub-client/issues/141)) ([c21e61e](https://github.com/opthub-org/opthub-client/commit/c21e61e34f07a0deb0148fa9899eab37c24c88aa))

## [0.4.0](https://github.com/opthub-org/opthub-client/compare/v0.3.0...v0.4.0) (2024-09-04)


### Features

* Require the -e option for the download command ([#135](https://github.com/opthub-org/opthub-client/issues/135)) ([6d17b0b](https://github.com/opthub-org/opthub-client/commit/6d17b0bc949eda57e8f5d4a2fba36861d0a31e34))


### Bug Fixes

* change query to mutation in create_api_key ([c6f4cb5](https://github.com/opthub-org/opthub-client/commit/c6f4cb529cc2f56048ca6d0eb95c5c48721930f2))

## [0.3.0](https://github.com/opthub-org/opthub-client/compare/v0.2.0...v0.3.0) (2024-08-17)


### Features

* Modify url, jwks url, and client id ([9847b82](https://github.com/opthub-org/opthub-client/commit/9847b82f2b5195b33d84a7794625e5be509a4975))

## [0.2.0](https://github.com/opthub-org/opthub-client/compare/v0.1.3...v0.2.0) (2024-08-16)


### Features

* create api_key command ([#121](https://github.com/opthub-org/opthub-client/issues/121)) ([6c58311](https://github.com/opthub-org/opthub-client/commit/6c58311f2c516a81a1cc3a3faca96e6c60376e1b))


### Bug Fixes

* read version from init.py instead of toml.file  ([#122](https://github.com/opthub-org/opthub-client/issues/122)) ([55db1d7](https://github.com/opthub-org/opthub-client/commit/55db1d773aaf574a78146a34531fbc535274da00))

## [0.1.3](https://github.com/opthub-org/opthub-client/compare/v0.1.2...v0.1.3) (2024-07-20)


### Bug Fixes

* fix depencies ([332a1ed](https://github.com/opthub-org/opthub-client/commit/332a1ed16db8915e2d9a16d74aba9b50145e6337))

## [0.1.2](https://github.com/opthub-org/opthub-client/compare/v0.1.1...v0.1.2) (2024-07-20)


### Bug Fixes

* fix dependencies ([2a1b41a](https://github.com/opthub-org/opthub-client/commit/2a1b41ac56e11e5a34016c3f5c45d7ad19803db0))

## [0.1.1](https://github.com/opthub-org/opthub-client/compare/v0.1.0...v0.1.1) (2024-07-20)


### Bug Fixes

* fix dependencies ([ae20c01](https://github.com/opthub-org/opthub-client/commit/ae20c01412512d3accc3a837100086c446747e30))
* fix dependencies ([2630cf2](https://github.com/opthub-org/opthub-client/commit/2630cf22362158f68ca7aeb110f0479fb082332c))

## 0.1.0 (2024-07-20)


### Features

* Submitting solutions to OptHub competitions
* Checking the history and status of solutions submitted to OptHub competitions
