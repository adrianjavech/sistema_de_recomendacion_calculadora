# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
import requests

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxJU8Ttz8XmHAflHu14xFw65aZ0ot0yKxl1u_g1kgBX6hvAjYJxSE4tKG7lUJ--blV7/exec"
ARCHIVO_LOG = "registro_uso.csv"

COLUMNAS = [
    "fecha_hora",
    "sesion_id",
    "usuario",
    "evento",
    "plan",
    "continuidad",
    "num_asegurados",
    "edades",
    "prima_total",
    "num_cuotas",
    "financiamiento",
    "cuota_mensual",
    "detalle",
]


def registrar_evento(evento, sesion_id="", usuario="", **datos):
    fila = {c: "" for c in COLUMNAS}
    fila.update({k: v for k, v in datos.items() if k in COLUMNAS})
    fila["fecha_hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fila["sesion_id"] = sesion_id
    fila["usuario"] = usuario
    fila["evento"] = evento
    try:
        requests.post(WEBHOOK_URL, json=fila, timeout=5)
        return True
    except Exception:
        return False


def leer_log():
    try:
        res = requests.get(WEBHOOK_URL, timeout=5).json()
        if len(res) <= 1:
            return pd.DataFrame(columns=COLUMNAS)
        return pd.DataFrame(res[1:], columns=res[0])
    except Exception:
        return pd.DataFrame(columns=COLUMNAS)
