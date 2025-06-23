# ARM Stack Usage Analyzer

A comprehensive tool for analyzing stack usage in ARM embedded projects. This Python-based analyzer provides detailed insights into function call graphs, stack consumption patterns, and peak memory usage estimates.

## Features

- **Comprehensive Analysis**: Analyzes object files and stack usage data to build complete call graphs
- **Visual Reports**: Color-coded output with clear categorization and formatting
- **File-based Grouping**: Organizes results by source files for better project understanding
- **Configurable Filtering**: Adjustable thresholds to focus on significant stack consumers
- **Peak Usage Estimation**: Calculates worst-case stack usage scenarios including interrupt handling
- **Symbol Resolution**: Handles complex symbol resolution across multiple object files
- **Professional Output**: Clean, readable reports suitable for documentation and code reviews
- **JSON Export**: Export analysis data to JSON format for automation and CI/CD integration
- **JSON Reading**: Read and filter existing JSON analysis files with threshold-based filtering
- **Comparison Mode**: Compare stack usage between different builds with git-diff style output
- **Multiple Output Formats**: Standard report, JSON output, or short function list
- **Function Pointer Detection**: RTL-based detection of function pointer calls for accurate unbounded analysis
- **Git Integration**: Automatically includes git repository information in analysis reports
- **Zephyr/CMake Support**: Handles both `.o` and `.c.obj` object file formats

## Requirements

### System Requirements
- Python 3.6 or higher
- ARM GCC toolchain (`arm-none-eabi-objdump`)
- Project compiled with `-fstack-usage` flag

### Build System Requirements
Your project must be compiled with the `-fstack-usage` compiler flag to generate the required `.su` files:

```cmake
# CMakeLists.txt example
target_compile_options(your_target PRIVATE -fstack-usage)
```

Or for Makefile-based projects:
```makefile
CFLAGS += -fstack-usage
```

### Enhanced Analysis (Optional)
For function pointer detection and enhanced unbounded analysis, also compile with RTL dumps:

```cmake
# Enhanced analysis with function pointer detection
target_compile_options(your_target PRIVATE -fstack-usage -fdump-rtl-dfinish)
```

## Installation

### Option 1: Install via pip (Recommended)

```bash
pip install arm-stack-analyzer
```

After installation, the `arm-stack` command will be available globally:

```bash
arm-stack --version
arm-stack build/
```

### Option 2: Install from source

```bash
git clone https://github.com/wizath/arm-stack.git
cd arm-stack
pip install .
```

### Option 3: Direct script usage

1. Clone or download the `arm-stack` script
2. Ensure Python 3.6+ is installed
3. Make the script executable: `chmod +x arm-stack`
4. Run directly: `./arm-stack build/`

### Prerequisites

Verify ARM toolchain is available:
```bash
arm-none-eabi-objdump --version
```

## Usage

### Basic Usage
```bash
./arm-stack <build_directory>
```

### Advanced Options
```bash
# Set custom threshold (default: 10 bytes)
arm-stack build --threshold 50

# Disable colored output
arm-stack build --no-color

# Suppress symbol resolution warnings
arm-stack build --no-warnings

# Export analysis data to JSON file
arm-stack build --export-json analysis.json

# Output JSON to stdout (for automation)
arm-stack build --json > analysis.json

# Short output mode (function list only)
arm-stack build --short

# Compare two analysis files
arm-stack --compare old_analysis.json new_analysis.json

# Read and display JSON analysis file
arm-stack --read-json analysis.json

# Filter JSON analysis by threshold
arm-stack --read-json analysis.json --threshold 100

# Custom objdump path
arm-stack build --objdump /path/to/arm-none-eabi-objdump

# Show version information
arm-stack --version

# Combine options
arm-stack cmake-build-debug --threshold 100 --no-warnings --export-json results.json
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `build_dir` | Build directory containing object files | Required |
| `--threshold N` | Minimum stack usage threshold in bytes | 10 |
| `--no-color` | Disable colored output | False |
| `--no-warnings` | Suppress warning messages | False |
| `--export-json FILE` | Export analysis data to JSON file | None |
| `--json` | Output JSON to stdout | False |
| `--short` | Output only function list with stack usage | False |
| `--objdump PATH` | Path to objdump executable | arm-none-eabi-objdump |
| `--compare OLD NEW` | Compare two JSON analysis files | None |
| `--read-json FILE` | Read and display JSON analysis file | None |

## Output Format

The analyzer generates a comprehensive report with several sections:

### 1. Stack Usage by Source File
```
main.c
  - main (1024 bytes)
  - init_system (256 bytes)
  - process_data (128 bytes)
  Total: 1408 bytes (3 functions)

stm32wlxx_hal_uart.c
  - HAL_UART_Transmit (512 bytes)
  - UART_WaitOnFlagUntilTimeout (256 bytes)
  Total: 768 bytes (2 functions)
```

### 2. Function Stack Usage Analysis
```
Flag Function Name                        Total   Frame   Depth
───── ──────────────────────────────────── ─────── ─────── ─────
▶     main                                 1024    64      15
🔄    recursive_function                   512     32      8
      helper_function                      128     24      3
