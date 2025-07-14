# Feature Plan: JavaScript/JSON Formatting in HTML Attributes

## Overview
Add support for formatting JavaScript and JSON content within HTML attributes, extending djLint's existing formatting capabilities.

## Current State Analysis

### Existing JavaScript Formatter
- **Library**: jsbeautifier (≥1.14.4)
- **Location**: `/src/djlint/formatter/js.py:19`
- **Current scope**: Formats JavaScript inside `<script>` tags only
- **Configuration**: Uses `config.js_config` with BeautifierOptions

### HTML Attribute Formatting Pipeline
- **Main function**: `format_attributes()` in `/src/djlint/formatter/attributes.py`
- **Integration point**: Called from `/src/djlint/formatter/indent.py:269-273`
- **Current capabilities**: 
  - Multi-line attribute formatting based on length
  - Style attribute formatting (semicolon breaks)
  - Template tag formatting within attributes
  - Quote preservation

## Proposed Implementation

### 1. Formatter Selection Strategy
- **JSON Objects**: Use Python's built-in `json` module for formatting
- **JavaScript Objects**: Use existing `jsbeautifier` with same config as `<script>` tags
- **Detection Logic**: 
  - Primary: Curly brace detection (`{...}` pattern)
  - Secondary: Configurable JavaScript attribute list

### 2. Trigger Conditions
- **Length-based**: Only format when attribute exceeds `max_attribute_length` (existing config)
- **Content-based**: Only format detected JavaScript/JSON objects
- **Configurable**: New setting to enable/disable this feature

### 3. Key Requirements
- **Preserve indentation**: Maintain existing HTML indentation context
- **Multi-line only**: Format only when attribute would be multi-line anyway
- **Quote preservation**: Maintain original quote style (single/double)
- **Error handling**: Gracefully handle malformed JS/JSON

## Technical Details

### Integration Points
1. **Detection**: Extend `format_attributes()` function
2. **Formatting**: Create helper functions for JS/JSON formatting
3. **Configuration**: Add new config options
4. **Testing**: Add comprehensive test cases

### Configuration Options (Proposed)
- `format_js_attributes`: Boolean flag to enable/disable feature
- `js_attribute_names`: List of attribute names to treat as JavaScript
- Reuse existing `max_attribute_length` for trigger condition

### Error Handling
- Malformed JavaScript/JSON should fall back to original content
- Preserve original formatting if parsing fails
- Log warnings for debugging (if applicable)

## Extended Planning Details

### JSON vs JavaScript Distinction

**JSON Detection & Formatting:**
- **Pattern**: Attributes starting and ending with `{` and `}`
- **Validation**: Use `json.loads()` to validate JSON syntax
- **Formatting**: Use `json.dumps()` with HTML-relative indentation using JS formatter indent size
- **Indentation**: Extract indent size from `config.js_config["indent_size"]` or default
- **Fallback**: If JSON parsing fails, treat as JavaScript

**JavaScript Detection & Formatting:**
- **Pattern**: Attributes starting and ending with `{` and `}` that fail JSON validation
- **Validation**: Basic syntax check (balanced braces, no obvious syntax errors)
- **Formatting**: Use existing `jsbeautifier` with `config.js_config`
- **Fallback**: If formatting fails, preserve original content

### Indent Preservation Strategy

**Current Context Analysis:**
- `max_attribute_length` config: Default 70 characters (settings.py:679)
- Trigger condition: `len(match.group(3).strip()) < config.max_attribute_length` (attributes.py:126-128)
- Existing indentation: `spacing = leading_space + len(tag) * " "` (attributes.py:137)

