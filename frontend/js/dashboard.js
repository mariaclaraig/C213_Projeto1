const estadoApp = {
    arquivo: null,
    dataset: null,
    identificacao: null,
    metodoIdentificacao: "smith",
    sintonia: null,
};

const CHAVE_AUTENTICACAO = "c213_login_ok";

function mostrarSecao(secaoAtiva) {
    const secoes = document.querySelectorAll(".secao");
    const botoes = document.querySelectorAll(".nav-btn");

    secoes.forEach((secao) => {
        const deveMostrar = secao.id === `sec-${secaoAtiva}`;
        secao.classList.toggle("hidden", !deveMostrar);
    });

    botoes.forEach((botao) => {
        botao.classList.toggle("active", botao.dataset.section === secaoAtiva);
    });
}

function formatarNumero(valor, casas = 4) {
    if (valor === null || valor === undefined || Number.isNaN(Number(valor))) {
        return "-";
    }

    if (!Number.isFinite(Number(valor))) {
        return "inf";
    }

    return Number(valor).toFixed(casas);
}

function atualizarTexto(id, valor) {
    const elemento = document.getElementById(id);

    if (elemento) {
        elemento.textContent = valor;
    }
}

function obterMetodoSelecionado() {
    const selectMetodoId = document.getElementById("selectMetodoId");

    if (!selectMetodoId) {
        return "smith";
    }

    return selectMetodoId.value;
}

function obterResultadoMetodo() {
    if (!estadoApp.identificacao) {
        return null;
    }

    return estadoApp.identificacao[estadoApp.metodoIdentificacao] || null;
}

function atualizarCamposIdentificacao() {
    const resultadoMetodo = obterResultadoMetodo();

    if (!resultadoMetodo) {
        atualizarTexto("val-k", "-");
        atualizarTexto("val-tau", "-");
        atualizarTexto("val-theta", "-");
        atualizarTexto("val-eqm", "-");
        return;
    }

    atualizarTexto("val-k", formatarNumero(resultadoMetodo.k));
    atualizarTexto("val-tau", formatarNumero(resultadoMetodo.tau));
    atualizarTexto("val-theta", formatarNumero(resultadoMetodo.theta));
    atualizarTexto("val-eqm", formatarNumero(resultadoMetodo.eqm, 6));
}

function atualizarGraficoIdentificacao() {
    const dataset = estadoApp.dataset;
    const resultadoMetodo = obterResultadoMetodo();

    if (!dataset || !resultadoMetodo) {
        plotarVazio(
            "graficoIdentificacao",
            "Identificacao do Sistema",
            "Carregue um arquivo e execute a identificação para visualizar o modelo."
        );
        return;
    }

    const nomeMetodo = estadoApp.metodoIdentificacao === "smith" ? "Smith" : "Sundaresan";

    plotarIdentificacao(
        dataset.t,
        dataset.y,
        resultadoMetodo.t_modelo,
        resultadoMetodo.y_modelo,
        dataset.unidade_y || "-",
        dataset.grandeza_y || "Saida",
        nomeMetodo
    );
}

function atualizarBadgeRecomendado() {
    const badge = document.getElementById("badgeRecomendado");

    if (!badge || !estadoApp.identificacao) {
        return;
    }

    const recomendado = estadoApp.identificacao.recomendado;
    const nomeMetodo = estadoApp.metodoIdentificacao === "smith" ? "Smith" : "Sundaresan";
    const isRecomendado = recomendado === estadoApp.metodoIdentificacao;

    badge.textContent = isRecomendado ? `Recomendado: ${nomeMetodo}` : `Comparando: ${nomeMetodo}`;
}

function atualizarVisualizacaoIdentificacao() {
    atualizarCamposIdentificacao();
    atualizarBadgeRecomendado();
    atualizarGraficoIdentificacao();
}

function atualizarEstadoCamposPid() {
    const metodo = document.getElementById("selectMetodo")?.value;
    const kp = document.getElementById("campo-Kp");
    const ti = document.getElementById("campo-Ti");
    const td = document.getElementById("campo-Td");

    if (!kp || !ti || !td) {
        return;
    }

    const isManual = metodo === "Manual";
    kp.readOnly = !isManual;
    ti.readOnly = !isManual;
    td.readOnly = !isManual;

    if (!isManual) {
        kp.value = "";
        ti.value = "";
        td.value = "";
    }
}

function preencherCamposPid(parametros) {
    const kp = document.getElementById("campo-Kp");
    const ti = document.getElementById("campo-Ti");
    const td = document.getElementById("campo-Td");

    if (!kp || !ti || !td || !parametros) {
        return;
    }

    kp.value = parametros.Kp ?? "";
    ti.value = parametros.Ti ?? "";
    td.value = parametros.Td ?? "";
}

function atualizarMetricasControle(resultado) {
    if (!resultado) {
        atualizarTexto("val-tr", "-");
        atualizarTexto("val-ts", "-");
        atualizarTexto("val-mp", "-");
        atualizarTexto("val-ess", "-");
        return;
    }

    atualizarTexto("val-tr", formatarNumero(resultado.tr));
    atualizarTexto("val-ts", formatarNumero(resultado.ts));
    atualizarTexto("val-mp", formatarNumero(resultado.Mp));
    atualizarTexto("val-ess", formatarNumero(resultado.ess, 6));
}

