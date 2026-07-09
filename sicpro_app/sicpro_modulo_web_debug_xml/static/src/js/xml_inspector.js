/** @odoo-module **/

import { Component, onMounted, onPatched } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

class XMLInspector {
    constructor() {
        this.active = false;
        this.overlay = null;
        this.currentElement = null;
        this.locked = false;
        this.env = null;
    }

    toggle() {
        this.active = !this.active;
        
        if (this.active) {
            this.activate();
        } else {
            this.deactivate();
        }
    }

    activate() {
        document.body.style.cursor = 'crosshair';
        this.createOverlay();
        this.attachListeners();
        
        const notification = document.createElement('div');
        notification.className = 'xml-inspector-notification';
        notification.textContent = '🔍 Inspector XML activado - Hover over elements';
        document.body.appendChild(notification);
        
        setTimeout(() => notification.remove(), 3000);
    }

    deactivate() {
        document.body.style.cursor = '';
        this.active = false;
        this.locked = false;
        this.currentElement = null;
        
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
        
        this.removeListeners();
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'xml-inspector-overlay';
        document.body.appendChild(this.overlay);
    }

    attachListeners() {
        this.mouseMoveHandler = this.onMouseMove.bind(this);
        this.clickHandler = this.onClick.bind(this);
        this.keyHandler = this.onKeyPress.bind(this);
        
        document.addEventListener('mousemove', this.mouseMoveHandler, true);
        document.addEventListener('click', this.clickHandler, true);
        document.addEventListener('keydown', this.keyHandler, true);
    }

    removeListeners() {
        document.removeEventListener('mousemove', this.mouseMoveHandler, true);
        document.removeEventListener('click', this.clickHandler, true);
        document.removeEventListener('keydown', this.keyHandler, true);
    }

    onMouseMove(e) {
        if (this.locked) return;
        
        const target = e.target;
        if (target === this.overlay) {
            return;
        }
        
        if (target.tagName === 'I' || 
            target.tagName === 'SPAN' && (target.className.includes('fa') || target.className.includes('oi'))) {
            if (this.overlay) {
                this.overlay.style.display = 'none';
            }
            return;
        }
        
        if (target.closest('.o_field_widget_tooltip') || 
            target.closest('.o_tooltip') ||
            target.closest('[data-tooltip]') ||
            target.closest('.tooltip')) {
            if (this.overlay) {
                this.overlay.style.display = 'none';
            }
            return;
        }
        
        const rect = target.getBoundingClientRect();
        if (rect.width < 30 && rect.height < 30 && target.tagName !== 'INPUT') {
            if (this.overlay) {
                this.overlay.style.display = 'none';
            }
            return;
        }
        
        const formSheet = target.closest('.o_form_sheet');
        if (!formSheet) {
            if (this.overlay) {
                this.overlay.style.display = 'none';
            }
            return;
        }
        
        this.highlightElement(target);
    }

    onClick(e) {
        const target = e.target;
        
        if (target.tagName === 'I' || 
            target.tagName === 'SPAN' && (target.className.includes('fa') || target.className.includes('oi'))) {
            e.preventDefault();
            e.stopPropagation();
            return;
        }
        
        if (target.closest('.o_field_widget_tooltip') || 
            target.closest('.o_tooltip') ||
            target.closest('[data-tooltip]') ||
            target.closest('.tooltip')) {
            e.preventDefault();
            e.stopPropagation();
            return;
        }
        
        const rect = target.getBoundingClientRect();
        if (rect.width < 30 && rect.height < 30 && target.tagName !== 'INPUT') {
            e.preventDefault();
            e.stopPropagation();
            return;
        }
        
        const formSheet = target.closest('.o_form_sheet');
        if (!formSheet) {
            return;
        }
        
        e.preventDefault();
        e.stopPropagation();
        
        this.showDetailedInfo(target);
    }

    onKeyPress(e) {
        if (e.key === 'Escape') {
            this.toggle();
        }
    }

    highlightElement(element) {
        const rect = element.getBoundingClientRect();
        this.overlay.style.display = 'block';
        this.overlay.style.top = rect.top + window.scrollY + 'px';
        this.overlay.style.left = rect.left + window.scrollX + 'px';
        this.overlay.style.width = rect.width + 'px';
        this.overlay.style.height = rect.height + 'px';
    }