**Proposed Implementation:**
```python
def format_js_json_in_attribute(config, attribute_value, base_indent):
    """Format JS/JSON while preserving HTML indentation context."""
    # Skip formatting for single-property objects
    if has_single_property(attribute_value):
        return attribute_value
    
    # Get indent size from JS config
    indent_size = config.js_config.get("indent_size", 4)
    
    # Detect if content is JSON or JavaScript
    if is_json_object(attribute_value):
        return format_json_with_indent(attribute_value, base_indent, indent_size)
    elif is_js_object(attribute_value):
        return format_js_with_indent(attribute_value, base_indent, config)
    return attribute_value  # No formatting needed

def has_single_property(value):
    """Check if JSON/JS object has only one property."""
    try:
        # Try parsing as JSON first
        data = json.loads(value)
        return len(data) == 1
    except:
        # For JS objects, count property-like patterns
        # Simple heuristic: count comma-separated properties
        cleaned = re.sub(r'["\']([^"\']*)["\']', '', value)  # Remove strings
        property_count = len(re.findall(r'[a-zA-Z_$][a-zA-Z0-9_$]*\s*:', cleaned))
        return property_count <= 1
```

### Curly Brace Detection Logic

**Primary Detection Pattern:**
```python
def has_object_braces(value):
    """Check if attribute value contains object-like braces."""
    stripped = value.strip()
    return stripped.startswith('{') and stripped.endswith('}')
```

**Secondary Detection:**
- Check attribute name against JavaScript attribute list
- Only format if both conditions are met: object braces AND JavaScript attribute

### JavaScript Attribute Configuration

**Regex Pattern Approach:**
```python
# Default comprehensive regex pattern for JavaScript attributes
DEFAULT_JS_ATTRIBUTE_PATTERN = r'^(?:' \
    r'on[a-z]+|' \                          # HTML event handlers (onclick, onload, etc.)
    r'data-[a-z\-]+|' \                     # Data attributes (data-*, data-action, etc.)
    r'x-[a-z\-]+|' \                        # Alpine.js (x-data, x-show, etc.)
    r'@[a-z\-]+|' \                         # Alpine.js shorthand (@click, @submit, etc.)
    r':[a-z\-]+|' \                         # Alpine.js/Vue.js bind shorthand (:class, :style, etc.)
    r'v-[a-z\-]+|' \                        # Vue.js directives (v-model, v-if, etc.)
    r'\([a-z\-]+\)|' \                      # Angular event bindings ((click), (submit), etc.)
    r'\[[a-z\-]+\]|' \                      # Angular property bindings ([disabled], [class], etc.)
    r'\*ng[A-Z][a-zA-Z]*|' \                # Angular structural directives (*ngIf, *ngFor, etc.)
    r'[a-z\-]+\.(bind|delegate|call|trigger)|' \ # Aurelia (.bind, .delegate, etc.)
    r'_|' \                                 # Hyperscript underscore attribute
    r'[a-z]+[A-Z][a-zA-Z]*' \              # React camelCase (onClick, onChange, etc.)
    r')$'
```

**Configuration Options:**
- `format_js_attributes`: Boolean flag (default: False)
- `js_attribute_pattern`: Custom regex pattern (default: DEFAULT_JS_ATTRIBUTE_PATTERN)

**Usage Example:**
```python
import re

def is_js_attribute(attribute_name, pattern):
    """Check if attribute name matches JavaScript attribute pattern."""
    return re.match(pattern, attribute_name, re.IGNORECASE) is not None

# User can customize with their own pattern:
# js_attribute_pattern = r'^(?:on[a-z]+|data-[a-z\-]+|x-[a-z\-]+)$'
```

### Implementation Triggers

**Multi-condition Activation:**
1. Feature enabled via `format_js_attributes` config
2. Attribute length exceeds `max_attribute_length` (existing logic - this is the primary trigger)
3. Attribute value contains object braces `{...}`
4. Attribute name matches the JavaScript attribute regex pattern
5. Object has more than one property (skip single-property objects)

**Length-based Behavior Clarification:**
- The existing `max_attribute_length` check happens FIRST in `format_attributes()`
- If `len(match.group(3).strip()) < config.max_attribute_length`, the function returns early
- Our JS/JSON formatting only activates when attributes are already considered "too long"
- This ensures we only format when multi-line formatting would already occur

