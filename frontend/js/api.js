const API_BASE = "http://localhost:8000/api";

async function extrairErro(resp) {
    try {
        const data = await resp.json();

        if (data && data.detail) {
            return data.detail;
        }
    } catch (error) {
        return `Erro HTTP ${resp.status}`;
    }

    return `Erro HTTP ${resp.status}`;
}

async function uploadMat(arquivo) {
    const formData = new FormData();
    formData.append("arquivo", arquivo);

    const resp = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
    });

    if (!resp.ok) {
        throw new Error(await extrairErro(resp));
    }

    return resp.json();
}

async function identificar(t, y, u) {
    const resp = await fetch(`${API_BASE}/identificar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ t, y, u }),
    });

    if (!resp.ok) {
        throw new Error(await extrairErro(resp));
    }

    return resp.json();
}

async function sintonizar(k, tau, theta, metodo, Kp = null, Ti = null, Td = null) {
    const resp = await fetch(`${API_BASE}/sintonizar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ k, tau, theta, metodo, Kp, Ti, Td }),
    });

    if (!resp.ok) {
        throw new Error(await extrairErro(resp));
    }

    return resp.json();
}

async function simular(k, tau, theta, Kp, Ti, Td, setpoint) {
    const resp = await fetch(`${API_BASE}/simular`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ k, tau, theta, Kp, Ti, Td, setpoint }),
    });

    if (!resp.ok) {
        throw new Error(await extrairErro(resp));
    }

    return resp.json();
}