    async showDetailedInfo(element) {
        const info = this.extractElementInfo(element);
        
        if (info.viewType !== 'form' || !this.env) {
            this.deactivate();
            return;
        }
        
        if (!info.viewId && info.model) {
            try {
                const viewInfo = await rpc('/web/dataset/call_kw', {
                    model: info.model,
                    method: 'get_views',
                    args: [],
                    kwargs: {
                        views: [[false, 'form']],
                        options: {
                            toolbar: false
                        }
                    }
                });
                
                if (viewInfo && viewInfo.views) {
                    if (viewInfo.views.form && viewInfo.views.form.id) {
                        info.viewId = viewInfo.views.form.id;
                    } else if (viewInfo.views.form && viewInfo.views.form.view_id) {
                        info.viewId = viewInfo.views.form.view_id;
                    }
                }
            } catch (error) {
                this.deactivate();
                return;
            }
        }
        
        if (!info.viewId) {
            this.deactivate();
            return;
        }
        
        try {
            const viewData = await rpc('/web/dataset/call_kw', {
                model: 'ir.ui.view',
                method: 'read',
                args: [[parseInt(info.viewId)], ['arch', 'name', 'model']],
                kwargs: {}
            });
            
            if (viewData && viewData.length > 0) {
                const baseArch = viewData[0].arch;
                let elementInfo = this.findElementInXML(element, baseArch);
                let finalViewId = info.viewId;
                
                if (!elementInfo.found) {
                    const inheritedViews = await rpc('/web/dataset/call_kw', {
                        model: 'ir.ui.view',
                        method: 'search_read',
                        args: [],
                        kwargs: {
                            domain: [
                                ['model', '=', info.model],
                                ['type', '=', 'form'],
                                ['mode', '=', 'extension']
                            ],
                            fields: ['id', 'name', 'arch', 'inherit_id']
                        }
                    });
                    
                    for (const inheritedView of inheritedViews) {
                        const inheritedElementInfo = this.findElementInXML(element, inheritedView.arch);
                        if (inheritedElementInfo.found) {
                            elementInfo = inheritedElementInfo;
                            finalViewId = inheritedView.id;
                            break;
                        }
                    }
                }
                
                this.deactivate();
                
                await this.env.services.action.doAction({
                    type: 'ir.actions.act_window',
                    res_model: 'ir.ui.view',
                    res_id: parseInt(finalViewId),
                    views: [[false, 'form']],
                    target: 'new',
                    context: {
                        'default_type': info.viewType || 'form',
                    }
                });
                
                if (elementInfo.found && elementInfo.lineNumber > 0) {
                    setTimeout(() => {
                        this.highlightLineInViewForm(elementInfo);
                    }, 1000);
                }
            }
        } catch (error) {
            this.deactivate();
        }
    }
    
    findElementInXML(element, xml) {
        const result = { found: false, pattern: '', description: '', lineNumber: 0, xmlTag: '' };
        
        let current = element;
        let depth = 0;
        
        while (current && current !== document.body && depth < 10) {
            const owlComponent = current.getAttribute('data-owl-component');
            
            if (current.classList && Array.from(current.classList).some(c => c.startsWith('o_field_'))) {
                const name = current.getAttribute('name');
                if (name) {
                    const searchResult = this.searchInXML(xml, `name="${name}"`, 'field');
                    if (searchResult.found) {
                        searchResult.xmlTag = 'field';
                        return searchResult;
                    }
                }
            }
            
            if (current.classList?.contains('o_form_label') || (element.tagName === 'LABEL' && element.hasAttribute('for'))) {
                const forAttr = element.getAttribute('for') || current.getAttribute('for');
                if (forAttr) {
                    const fieldName = forAttr.replace(/_\d+$/, '');
                    const searchResult = this.searchInXML(xml, `name="${fieldName}"`, 'field');
                    if (searchResult.found) {
                        searchResult.xmlTag = 'field';
                        searchResult.description = `field name="${fieldName}" (from label)`;
                        return searchResult;
                    }
                }
            }
            
            if (current.classList?.contains('o_group') || current.classList?.contains('o_inner_group')) {
                const titleElement = current.querySelector(':scope > .o_horizontal_separator');
                if (titleElement) {
                    const groupTitle = titleElement.textContent?.trim();
                    if (groupTitle) {
                        const searchResult = this.searchInXML(xml, `string="${groupTitle}"`, 'group');
                        if (searchResult.found) {
                            searchResult.xmlTag = 'group';
                            return searchResult;
                        }
                    }
                }
            }
            
            if (current.classList?.contains('o_notebook')) {
                const activePage = current.querySelector('.tab-pane.active');
                if (activePage) {
                    const tabId = activePage.getAttribute('id');
                    if (tabId) {
                        const tabLink = document.querySelector(`[href="#${tabId}"]`);
                        if (tabLink) {
                            const pageTitle = tabLink.textContent?.trim();
                            if (pageTitle) {
                                const searchResult = this.searchInXML(xml, `string="${pageTitle}"`, 'page');
                                if (searchResult.found) {
                                    searchResult.xmlTag = 'page';
                                    return searchResult;
                                }
                            }
                        }
                    }
                }
            }
            
            if (current.classList?.contains('o_horizontal_separator')) {
                const separatorText = current.textContent?.trim();
                if (separatorText) {
                    let searchResult = this.searchInXML(xml, `string="${separatorText}"`, 'group');
                    if (searchResult.found) {
                        searchResult.xmlTag = 'group';
                        return searchResult;
                    }
                    searchResult = this.searchInXML(xml, `string="${separatorText}"`, 'separator');
                    if (searchResult.found) {
                        searchResult.xmlTag = 'separator';
                        return searchResult;
                    }
                }
            }
            
            if (current.tagName === 'BUTTON' || current.classList?.contains('btn')) {
                const name = current.getAttribute('name');
                const buttonText = current.textContent?.trim();
                
                if (name) {
                    const searchResult = this.searchInXML(xml, `name="${name}"`, 'button');
                    if (searchResult.found) {
                        searchResult.xmlTag = 'button';
                        return searchResult;
                    }
                }
                
                if (buttonText && buttonText.length < 50) {
                    const searchResult = this.searchInXML(xml, `string="${buttonText}"`, 'button');
                    if (searchResult.found) {
                        searchResult.xmlTag = 'button';
                        return searchResult;
                    }
                }
            }
            
            const name = current.getAttribute('name');
            if (name) {
                const searchResult = this.searchInXML(xml, `name="${name}"`);
                if (searchResult.found) {
                    searchResult.description = depth === 0 ? `name="${name}"` : `name="${name}" (parent element)`;
                    return searchResult;
                }
            }
            
            current = current.parentElement;
            depth++;
        }
        
        return result;
    }
    
