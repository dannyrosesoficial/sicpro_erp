/** @odoo-module **/

import {registry} from '@web/core/registry';
import { user } from "@web/core/user";
import {loadCSS, loadJS} from '@web/core/assets';
import {standardFieldProps} from '@web/views/fields/standard_field_props';

import {
    Component,
    onMounted,
    onWillUnmount,
    onWillUpdateProps,
    onWillStart,
    useEffect,
    useRef,
    useState,
} from '@odoo/owl';

import {UploadAdapterPlugin} from './UploadAdapterPlugin';


function formatLang(lang) {
    if (!lang) {
        return 'en'
    }
    else if (lang === 'zh_CN') {
        return 'zh-cn';
    } else {
        return lang.split('-')[0];
    }
}


export class CkEditorField extends Component {

    static template = 'sicpro_modulo_widget_ckeditor.CkEditorField';

    static props = {
        ...standardFieldProps,
    };

    get propsValue() {
        return this.props.record.data[this.props.name];
    }

    setup() {
        super.setup();
        this.textareaRef = useRef('textarea');
        this.state = useState({
            value: this.propsValue.toString(),
        });
        this.editor = null;
        this.changeTimeout = null;

        onWillStart(async () => {
            await Promise.all([
                window.CKEDITOR_GLOBAL_LICENSE_KEY = 'GPL',
                loadJS('/sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/ckeditor5.umd.js'),
                this.loadEditorLanguage(),
            ]);
        });

        onMounted(async () => {
            try {
                const editor = await this.loadCKEditor();
                this.editor = editor;
            } catch (error) {
                console.error('No se pudo inicializar CKEditor:', error);
            }
        });

        onWillUpdateProps((nextProps) => {
            if (this.editor) {
                this.state.value = nextProps.record.data[nextProps.name].toString();
                this.editor.setData(this.state.value);
            }
        });

        onWillUnmount(() => {
            // Clean up timeout
            if (this.changeTimeout) {
                clearTimeout(this.changeTimeout);
                this.changeTimeout = null;
            }

            // Clean up editor instance
            if (this.editor) {
                try {
                    this.editor.destroy();
                } catch (error) {
                    console.error('Error al destruir CKEditor:', error);
                } finally {
                    this.editor = null;
                }
            }
        });

        useEffect(() => {
            const value = this.propsValue.toString();
            if (!this.props.record.dirty && value !== this.state.value) {
                this.state.value = value;
                if (this.editor && this.editor.setData) {
                    this.editor.setData(value);
                }
            }
        });

    };

    async loadEditorLanguage() {
        const lang = formatLang(user.lang)
        if (lang === 'en') return;
        try {
            await loadJS(`/sicpro_modulo_widget_ckeditor/static/lib/ckeditor5/translations/${lang}.umd.js`);
        } catch (error) {
            console.warn('No se puede cargar el idioma de CKEditor: ', lang);
        }
    }

    getCKEditorPlugins() {
        return [
            CKEDITOR.GeneralHtmlSupport,
            CKEDITOR.HtmlEmbed,
            CKEDITOR.Essentials,
            CKEDITOR.Bold,
            CKEDITOR.Italic,
            CKEDITOR.Underline,
            CKEDITOR.Strikethrough,
            CKEDITOR.Font,
            CKEDITOR.Paragraph,
            CKEDITOR.Heading,
            CKEDITOR.BlockQuote,
            CKEDITOR.CodeBlock,
            CKEDITOR.List,
            CKEDITOR.Image,
            CKEDITOR.ImageResize,
            CKEDITOR.ImageInsert,
            CKEDITOR.ImageToolbar,
            CKEDITOR.ImageUpload,
            CKEDITOR.ImageUploadUI,
            CKEDITOR.ImageCaption,
            CKEDITOR.Link,
            CKEDITOR.Table,
            CKEDITOR.TableToolbar,
            CKEDITOR.PlainTableOutput,
            CKEDITOR.SourceEditing,
            CKEDITOR.Alignment,
            CKEDITOR.FindAndReplace,
            CKEDITOR.EmptyBlock,
            CKEDITOR.CustomElementSupport,
        ]
    }

