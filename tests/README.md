# Tests Organization

This directory contains all test files organized by category.

## Directory Structure

### 📁 `tests/unit/`
Unit tests for individual components and methods:
- `test_enhanced_autotune_logic.py` - Logic validation for enhanced auto-tune methods
- `test_enhanced_autotune.py` - Enhanced auto-tune methods testing
- `test_auto_tune_fix.py` - Auto-tune corrections and fixes
- `test_beer_lambert_reset.py` - Beer-Lambert reset functionality
- `test_reset_autotune.py` - Auto-tune reset mechanisms
- `test_fusion_default.py` - Multiscale fusion default parameters
- `test_udcp.py` - UDCP algorithm testing
- `test_white_balance.py` - White balance methods testing
- `test_localization.py` - Localization and translation testing
- `test_loading_flag.py` - Loading state management
- `test_translations.py` - Translation system testing

### 📁 `tests/integration/`
Integration tests for full workflow validation:
- `test_integration_final.py` - Final integration validation
- `test_auto_tune.py` - Auto-tune integration testing
- `test_final_functionality.py` - Complete functionality testing
- `test_pipeline.py` - Processing pipeline integration

### 📁 `tests/ui/`
User interface tests:
- `test_interface.py` - Main interface testing
- `test_button_translation.py` - Button localization
- `test_parameter_updates.py` - Parameter UI updates
- `test_manual_buttons.py` - Manual control buttons
- `test_rotation_*.py` - Image rotation functionality
- `test_reset.py` - UI reset functionality
- `test_enable_disable.py` - Enable/disable controls
- `test_dark_mode.py` - Dark mode interface
- `test_global_reset.py` - Global reset functionality
- `test_auto_tune_checkboxes.py` - Auto-tune checkbox controls

### 📁 `tests/performance/`
Performance and optimization tests:
- `test_performance.py` - Performance benchmarking
- `test_multiscale_fusion.py` - Multiscale fusion performance
- `test_subsampling.py` - Subsampling optimization

### 📁 `tests/analysis/`
Analysis and validation tools:
- `analyze_autotune_methods.py` - Auto-tune methods analysis
- `analyze_default_params.py` - Default parameters analysis
- `validate_improvements.py` - Improvements validation

### 📁 `tests/fixtures/`
Test data and sample files:
- `test_*.jpg` - Sample images for testing

## Running Tests

### All Tests
```bash
python -m pytest tests/
```

### Specific Categories
```bash
# Unit tests only
python -m pytest tests/unit/

# Integration tests only  
python -m pytest tests/integration/

# UI tests only
python -m pytest tests/ui/

# Performance tests only
python -m pytest tests/performance/
```

### Individual Test Files
```bash
python -m pytest tests/unit/test_enhanced_autotune_logic.py
```

## Development Tools

### 📁 `tools/`
Development and implementation utilities:
- `implement_enhanced_autotune.py` - Enhanced auto-tune implementation script

## Test Guidelines

1. **Unit tests** should test individual functions/methods in isolation
2. **Integration tests** should test component interactions and workflows
3. **UI tests** should validate user interface behavior and responsiveness
4. **Performance tests** should benchmark execution times and resource usage
5. **Analysis tools** should provide insights and validation of improvements

## Adding New Tests

When adding new tests:
1. Place them in the appropriate category directory
2. Follow the naming convention `test_*.py`
3. Include docstrings explaining the test purpose
4. Add any required fixtures to `tests/fixtures/`
5. Update this README if adding new categories