function obterParametrosManuais() {
    const kp = Number(document.getElementById("campo-Kp")?.value);
    const ti = Number(document.getElementById("campo-Ti")?.value);
    const td = Number(document.getElementById("campo-Td")?.value);

    if ([kp, ti, td].some((valor) => !Number.isFinite(valor))) {
        throw new Error("Preencha Kp, Ti e Td manualmente antes de simular.");
    }

    return { Kp: kp, Ti: ti, Td: td };
}

function inicializarGraficos() {
    plotarVazio(
        "graficoIdentificacao",
        "Identificacao do Sistema",
        "Carregue um arquivo .mat para comparar a resposta experimental com o modelo."
    );
    plotarVazio(
        "graficoMalhaFechada",
        "Resposta em Malha Fechada",
        "Execute a sintonia PID para visualizar a simulação do sistema."
    );
}

async function executarIdentificacao() {
    if (!estadoApp.arquivo) {
        throw new Error("Selecione um arquivo .mat antes de identificar.");
    }

    const btnIdentificar = document.getElementById("btnIdentificar");

    if (btnIdentificar) {
        btnIdentificar.disabled = true;
        btnIdentificar.textContent = "Identificando...";
    }

    try {
        estadoApp.dataset = await uploadMat(estadoApp.arquivo);
        estadoApp.identificacao = await identificar(estadoApp.dataset.t, estadoApp.dataset.y, estadoApp.dataset.u);
        estadoApp.metodoIdentificacao = estadoApp.identificacao.recomendado || "smith";

        const seletor = document.getElementById("seletorIdentificacao");
        const selectMetodoId = document.getElementById("selectMetodoId");

        if (seletor) {
            seletor.classList.remove("hidden");
        }

        if (selectMetodoId) {
            selectMetodoId.value = estadoApp.metodoIdentificacao;
        }

        atualizarVisualizacaoIdentificacao();
        mostrarSecao("identificacao");
    } finally {
        if (btnIdentificar) {
            btnIdentificar.disabled = false;
            btnIdentificar.textContent = "Identificação";
        }
    }
}

async function executarSintoniaESimulacao() {
    const resultadoMetodo = obterResultadoMetodo();

    if (!resultadoMetodo) {
        throw new Error("Execute a identificação antes de simular o controlador.");
    }

    const metodo = document.getElementById("selectMetodo")?.value || "CHR";
    const setpoint = Number(document.getElementById("inputSetpoint")?.value || 1);
    const btnSimular = document.getElementById("btnSimular");

    if (!Number.isFinite(setpoint)) {
        throw new Error("Informe um valor válido para o setpoint.");
    }

    if (btnSimular) {
        btnSimular.disabled = true;
        btnSimular.textContent = "Simulando...";
    }

    try {
        const k = resultadoMetodo.k;
        const tau = resultadoMetodo.tau;
        const theta = resultadoMetodo.theta;

        let parametrosPid;

        if (metodo === "Manual") {
            const manual = obterParametrosManuais();
            parametrosPid = await sintonizar(k, tau, theta, metodo, manual.Kp, manual.Ti, manual.Td);
        } else {
            parametrosPid = await sintonizar(k, tau, theta, metodo);
        }

        estadoApp.sintonia = parametrosPid;
        preencherCamposPid(parametrosPid);

        const simulacao = await simular(
            k,
            tau,
            theta,
            parametrosPid.Kp,
            parametrosPid.Ti,
            parametrosPid.Td,
            setpoint
        );

        atualizarMetricasControle(simulacao);
        plotarMalhaFechada(simulacao.t, simulacao.y, setpoint, simulacao.tr, simulacao.ts);
        mostrarSecao("controle");
    } finally {
        if (btnSimular) {
            btnSimular.disabled = false;
            btnSimular.textContent = "Sintonia PID";
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (sessionStorage.getItem(CHAVE_AUTENTICACAO) !== "true") {
        window.location.href = "index.html";
        return;
    }

    const inputMat = document.getElementById("inputMat");
    const nomeArquivo = document.getElementById("nomeArquivo");
    const btnIdentificar = document.getElementById("btnIdentificar");
    const selectMetodoId = document.getElementById("selectMetodoId");
    const selectMetodo = document.getElementById("selectMetodo");
    const btnSimular = document.getElementById("btnSimular");

    mostrarSecao("identificao");
    atualizarEstadoCamposPid();
    atualizarMetricasControle(null);
    inicializarGraficos();

    if (inputMat && nomeArquivo && btnIdentificar) {
        inputMat.addEventListener("change", () => {
            const arquivo = inputMat.files && inputMat.files[0];
            estadoApp.arquivo = arquivo || null;

            if (arquivo) {
                nomeArquivo.textContent = arquivo.name;
                btnIdentificar.disabled = false;
                return;
            }

            nomeArquivo.textContent = "Nenhum arquivo selecionado";
            btnIdentificar.disabled = true;
        });

        btnIdentificar.addEventListener("click", async () => {
            try {
                await executarIdentificacao();
            } catch (error) {
                alert(error.message || "Falha ao identificar o sistema.");
            }
        });
    }

    if (selectMetodoId) {
        selectMetodoId.addEventListener("change", () => {
            estadoApp.metodoIdentificacao = selectMetodoId.value;
            atualizarVisualizacaoIdentificacao();
        });
    }

    if (selectMetodo) {
        selectMetodo.addEventListener("change", () => {
            atualizarEstadoCamposPid();
        });
    }

    if (btnSimular) {
        btnSimular.addEventListener("click", async () => {
            try {
                await executarSintoniaESimulacao();
            } catch (error) {
                alert(error.message || "Falha ao simular o controlador.");
            }
        });
    }
});