```

**Legend:**
- `▶` Root function (entry point)
- `🔄` Recursive function
- `⚠` Function pointer call (unbounded)
- `❌` Unbounded function (other reasons)
- **Total**: Frame size + maximum callee cost
- **Frame**: Local variables and call overhead
- **Depth**: Maximum call chain length

### 3. Analysis Summary
```
📊 ANALYSIS SUMMARY
Peak execution estimate:
   Main function cost:       1024 bytes
   Worst interrupt cost:      512 bytes
   Total estimated peak:     1536 bytes

Statistics:
   Functions analyzed:         156
   Average stack usage:         45 bytes
   Maximum single function:   1024 bytes
```

## Advanced Features

### JSON Export and Automation

Export analysis data for automation, CI/CD integration, or further processing:

```bash
# Export to JSON file
arm-stack build --export-json analysis.json

# Output JSON to stdout (for piping)
arm-stack build --json | jq '.summary.total_peak_estimate'

# Short format for simple automation
arm-stack build --short | grep "main:"
```

The JSON output includes comprehensive metadata, function details, file statistics, and summary information suitable for automated analysis.

### Build Comparison

Track stack usage changes between builds:

```bash
# Analyze current build
arm-stack build --export-json current.json

# After code changes, analyze again
arm-stack build --export-json updated.json

# Compare the results
arm-stack --compare current.json updated.json
```

The comparison output shows:
- Summary statistic changes (peak usage, averages)
- Function-level changes (added/removed/modified)
- File-level aggregated changes
- Git-diff style color-coded output

### JSON Analysis and Filtering

Read and analyze existing JSON files with optional filtering:

```bash
# Display complete analysis from JSON file
arm-stack --read-json analysis.json

# Filter functions with stack usage >= 100 bytes
arm-stack --read-json analysis.json --threshold 100

# Output filtered results as JSON
arm-stack --read-json analysis.json --threshold 50 --json

# Simple function list format
arm-stack --read-json analysis.json --short
```

This feature is useful for:
- Post-processing analysis results
- Creating filtered reports for specific teams
- Automated threshold-based validation
- Integration with custom reporting tools

## Algorithm Details

### Call Graph Construction
1. **Disassembly Parsing**: Uses `arm-none-eabi-objdump` to extract function definitions and call relationships
2. **Symbol Resolution**: Resolves function calls across object files using address mappings and symbol tables
3. **Graph Building**: Constructs directed graph representing function call relationships

### Stack Cost Calculation
1. **Frame Size Extraction**: Reads `.su` files generated by `-fstack-usage` compiler flag
2. **Recursive Traversal**: Performs depth-first traversal with cycle detection
3. **Cost Computation**: Calculates total cost as `frame_size + max(callee_costs)`
4. **Peak Estimation**: Combines main execution path with worst-case interrupt scenario

### Key Features
- **Cycle Detection**: Identifies and marks recursive functions
- **Function Pointer Detection**: RTL-based analysis to detect indirect function calls
- **Unbounded Analysis**: Proper handling of functions with unbounded stack usage
- **Ambiguity Handling**: Manages functions with identical names across files
- **External Function Handling**: Tracks unresolved external library calls
- **Interrupt Analysis**: Special handling for interrupt service routines
- **Git Integration**: Automatic repository information inclusion in reports

## Troubleshooting

### Common Issues

**Error: No stack usage files (.su) found**
- Ensure compilation with `-fstack-usage` flag
- Check that build completed successfully
- Verify object files exist in build directory

**Error: arm-none-eabi-objdump not found**
- Install ARM GCC toolchain
- Add toolchain to system PATH
- Verify installation: `arm-none-eabi-objdump --version`

**Warning: Ambiguous resolution**
- Multiple functions with same name across files
- Use `--no-warnings` to suppress if not critical
- Consider function name uniqueness in code

**Empty or minimal results**
- Check threshold setting (try `--threshold 1`)
- Verify object files contain debug information
- Ensure project uses standard ARM calling conventions

### Debug Tips

1. **Verify Prerequisites**: Run with verbose output to see file discovery
2. **Check Object Files**: Ensure `.o` or `.c.obj` files exist and contain symbols
3. **Validate .su Files**: Check that `.su` or `.c.su` files are generated and contain data
4. **Test with Lower Threshold**: Use `arm-stack build --threshold 1` to see all functions
5. **Use JSON Export**: Export data with `--export-json` for detailed analysis
6. **Compare Builds**: Use `--compare` to track changes between builds

## Contributing

Contributions are welcome! Areas for improvement:
- Additional output formats (CSV, HTML, XML)
- Enhanced visualization options (graphs, charts)
- Support for other architectures (RISC-V, x86)
- Performance optimizations for large projects
- IDE integrations and plugins
- Web-based analysis dashboard

### Development Setup

```bash
git clone https://github.com/wizath/arm-stack.git
cd arm-stack
pip install -e .[dev]
```

This installs the package in development mode with additional tools for testing and linting.

## License

MIT License - see LICENSE file for details.
