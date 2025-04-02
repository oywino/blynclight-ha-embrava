# Changelog

All notable changes to the Blynclight Embrava integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-04-02

### Fixed
- Corrected version number inconsistency between manifest.json and GitHub release tag
- Fixed SelectEntity setup and device linking
- Improved error handling for network connectivity issues

### Added
- Added detailed documentation in README.md
- Implemented proper HACS compatibility
- Enhanced installation instructions

### Changed
- Updated README.md with clearer setup instructions
- Improved error messages for better troubleshooting

## [0.0.1] - 2025-03-04

### Added
- Initial release with select entity for Blynclight control
- Integration with Embrava Connect's global hotkeys
- Simple dropdown control in Lovelace (`select.blynclight`)
- Local communication via PowerShell HTTP server
- Basic configuration flow UI

[0.1.1]: https://github.com/oywino/blynclight-ha-embrava/compare/v0.0.1...v0.1.1
[0.0.1]: https://github.com/oywino/blynclight-ha-embrava/releases/tag/v0.0.1
