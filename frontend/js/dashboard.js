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

document.addEventListener("DOMContentLoaded", () => {
    const inputMat = document.getElementById("inputMat");
    const nomeArquivo = document.getElementById("nomeArquivo");
    const btnIdentificar = document.getElementById("btnIdentificar");

    mostrarSecao("identificacao");

    if (!inputMat || !nomeArquivo || !btnIdentificar) {
        return;
    }

    inputMat.addEventListener("change", () => {
        const arquivo = inputMat.files && inputMat.files[0];

        if (arquivo) {
            nomeArquivo.textContent = arquivo.name;
            btnIdentificar.disabled = false;
            return;
        }

        nomeArquivo.textContent = "Nenhum arquivo selecionado";
        btnIdentificar.disabled = true;
    });
});
