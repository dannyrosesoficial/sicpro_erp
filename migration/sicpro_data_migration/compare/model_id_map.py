#!/usr/bin/env python3

from pathlib import Path
import csv

BASE = Path("/opt/odoo/migration/sicpro_data_migration")
FILE_15 = BASE / "inventory" / "ir_model_15.txt"
FILE_19 = BASE / "inventory" / "ir_model_19.txt"
OUTPUT = BASE / "compare" / "model_id_map.csv"


def load_models(path):
    models = {}

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")

            if not line:
                continue

            parts = line.split("|", 3)

            if len(parts) != 4:
                raise ValueError(
                    f"Registro inválido en {path}: {line!r}"
                )

            record_id, model, name, state = parts

            if model in models:
                raise ValueError(
                    f"Modelo duplicado en {path}: {model}"
                )

            models[model] = {
                "id": int(record_id),
                "name": name,
                "state": state,
            }

    return models


def main():
    models_15 = load_models(FILE_15)
    models_19 = load_models(FILE_19)

    all_models = sorted(set(models_15) | set(models_19))

    same_id = 0
    different_id = 0
    only_15 = 0
    only_19 = 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "model",
            "id_15",
            "id_19",
            "status",
            "name_15",
            "name_19",
            "state_15",
            "state_19",
        ])

        for model in all_models:
            record_15 = models_15.get(model)
            record_19 = models_19.get(model)

            if record_15 and record_19:
                if record_15["id"] == record_19["id"]:
                    status = "SAME_ID"
                    same_id += 1
                else:
                    status = "DIFFERENT_ID"
                    different_id += 1

                writer.writerow([
                    model,
                    record_15["id"],
                    record_19["id"],
                    status,
                    record_15["name"],
                    record_19["name"],
                    record_15["state"],
                    record_19["state"],
                ])

            elif record_15:
                only_15 += 1

                writer.writerow([
                    model,
                    record_15["id"],
                    "",
                    "ONLY_15",
                    record_15["name"],
                    "",
                    record_15["state"],
                    "",
                ])

            else:
                only_19 += 1

                writer.writerow([
                    model,
                    "",
                    record_19["id"],
                    "ONLY_19",
                    "",
                    record_19["name"],
                    "",
                    record_19["state"],
                ])

    print(f"Modelos Odoo 15: {len(models_15)}")
    print(f"Modelos Odoo 19: {len(models_19)}")
    print(f"Comunes con mismo ID: {same_id}")
    print(f"Comunes con ID diferente: {different_id}")
    print(f"Solo Odoo 15: {only_15}")
    print(f"Solo Odoo 19: {only_19}")
    print(f"Mapa generado: {OUTPUT}")


if __name__ == "__main__":
    main()
