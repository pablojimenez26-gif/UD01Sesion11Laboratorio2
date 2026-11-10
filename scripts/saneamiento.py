#!/usr/bin/env python3
"""Saneamiento de telemetria_envios.csv y cálculo de huellas SHA-256."""
import hashlib
from pathlib import Path
import pandas as pd

ORIGINAL = Path("datos/telemetria_envios.csv")
LIMPIO = Path("datos/telemetria_limpia.csv")
HASH_REFERENCIA = "4471c18a0284b3aa5b32a0713e691e3c7fcadae402f105e901c7c57f49474911"

ESTADOS_VALIDOS = {"ENTREGADO", "EN_TRANSITO", "EN_REPARTO", "INCIDENCIA_REPARTO"}
TEMP_MIN, TEMP_MAX = -30.0, 30.0


def sha256_fichero(ruta: Path) -> str:
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:                      # "rb": hash sobre bytes, no texto
        for bloque in iter(lambda: f.read(4096), b""):  # lectura por bloques: escala a GB
            sha.update(bloque)
    return sha.hexdigest()


def main():
    h_orig = sha256_fichero(ORIGINAL)
    print(f"SHA-256 original : {h_orig}")
    print(f"Coincide con referencia: {h_orig == HASH_REFERENCIA}")

    df = pd.read_csv(ORIGINAL, encoding="utf-8")
    print(f"\nFilas iniciales: {len(df)}")
    print(df.isna().sum(), "\n")

    n = len(df)
    df = df.drop_duplicates();                          print(f"Duplicados eliminados: {n - len(df)}"); n = len(df)
    df = df.dropna(subset=["peso_kg", "temp_celsius", "destino"])
    print(f"Filas con nulos eliminadas: {n - len(df)}"); n = len(df)
    df = df[df["peso_kg"] > 0];                         print(f"Pesos no positivos eliminados: {n - len(df)}"); n = len(df)
    df = df[df["temp_celsius"].between(TEMP_MIN, TEMP_MAX)]
    print(f"Temperaturas fuera de rango eliminadas: {n - len(df)}"); n = len(df)
    df = df[df["estado_envio"].isin(ESTADOS_VALIDOS)]
    print(f"Estados no catalogados eliminados: {n - len(df)}")

    assert df["id_envio"].is_unique, "Quedan id_envio repetidos"
    df.to_csv(LIMPIO, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\nFilas finales: {len(df)}")
    print(f"SHA-256 limpio   : {sha256_fichero(LIMPIO)}")


if __name__ == "__main__":
    main()