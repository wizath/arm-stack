# Changelog

All notable changes to the ARM Stack Usage Analyzer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2024-12-19

### Added
- JSON export functionality with `--export-json` option
- Comparison mode for analyzing changes between builds with `--compare` option
- Git-diff style output for stack usage comparisons
- Comprehensive metadata tracking in exported JSON data
- Support for detecting function additions, removals, and modifications
- Enhanced command-line interface with new export and comparison options

### Changed
- Analysis workflow now returns structured data for JSON export
- Command-line argument parsing updated to support new modes
- Help text updated with new usage examples

### Features
- **JSON Export:**
  - Complete analysis data export including metadata, summary, functions, and file statistics
  - Timestamped exports for tracking analysis history
  - Structured data format suitable for automation and CI/CD integration

- **Comparison Analysis:**
  - Side-by-side comparison of two JSON analysis files
  - Git-diff style output with color-coded changes
  - Function-level change detection (added/removed/modified)
  - Summary statistics comparison
  - File-level aggregated change reporting

## [1.1.0] - 2024-12-19

### Added
- Support for Zephyr/CMake `.c.obj` object files in addition to standard `.o` files
- Enhanced object file discovery with dual extension support (`**/*.o`, `**/*.c.obj`)
- Proper stack usage file mapping for `.c.obj` -> `.c.su` files

### Fixed
- Stack usage file detection now correctly handles both `.o` and `.c.obj` extensions
- Object file prerequisite checking updated to support Zephyr build systems
- Error messages now reflect support for both file types

### Changed
- Updated file search patterns to include both `.o` and `.c.obj` extensions
- Enhanced `find_object_files()` method to handle CMake-generated object files
- Improved `_parse_su_file()` method with proper extension handling
- Updated `check_prerequisites()` to validate both object file types

## [1.0.0] - 2024-12-19

### Added
- Initial release of ARM Stack Usage Analyzer
- Comprehensive stack usage analysis for ARM embedded projects
- Call graph traversal and stack cost calculation
- Function-level stack usage reporting with frame sizes and call depths
- File-based stack usage organization and summary
- Symbol resolution across multiple object files
- Recursion detection and marking
- Interrupt handler analysis with virtual interrupt node
- Configurable reporting threshold
- Color-coded terminal output
- Ambiguous symbol resolution warnings
- Peak stack usage estimation
- Support for ARM GCC toolchain (`arm-none-eabi-objdump`)
- Command-line interface with multiple options
- Comprehensive error handling and prerequisite checking

### Features
- **Analysis Capabilities:**
  - Parse object file disassembly to build call graphs
  - Read stack usage information from `.su` files
  - Calculate total stack costs through call graph traversal
  - Detect recursive functions and call cycles
  - Identify root functions (entry points)

- **Reporting:**
  - File-based stack usage hierarchy
  - Detailed function table with costs, frame sizes, and call depths
  - Peak stack usage estimates for main and interrupt contexts
  - Statistics summary with function counts and averages
  - Unresolved function warnings

- **Configuration:**
  - Adjustable stack usage threshold for filtering
  - Optional warning suppression
  - Color output control
  - Flexible build directory specification

### Technical Details
- Written in Python 3 with comprehensive type hints
- Uses ARM GCC objdump for disassembly parsing
- Implements depth-first traversal with memoization
- Handles ARM function call overhead (4 bytes)
- Filters out CMake compiler identification files
- Supports glob patterns for recursive file discovery

[1.2.0]: https://github.com/wizath/arm-stack/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/wizath/arm-stack/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/wizath/arm-stack/releases/tag/v1.0.0 