    searchInXML(xml, searchValue, xmlTag = null) {
        const result = { found: false, pattern: '', description: '', lineNumber: 0 };
        
        const patterns = [
            searchValue,
            searchValue.replace(/"/g, "'"),
        ];
        
        for (const pattern of patterns) {
            if (xml.includes(pattern)) {
                const lines = xml.split('\n');
                for (let i = 0; i < lines.length; i++) {
                    const line = lines[i];
                    if (xmlTag && !line.includes(`<${xmlTag}`)) {
                        continue;
                    }
                    if (line.includes(pattern)) {
                        result.found = true;
                        result.pattern = pattern;
                        result.description = xmlTag ? `${xmlTag} ${pattern}` : pattern;
                        result.lineNumber = i + 1;
                        return result;
                    }
                }
            }
        }
        
        return result;
    }
    
    highlightLineInViewForm(elementInfo) {
        try {
            let attempts = 0;
            const maxAttempts = 20;
            
            const tryHighlight = () => {
                attempts++;
                
                const modal = document.querySelector('.modal.o_technical_modal, .modal.show, .o_dialog');
                if (!modal && attempts < maxAttempts) {
                    setTimeout(tryHighlight, 100);
                    return;
                }
                
                if (!modal) {
                    return;
                }
                
                
                const archTab = modal.querySelector('[name="arch"], .nav-link[name="arch"]');
                if (archTab && !archTab.classList.contains('active')) {
                    archTab.click();
                }
                
                const checkEditor = () => {
                    const aceEditor = modal.querySelector('.ace_editor');
                    if (!aceEditor) {
                        if (attempts < maxAttempts) {
                            attempts++;
                            setTimeout(checkEditor, 50);
                        }
                        return;
                    }
                    
                    const aceLines = aceEditor.querySelectorAll('.ace_line');
                    if (aceLines.length === 0 && attempts < maxAttempts) {
                        attempts++;
                        setTimeout(checkEditor, 50);
                        return;
                    }
                    
                    if (aceLines.length >= elementInfo.lineNumber) {
                        const targetLine = aceLines[elementInfo.lineNumber - 1];
                        if (targetLine) {
                            const lineText = targetLine.textContent.trim();
                            
                            let startLine = elementInfo.lineNumber - 1;
                            let endLine = elementInfo.lineNumber - 1;
                            
                            if (lineText.includes('<') && !lineText.includes('/>') && !lineText.includes('</')) {
                                const tagMatch = lineText.match(/<(\w+)/);
                                if (tagMatch) {
                                    const tagName = tagMatch[1];
                                    
                                    let depth = 1;
                                    for (let i = elementInfo.lineNumber; i < aceLines.length; i++) {
                                        const currentLineText = aceLines[i].textContent.trim();
                                        
                                        const openTags = (currentLineText.match(new RegExp(`<${tagName}[\\s>]`, 'g')) || []).length;
                                        const closeTags = (currentLineText.match(new RegExp(`</${tagName}>`, 'g')) || []).length;
                                        
                                        depth += openTags - closeTags;
                                        
                                        if (depth === 0) {
                                            endLine = i;
                                            break;
                                        }
                                    }
                                }
                            }
                            
                            
                            const highlightClass = 'xml-inspector-highlight-' + Date.now();
                            const style = document.createElement('style');
                            style.textContent = `
                                .${highlightClass} {
                                    background: rgba(135, 206, 250, 0.3) !important;
                                    animation: xmlInspectorPulse 2s ease-in-out;
                                }
                                .${highlightClass}:first-child {
                                    border-left: 4px solid #4CAF50 !important;
                                    padding-left: 4px !important;
                                }
                                @keyframes xmlInspectorPulse {
                                    0%, 100% { background: rgba(135, 206, 250, 0.3) !important; }
                                    50% { background: rgba(135, 206, 250, 0.5) !important; }
                                }
                            `;
                            document.head.appendChild(style);
                            
                            for (let i = startLine; i <= endLine; i++) {
                                if (aceLines[i]) {
                                    aceLines[i].classList.add(highlightClass);
                                }
                            }
                            
                            targetLine.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            
                            setTimeout(() => {
                                for (let i = startLine; i <= endLine; i++) {
                                    if (aceLines[i]) {
                                        aceLines[i].classList.remove(highlightClass);
                                    }
                                }
                                style.remove();
                            }, 5000);
                            return;
                        }
                    }
                    
                    const codeContainer = modal.querySelector('.o_field_text, .o_field_xml, pre, code, .ace_content');
                    if (!codeContainer) {
                        return;
                    }
                    
                    
                    const allSpans = codeContainer.querySelectorAll('span');
                    
                    if (allSpans.length > 0) {
                        let currentLine = 1;
                        let targetSpan = null;
                        
                        for (const span of allSpans) {
                            const text = span.textContent;
                            if (text.includes('\n')) {
                                currentLine += (text.match(/\n/g) || []).length;
                            }
                            
                            if (currentLine >= elementInfo.lineNumber && !targetSpan) {
                                targetSpan = span;
                                break;
                            }
                            
                            if (!text.includes('\n')) {
                                currentLine++;
                            }
                        }
                        
                        if (targetSpan) {
                            targetSpan.style.background = 'rgba(135, 206, 250, 0.5)';
                            targetSpan.style.borderLeft = '4px solid #4CAF50';
                            targetSpan.style.paddingLeft = '8px';
                            targetSpan.style.display = 'block';
                            
                            targetSpan.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            
                            setTimeout(() => {
                                targetSpan.style.background = '';
                                targetSpan.style.borderLeft = '';
                                targetSpan.style.paddingLeft = '';
                                targetSpan.style.display = '';
                            }, 4000);
                        } else {
                            if (elementInfo.pattern) {
                                for (const span of allSpans) {
                                    if (span.textContent.includes(elementInfo.pattern.replace(/"/g, ''))) {
                                        span.style.background = 'rgba(255, 193, 7, 0.5)';
                                        span.style.padding = '2px 4px';
                                        span.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                        
                                        setTimeout(() => {
                                            span.style.background = '';
                                            span.style.padding = '';
                                        }, 4000);
                                        break;
                                    }
                                }
                            }
                        }
                    } else {
                        const text = codeContainer.textContent;
                        const lines = text.split('\n');
                        
                        if (elementInfo.lineNumber > 0 && elementInfo.lineNumber <= lines.length) {
                            const targetText = lines[elementInfo.lineNumber - 1];
                            
                            if (elementInfo.pattern && codeContainer.innerHTML) {
                                const escapedPattern = elementInfo.pattern
                                    .replace(/&/g, '&amp;')
                                    .replace(/</g, '&lt;')
                                    .replace(/>/g, '&gt;');
                                
                                codeContainer.innerHTML = codeContainer.innerHTML.replace(
                                    escapedPattern,
                                    `<mark style="background: rgba(135, 206, 250, 0.7); padding: 2px 4px; border-left: 4px solid #4CAF50;">${escapedPattern}</mark>`
                                );
                                
                                const mark = codeContainer.querySelector('mark');
                                if (mark) {
                                    mark.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                }
                            }
                        }
                    }
                };
                
                checkEditor();
            };
            
            tryHighlight();
        } catch (error) {
        }
    }

    extractElementInfo(element) {
        const info = {};
        
        let current = element;
        let depth = 0;
        while (current && current !== document.body && depth < 20) {
            if (current.hasAttribute('data-owl-component')) {
                info.component = current.getAttribute('data-owl-component');
            }
            if (current.hasAttribute('data-owl-template')) {
                info.template = current.getAttribute('data-owl-template');
            }
            if (current.dataset) {
                if (current.dataset.resModel) {
                    info.model = current.dataset.resModel;
                }
                if (current.dataset.viewId) {
                    info.viewId = current.dataset.viewId;
                }
            }
            
            if (current.hasAttribute('data-view-id')) {
                info.viewId = current.getAttribute('data-view-id');
            }
            
            if (info.component && info.template) break;
            
            current = current.parentElement;
        }
        
        if (element.className) {
            info.classes = Array.from(element.classList).slice(0, 5).join(', ');
        }
        
        try {
            if (this.env && this.env.services) {
                const actionService = this.env.services.action;
                
                if (actionService && actionService.currentController) {
                    const controller = actionService.currentController;
                    
                    if (controller.view) {
                        if (controller.view.viewId) {
                            info.viewId = controller.view.viewId;
                        }
                        if (controller.view.type) {
                            info.viewType = controller.view.type;
                        }
                    }
                    
                    if (controller.props) {
                        if (controller.props.resModel) {
                            info.model = controller.props.resModel;
                        }
                        if (controller.props.viewId) {
                            info.viewId = controller.props.viewId;
                        }
                    }
                    
                    if (controller.action) {
                        if (controller.action.res_model && !info.model) {
                            info.model = controller.action.res_model;
                        }
                        if (controller.action.views && !info.viewId) {
                            const currentView = controller.action.views.find(v => v[1] === info.viewType);
                            if (currentView && currentView[0]) {
                                info.viewId = currentView[0];
                            }
                        }
                    }
                    
                    if (controller.model && controller.model.config) {
                        const config = controller.model.config;
                        if (config.resModel && !info.model) {
                            info.model = config.resModel;
                        }
                        if (config.viewId && !info.viewId) {
                            info.viewId = config.viewId;
                        }
                    }
                    
                    if (!info.viewId && controller.views) {
                        const formView = controller.views.find(v => v.type === 'form');
                        if (formView && formView.viewId) {
                            info.viewId = formView.viewId;
                        }
                    }
                    
                    if (!info.viewId && controller.config && controller.config.views) {
                        const formView = controller.config.views.find(v => v[1] === 'form');
                        if (formView && formView[0]) {
                            info.viewId = formView[0];
                        }
                    }
                    
                    if (!info.viewId && controller.action && controller.action.controllers) {
                        if (controller.action.controllers.form && controller.action.controllers.form.viewId) {
                            info.viewId = controller.action.controllers.form.viewId;
                        }
                    }
                }
            }
        } catch (e) {
        }
        
        return info;
    }
}

const xmlInspector = new XMLInspector();

patch(Component.prototype, {
    setup() {
        super.setup(...arguments);
        
        const componentName = this.constructor.name;
        const componentTemplate = this.constructor.template;
        
        onMounted(() => {
            this._injectXMLInfo(componentName, componentTemplate);
        });
        
        onPatched(() => {
            this._injectXMLInfo(componentName, componentTemplate);
        });
    },
    
    _injectXMLInfo(componentName, componentTemplate) {
        if (!this.el) return;
        
        const rootElement = this.el;
        
        if (rootElement && rootElement.nodeType === Node.ELEMENT_NODE) {
            rootElement.setAttribute('data-owl-component', componentName);
            
            if (componentTemplate) {
                rootElement.setAttribute('data-owl-template', componentTemplate);
            }
            
            if (this.props) {
                const propsInfo = {};
                for (const key in this.props) {
                    if (this.props.hasOwnProperty(key)) {
                        const value = this.props[key];
                        if (typeof value !== 'function' && typeof value !== 'object') {
                            propsInfo[key] = value;
                        }
                    }
                }
                if (Object.keys(propsInfo).length > 0) {
                    rootElement.setAttribute('data-owl-props', JSON.stringify(propsInfo));
                }
            }
        }
    }
});

function inspectXMLMode({ env }) {
    const actionService = env.services.action;
    const currentController = actionService?.currentController;
    const viewType = currentController?.view?.type;
    
    if (viewType !== 'form') {
        return null;
    }
    
    xmlInspector.env = env;
    return {
        type: "item",
        description: "Inspección modo XML avanzado",
        callback: () => {
            xmlInspector.toggle();
        },
        sequence: 250,
        section: "ui",
    };
}

registry
    .category("debug")
    .category("default")
    .add("inspectXMLMode", inspectXMLMode);
