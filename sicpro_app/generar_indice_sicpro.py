from pathlib import Path
import ast
import json

ROOT = Path("sicpro_app")
OUTPUT = Path("SICPRO_ERP_Indice_Arquitectura.md")


def read_manifest(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
                return ast.literal_eval(node.value)
    except Exception:
        pass

    return {}


def python_summary(path):
    result = {
        "models": [],
        "transient_models": [],
        "classes": [],
        "methods": [],
    }

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)

                bases = []
                for base in node.bases:
                    try:
                        bases.append(ast.unparse(base))
                    except Exception:
                        pass

                if any(
                    "Model" in base and "TransientModel" not in base
                    for base in bases
                ):
                    result["models"].append(node.name)

                if any("TransientModel" in base for base in bases):
                    result["transient_models"].append(node.name)

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                result["methods"].append(node.name)

    except Exception:
        pass

    return result


def relative(path):
    return path.relative_to(ROOT).as_posix()


modules = []

if not ROOT.exists():
    raise SystemExit(
        f"No se encontró la carpeta: {ROOT.resolve()}"
    )

for module_path in sorted(p for p in ROOT.iterdir() if p.is_dir()):

    manifest_path = module_path / "__manifest__.py"

    if not manifest_path.exists():
        continue

    manifest = read_manifest(manifest_path)

    module = {
        "name": module_path.name,
        "path": module_path.as_posix(),
        "manifest": manifest,
        "python_files": [],
        "xml_files": [],
        "js_files": [],
        "csv_files": [],
        "scss_css_files": [],
        "qweb_files": [],
        "models": [],
        "transient_models": [],
    }

    for file in module_path.rglob("*"):

        if not file.is_file():
            continue

        suffix = file.suffix.lower()

        if suffix == ".py":
            module["python_files"].append(relative(file))

            summary = python_summary(file)

            module["models"].extend(summary["models"])
            module["transient_models"].extend(
                summary["transient_models"]
            )

        elif suffix == ".xml":
            module["xml_files"].append(relative(file))

        elif suffix == ".js":
            module["js_files"].append(relative(file))

        elif suffix == ".csv":
            module["csv_files"].append(relative(file))

        elif suffix in {".scss", ".css"}:
            module["scss_css_files"].append(relative(file))

        elif "qweb" in file.parts:
            module["qweb_files"].append(relative(file))

    for key in (
        "python_files",
        "xml_files",
        "js_files",
        "csv_files",
        "scss_css_files",
        "qweb_files",
        "models",
        "transient_models",
    ):
        module[key] = sorted(set(module[key]))

    modules.append(module)


with OUTPUT.open("w", encoding="utf-8") as f:

    f.write("# SICPRO ERP — Índice de Arquitectura\n\n")

    f.write(
        "> Índice generado automáticamente desde el árbol local "
        "del proyecto. Este documento no modifica ningún archivo "
        "del código fuente.\n\n"
    )

    f.write(f"## Módulos detectados: {len(modules)}\n\n")

    for module in modules:

        manifest = module["manifest"]

        f.write(f"## {module['name']}\n\n")

        f.write(f"**Ruta:** `{module['path']}`\n\n")

        if manifest:
            f.write("### Manifest\n\n")

            for key in (
                "name",
                "version",
                "category",
                "summary",
                "description",
                "license",
                "application",
                "installable",
            ):
                if key in manifest:
                    value = manifest[key]

                    if isinstance(value, str):
                        value = value.replace("\n", " ")

                    f.write(f"- **{key}:** `{value}`\n")

            dependencies = manifest.get("depends", [])

            if dependencies:
                f.write("\n**Dependencias:**\n\n")

                for dependency in dependencies:
                    f.write(f"- `{dependency}`\n")

        if module["models"]:
            f.write("\n### Modelos Python\n\n")

            for model in module["models"]:
                f.write(f"- `{model}`\n")

        if module["transient_models"]:
            f.write("\n### Wizards / TransientModel\n\n")

            for model in module["transient_models"]:
                f.write(f"- `{model}`\n")

        if module["python_files"]:
            f.write("\n### Python\n\n")

            for path in module["python_files"]:
                f.write(f"- `{path}`\n")

        if module["xml_files"]:
            f.write("\n### XML\n\n")

            for path in module["xml_files"]:
                f.write(f"- `{path}`\n")

        if module["js_files"]:
            f.write("\n### JavaScript / OWL\n\n")

            for path in module["js_files"]:
                f.write(f"- `{path}`\n")

        if module["csv_files"]:
            f.write("\n### CSV / Seguridad / Datos\n\n")

            for path in module["csv_files"]:
                f.write(f"- `{path}`\n")

        if module["scss_css_files"]:
            f.write("\n### CSS / SCSS\n\n")

            for path in module["scss_css_files"]:
                f.write(f"- `{path}`\n")

        f.write("\n---\n\n")


print()
print("Índice generado correctamente.")
print(f"Módulos encontrados: {len(modules)}")
print(f"Archivo: {OUTPUT.resolve()}")
