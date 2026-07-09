import { useEffect } from "@odoo/owl";
import { session } from "@web/session"; // Importamos session para leer lo que enviamos desde Python
import { useBus, useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";

export class AppsMenu extends Dropdown {
    setup() {
        super.setup();
        this.commandPaletteOpen = false;
        this.commandService = useService("command");

        // 1. Prioridad: Imagen global de SICPRO enviada por session_info
        if (session.has_background_image && session.theme_background_image) {
            // Como es Base64, construimos el data URI directamente
            this.imageUrl = `data:image/png;base64,${session.theme_background_image}`;
        }
        // 2. Backup: Imagen por defecto del módulo
        else {
            this.imageUrl = '/sicpro_modulo_tema_visual/static/src/img/background-dark.jpg';
        }

        useEffect(
            (isOpen) => {
                if (isOpen) {
                    const openMainPalette = (ev) => {
                        if (
                            !this.commandPaletteOpen &&
                            ev.key.length === 1 &&
                            !ev.ctrlKey &&
                            !ev.altKey
                        ) {
                            this.commandService.openMainPalette(
                                { searchValue: `/${ev.key}` },
                                () => { this.commandPaletteOpen = false; }
                            );
                            this.commandPaletteOpen = true;
                        }
                    }
                    window.addEventListener("keydown", openMainPalette);
                    return () => {
                        window.removeEventListener("keydown", openMainPalette);
                        this.commandPaletteOpen = false;
                    }
                }
            },
            () => [this.state.isOpen]
        );

        useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", () => {
            if (this.state.close) {
                this.state.close();
            }
        });
    }

    onOpened() {
        super.onOpened();
        // Aplicamos el fondo al abrir el menú de aplicaciones
        if (this.menuRef && this.menuRef.el) {
            this.menuRef.el.style.backgroundImage = `url('${this.imageUrl}')`;
            this.menuRef.el.style.backgroundSize = 'cover';
            this.menuRef.el.style.backgroundPosition = 'center';
        }
    }
}