

### Dependencies

This module depends on:
- `base` - Odoo base module
- `web` - Odoo web framework

## Usage

### Add CKEditor Widget to Form View

Use the `widget="ckeditor"` attribute on Text or Html fields:

```xml
<record id="view_form_example" model="ir.ui.view">
    <field name="model">your.model</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <group>
                    <field name="description" widget="ckeditor"/>
                    <field name="html_content" widget="ckeditor"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

### Field Types

The CKEditor widget supports:
- **Text fields**: `fields.Text()`
- **Html fields**: `fields.Html()`

## Editor Features

### Toolbar Features

**Text Formatting**:
- Bold, Italic, Underline, Strikethrough
- Font family and size selection
- Font color and background color
- Text alignment (left, center, right, justify)

**Content Structure**:
- Headings (H1-H6)
- Paragraphs and line breaks
- Bulleted and numbered lists
- Todo/checklist lists
- Block quotes
- Code blocks

**Media & Links**:
- Image insertion and upload
- Image resizing (25%, 50%, 75%, original)
- Image alignment and styling
- Image captions and alt text
- Link insertion and editing

**Tables**:
- Table creation and editing
- Row and column management
- Cell merging and splitting
- Table properties and cell properties

**Advanced Features**:
- HTML source editing
- Find and replace
- Undo/redo functionality
- HTML embed support

### Image Upload

The widget integrates with Odoo's attachment system:

**Upload Process**:
1. User inserts image via toolbar or drag-and-drop
2. Image uploads to Odoo as attachment
3. Image displays in editor with full styling options

**Supported Image Operations**:
- Upload from computer
- Resize with percentage or pixel values
- Alignment (inline, block, left, center, right, side)
- Image captions and alternative text
- Link images to URLs

