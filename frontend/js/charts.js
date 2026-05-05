const layoutBase = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(255,255,255,0.03)",
    font: { color: "#ccc", family: "Inter, sans-serif" },
    margin: { t: 40, r: 20, b: 50, l: 60 },
    legend: { bgcolor: "rgba(0,0,0,0)", bordercolor: "rgba(255,255,255,0.1)" },
    xaxis: { gridcolor: "rgba(255,255,255,0.07)", zerolinecolor: "rgba(255,255,255,0.1)" },
    yaxis: { gridcolor: "rgba(255,255,255,0.07)", zerolinecolor: "rgba(255,255,255,0.1)" },
};

const plotConfig = {
    responsive: true,
    displaylogo: false,
};

function plotarVazio(containerId, titulo, mensagem) {
    Plotly.newPlot(
        containerId,
        [],
        {
            ...layoutBase,
            title: titulo,
            annotations: [
                {
                    text: mensagem,
                    showarrow: false,
                    font: { color: "#9ba3c7", size: 14 },
                },
            ],
            xaxis: { ...layoutBase.xaxis, visible: false },
            yaxis: { ...layoutBase.yaxis, visible: false },
        },
        plotConfig
    );
}

function plotarIdentificacao(t, yExp, tModelo, yModelo, unidadeY, grandezaY, nomeMetodo) {
    const traces = [
        {
            x: t,
            y: yExp,
            name: "Experimental",
            line: { color: "#7c6bff", width: 2.5 },
        },
        {
            x: tModelo,
            y: yModelo,
            name: `Modelo FOPDT (${nomeMetodo})`,
            line: { color: "#ff6b9d", width: 2, dash: "dash" },
        },
    ];

    const layout = {
        ...layoutBase,
        title: `Identificação - Método de ${nomeMetodo}`,
        xaxis: { ...layoutBase.xaxis, title: "Tempo (s)" },
        yaxis: { ...layoutBase.yaxis, title: `${grandezaY} (${unidadeY})` },
    };

    Plotly.newPlot("graficoIdentificacao", traces, layout, plotConfig);
}

function plotarMalhaFechada(t, y, setpoint, tr, ts, td, tp) {
    const spLine = {
        x: [t[0], t[t.length - 1]],
        y: [setpoint, setpoint],
        name: "SetPoint",
        line: { color: "#ffd166", dash: "dot", width: 1.5 },
    };

    const resposta = {
        x: t,
        y: y,
        name: "Saída controlada",
        line: { color: "#06d6a0", width: 2.5 },
    };

    const yMax = Math.max(setpoint * 1.3, ...y);
    const traces = [spLine, resposta];

    if (Number.isFinite(tr)) {
        traces.push({
            x: [tr, tr],
            y: [0, yMax],
            mode: "lines",
            name: "Tempo de Subida (tr)",
            line: { color: "#ef476f", dash: "dash", width: 1.5 },
            hoverinfo: "x+name"
        });
    }

    if (Number.isFinite(td)) {
        traces.push({
            x: [td, td],
            y: [0, yMax],
            mode: "lines",
            name: "Tempo de Atraso (td)",
            line: { color: "#118ab2", dash: "dash", width: 1.5 },
            hoverinfo: "x+name"
        });
    }
    
    if (Number.isFinite(tp) && tp < Infinity) {
        traces.push({
            x: [tp, tp],
            y: [0, yMax],
            mode: "lines",
            name: "Tempo de Pico (tp)",
            line: { color: "#ff9f1c", dash: "dash", width: 1.5 },
            hoverinfo: "x+name"
        });
    }

    if (Number.isFinite(ts)) {
        traces.push({
            x: [ts, ts],
            y: [0, yMax],
            mode: "lines",
            name: "Tempo de Acomodação (ts)",
            line: { color: "#9ba3c7", dash: "dash", width: 1.5 },
            hoverinfo: "x+name"
        });
    }

    const layout = {
        ...layoutBase,
        title: "Resposta em Malha Fechada",
        xaxis: { ...layoutBase.xaxis, title: "Tempo (s)" },
        yaxis: { ...layoutBase.yaxis, title: "Saída" },
    };

    Plotly.newPlot("graficoMalhaFechada", traces, layout, plotConfig);
}