**Error Handling Strategy:**
- JSON parsing errors → fallback to JavaScript formatting
- JavaScript formatting errors → preserve original content
- Log warnings for debugging (use existing djlint logging)

**Additional Implementation Details:**
```python
def format_json_with_indent(value, base_indent, indent_size):
    """Format JSON with proper HTML-relative indentation."""
    try:
        data = json.loads(value)
        # Use indent_size spaces for JSON formatting
        formatted = json.dumps(data, indent=indent_size)
        # Add base_indent to each line (except first)
        lines = formatted.split('\n')
        if len(lines) > 1:
            indented_lines = [lines[0]] + [base_indent + line for line in lines[1:]]
            return '\n'.join(indented_lines)
        return formatted
    except:
        return value
```

## Test Case Specifications

### Test Case 1: JSON Single Property (No Formatting)
**Input:**
```html
<div data-config='{"name": "value"}'>
```
**Configuration:**
- `max_attribute_length`: 0 (force multi-line)
- `format_js_attributes`: True
- `js_attribute_pattern`: default (includes `data-*`)

**Expected Output:**
```html
<div data-config='{"name": "value"}'>
```
**Rationale:** Single property objects should skip formatting entirely

### Test Case 2: JSON Two Properties (Multi-line Formatting)
**Input:**
```html
<div data-config='{"name": "value", "enabled": true}'>
```
**Configuration:**
- `max_attribute_length`: 0 (force multi-line)
- `format_js_attributes`: True
- `js_attribute_pattern`: default (includes `data-*`)
- `js_config`: `{"indent_size": 2}`

**Expected Output:**
```html
<div data-config='{
  "name": "value",
  "enabled": true
}'>
```
**Rationale:** Multi-property JSON should be formatted with proper indentation

### Test Case 3: JavaScript Single Property (No Formatting)
**Input:**
```html
<div onclick='{action: "click"}'>
```
**Configuration:**
- `max_attribute_length`: 0 (force multi-line)
- `format_js_attributes`: True
- `js_attribute_pattern`: default (includes `on*`)

**Expected Output:**
```html
<div onclick='{action: "click"}'>
```
**Rationale:** Single property JS objects should skip formatting entirely

### Test Case 4: JavaScript Two Properties (Multi-line Formatting)
**Input:**
```html
<div onclick='{action: "click", preventDefault: true}'>
```
**Configuration:**
- `max_attribute_length`: 0 (force multi-line)
- `format_js_attributes`: True
- `js_attribute_pattern`: default (includes `on*`)
- `js_config`: `{"indent_size": 2}`

**Expected Output:**
```html
<div onclick='{
  action: "click",
  preventDefault: true
}'>
```
**Rationale:** Multi-property JS objects should be formatted with jsbeautifier

### Test Case 5: JavaScript Code Block (Multi-line Formatting)
**Input:**
```html
<div onclick='console.log("start"); var x = 1; console.log("end");'>
```
**Configuration:**
- `max_attribute_length`: 0 (force multi-line)
- `format_js_attributes`: True
- `js_attribute_pattern`: default (includes `on*`)
- `js_config`: `{"indent_size": 2}`

**Expected Output:**
```html
<div onclick='console.log("start");
var x = 1;
console.log("end");'>
```
**Rationale:** JavaScript code statements should be formatted with jsbeautifier

**Note:** Test Case 5 doesn't have curly braces, so it would need different detection logic or might be considered out of scope for the initial implementation that focuses on object detection.

## Next Steps
1. ✅ Create memory file with current plan
2. ✅ Extend planning with detailed JSON vs JS distinction  
3. ✅ Design indent preservation strategy
4. ✅ Identify existing `max_attribute_length` config
5. ✅ Design curly brace detection logic
6. ✅ Plan JavaScript attribute configuration list
7. ✅ Define test case specifications
8. Implementation and testing