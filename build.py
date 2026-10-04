#!/usr/bin/env python3
"""Build the two data-only JARs with Python 3.11+; no game or Gradle needed."""
import argparse
import hashlib
import json
from pathlib import Path
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parent
CELLS = {
    "forge1201": ("forge-1.20.1", "mods.toml", 15, 28),
    "neoforge1211": ("neoforge-1.21.1", "neoforge.mods.toml", 48, 20),
}


def build(cell_name, output_dir):
    suffix, metadata_name, pack_format, item_count = CELLS[cell_name]
    cell = ROOT / "ports" / cell_name
    metadata = cell / "src/META-INF" / metadata_name
    mod = tomllib.loads(metadata.read_text())["mods"][0]
    if (mod["modId"], mod["version"], mod["displayName"]) != (
        "relics_emc", "0.1.0", "EMC for Relics"
    ):
        raise ValueError("Unexpected mod metadata")
    pack = cell / "src/pack.mcmeta"
    if json.loads(pack.read_text())["pack"]["pack_format"] != pack_format:
        raise ValueError("Unexpected resource pack format")
    conversion = cell / "src/data/relics_emc/pe_custom_conversions/relics_emc.json"
    values = json.loads(conversion.read_text())["values"]["before"]
    if cell_name == "forge1201":
        if not isinstance(values, dict):
            raise ValueError("Forge ProjectE requires the item-to-EMC map")
        pairs = list(values.items())
    else:
        if not isinstance(values, list) or any(v["type"] != "projecte:item" for v in values):
            raise ValueError("NeoForge ProjectE requires the item record array")
        pairs = [(v["id"], v["emc_value"]) for v in values]
    if len(pairs) != item_count or len({item for item, _ in pairs}) != item_count:
        raise ValueError("Unexpected or duplicate priced item IDs")
    if any(not item.startswith("relics:") or type(value) is not int or value <= 0
           or value % 1024 for item, value in pairs):
        raise ValueError("Invalid authored item price")
    entries = {
        "LICENSE_relics_emc": (cell / "LICENSE").read_bytes(),
        "META-INF/" + metadata_name: metadata.read_bytes(),
        "pack.mcmeta": pack.read_bytes(),
        "data/relics_emc/pe_custom_conversions/relics_emc.json": conversion.read_bytes(),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"emc-for-relics-0.1.0+{suffix}.jar"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as jar:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            jar.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output) as jar:
        if jar.testzip() or set(jar.namelist()) != set(entries):
            raise ValueError("JAR entry or CRC mismatch")
        if any(jar.read(name) != data for name, data in entries.items()):
            raise ValueError("Packaged source mismatch")
    data = output.read_bytes()
    print(f"{output.name}: {len(data)} bytes, SHA-256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cell", choices=CELLS, help="Build one port; default builds both")
    parser.add_argument("--output", type=Path, default=ROOT / "build")
    args = parser.parse_args()
    for cell_name in ([args.cell] if args.cell else CELLS):
        build(cell_name, args.output)
