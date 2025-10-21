# Changelog

All notable changes to Yourdio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2024-10-22

### Added
- Dark Sun: Wasteland theme for post-apocalyptic desert fantasy
- New theme featuring E Phrygian mode with dissonant clusters
- Descending structural arc (world fading/dying)
- Very sparse, low-intensity atmosphere (perfect for Dark Sun RPG)

### Fixed
- All flake8 linting errors (17 issues) across codebase
- All mypy type checking errors (7 issues)
- Critical bug: undefined 'audio_path' in analyze_reference.py
- Removed 8 unused imports across multiple files
- Fixed 7 f-strings without placeholders
- Fixed bare except clause in yourdio_gui.py
- Added proper type annotations throughout

### Changed
- Applied Black code formatting to entire codebase
- Improved type safety with explicit Optional types
- Enhanced code quality to pass all static analysis checks

## [1.0.1] - 2024-10-22

### Added
- GitHub Actions workflow for automated Windows releases
- Automated build pipeline triggered by version tags
- LICENSE file (MIT License)
- pyproject.toml for proper Python package installation
- CHANGELOG.md for version tracking
- Code quality configuration (Black, Flake8, mypy)
- CONTRIBUTING.md with development guidelines
- Test infrastructure setup

### Changed
- Improved tab text visibility in GUI with bold dark green styling
- Enhanced tab appearance with 3D relief effects
- Tab text now uses #006400 dark green color with raised borders

### Fixed
- Tab text readability against dark background

## [1.0.0] - 2024-10-22

### Added
- Initial release of Yourdio
- Retro Lo-Fi algorithmic MIDI music generator
- 6-hour composition generation system
- Event soundscape generator for short loops
- Windows GUI application with Winamp-inspired interface
- Theme-based configuration system (8 pre-built themes)
- Chaos theory integration (Lorenz attractor, logistic map)
- Prime number sequence rhythms
- Fibonacci timing patterns
- YAML theme configuration
- Comprehensive documentation suite
- Windows executable build system
- Audio playback support
- Theme analysis from existing audio (optional)

### Features
- 12 chapter generation (30 minutes each = 6 hours total)
- 8 event types (combat, stealth, tavern, exploration, etc.)
- Modal music theory foundation (Dorian, Aeolian, Phrygian)
- Quartal/Quintal harmony support
- Generative MIDI with 4 parallel tracks per chapter
- General MIDI instrument support
- Structural arc system (parabolic, slow burn, descending, flat)
- Dynamic intensity scaling
- Drone and ambient texture layers
- Cross-platform Python codebase

[1.0.1]: https://github.com/kostchei/Yourdio/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/kostchei/Yourdio/releases/tag/v1.0.0
