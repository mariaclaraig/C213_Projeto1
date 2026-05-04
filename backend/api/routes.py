import os
import tempfile
from typing import Optional

import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.models.identificacao import identificar_sistemas
from backend.models.sintonia import (
    sintonizar_cc,
    sintonizar_chr,
    sintonizar_manual,
    validar_estabilidade,
)
from backend.utils.data_loader import carregar_mat
from backend.utils.simulation import simular_malha_fechada


router = APIRouter()


class IdentificacaoRequest(BaseModel):
    t: list[float]
    y: list[float]
    u: list[float]


class SintoniaRequest(BaseModel):
    k: float
    tau: float
    theta: float
    metodo: str
    Kp: Optional[float] = None
    Ti: Optional[float] = None
    Td: Optional[float] = None


class SimulacaoRequest(BaseModel):
    k: float
    tau: float
    theta: float
    Kp: float
    Ti: float
    Td: float
    setpoint: float


@router.post("/upload")
async def upload_mat(arquivo: UploadFile = File(...)):
    if not arquivo.filename.lower().endswith(".mat"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .mat.")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mat") as temp:
            temp.write(await arquivo.read())
            temp_path = temp.name

        dados = carregar_mat(temp_path)

        return {
            "t": dados["t"].tolist(),
            "y": dados["y"].tolist(),
            "u": dados["u"].tolist(),
            "unidade_t": dados["unidade_t"],
            "unidade_y": dados["unidade_y"],
            "grandeza_y": dados["grandeza_y"],
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/identificar")
def identificar(payload: IdentificacaoRequest):
    try:
        return identificar_sistemas(
            np.array(payload.t, dtype=float),
            np.array(payload.y, dtype=float),
            np.array(payload.u, dtype=float),
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/sintonizar")
def sintonizar(payload: SintoniaRequest):
    try:
        metodo = payload.metodo

        if metodo == "CHR":
            return sintonizar_chr(payload.k, payload.tau, payload.theta)

        if metodo == "CC":
            return sintonizar_cc(payload.k, payload.tau, payload.theta)

        if metodo == "Manual":
            if None in (payload.Kp, payload.Ti, payload.Td):
                raise HTTPException(
                    status_code=400,
                    detail="Preencha Kp, Ti e Td para o modo Manual.",
                )

            estavel, msg = validar_estabilidade(
                payload.k,
                payload.tau,
                payload.theta,
                payload.Kp,
                payload.Ti,
                payload.Td,
            )

            if not estavel:
                raise HTTPException(status_code=400, detail=f"Sistema instavel: {msg}")

            return sintonizar_manual(payload.Kp, payload.Ti, payload.Td)

        raise HTTPException(status_code=400, detail=f"Metodo desconhecido: {metodo}")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/simular")
def simular(payload: SimulacaoRequest):
    try:
        return simular_malha_fechada(
            k=payload.k,
            tau=payload.tau,
            theta=payload.theta,
            Kp=payload.Kp,
            Ti=payload.Ti,
            Td=payload.Td,
            setpoint=payload.setpoint,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