    async loadCKEditor() {
        const rawInitialData = this.props.record.data[this.props.name].toString();

        const editor = await CKEDITOR.ClassicEditor
            .create(document.querySelector('#editor'), {
                plugins: this.getCKEditorPlugins(),
                extraPlugins: [UploadAdapterPlugin],
                uploadAdapter: {
                    uploadUrl: '/web/binary/upload_attachment',
                    token: odoo.csrf_token,
                    model: this.props.record.resModel,
                    recordId: this.props.record.resId,
                },
                allowedContent: true,
                toolbar: {
                    items: [
                        'undo', 'redo', '|',
                        'heading', '|',
                        'bold', 'italic', 'underline', 'strikethrough', '|',
                        'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
                        'alignment', '|',
                        'bulletedList', 'numberedList', '|',
                        'link', 'insertImage', 'insertTable', '|',
                        'blockQuote', 'codeBlock', '|',
                        'findAndReplace', 'sourceEditing', '|',
                    ],
                    shouldNotGroupWhenFull: true
                },
                image: {
                    toolbar: [
                        'imageStyle:inline',
                        'imageStyle:block',
                        'imageStyle:side',
                        'imageStyle:alignLeft',
                        'imageStyle:alignCenter',
                        'imageStyle:alignRight',
                        '|',
                        'toggleImageCaption',
                        'imageTextAlternative',
                        '|',
                        'linkImage'
                    ],
                    // Enable image resizing with handles
                    resizeUnit: 'px',
                    resizeOptions: [
                        {
                            name: 'resizeImage:original',
                            value: null,
                            label: 'Original'
                        },
                        {
                            name: 'resizeImage:25',
                            value: '25',
                            label: '25%'
                        },
                        {
                            name: 'resizeImage:50',
                            value: '50',
                            label: '50%'
                        },
                        {
                            name: 'resizeImage:75',
                            value: '75',
                            label: '75%'
                        }
                    ]
                },
                table: {
                    contentToolbar: [
                        'tableColumn', 'tableRow', 'mergeTableCells',
                        'tableProperties', 'tableCellProperties'
                    ]
                },
                htmlSupport: {
                    allowEmpty: [
                        'a', 'abbr', 'address', 'article', 'aside', 'b', 'button', 'canvas', 'caption', 'cite', 'code',
                        'div', 'em', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'i', 'img', 'input',
                        'label', 'li', 'link', 'main', 'nav', 'p', 's', 'section', 'small', 'span', 'strong', 'sub', 'sup',
                        'table', 'tbody', 'thead', 'tfoot', 'tr', 'td', 'th', 'u', 'var',
                        't'
                    ],
                    allow: [
                        {
                            name: /.*/,
                            attributes: true,
                            classes: true,
                            styles: true
                        },
                        {
                            name: 't',
                            attributes: true,
                        },
                    ],
                },
                list: {
                    properties: {
                        styles: true,
                        startIndex: true,
                        reversed: true
                    }
                },
                initialData: rawInitialData
            }).then(editor => {
                return editor;
            })
            .catch(error => {
                console.error('Error al crear CKEditor:', error);
                throw error;
            });

        if (this.props.readonly) {
            editor.isReadOnly = true;
        } else {
            let changeTimeout;
            editor.model.document.on('change', () => {
                clearTimeout(changeTimeout);
                changeTimeout = setTimeout(() => {
                    this._onChange();
                }, 300); // Debounce changes
            });

            // Also listen for direct content changes
            editor.editing.view.document.on('blur', () => {
                this._onChange();
            });
        }

        return editor;
    };

    _onChange() {
        if (!this.editor) return;

        const newValue = this.editor.getData();

        const currentValue = this.propsValue.toString();
        if (newValue !== currentValue) {
            this.state.value = newValue;

            this.props.record.update({
                [this.props.name]: newValue
            });
        }
    };

}

export const ckeditorField = {
    component: CkEditorField,
    supportedTypes: ['text', 'html'],
};

registry.category('fields').add('ckeditor', ckeditorField);
