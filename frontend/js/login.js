const loginForm = document.getElementById("loginForm");
const loginCard = document.getElementById("loginCard");
const usuarioInput = document.getElementById("usuario");
const senhaInput = document.getElementById("senha");
const errorMsg = document.getElementById("errorMsg");
const loginButton = document.getElementById("loginButton");

const CREDENCIAIS = {
    usuario: "grupo6",
    senha: "c213",
};

const CHAVE_AUTENTICACAO = "c213_login_ok";

window.addEventListener("load", () => {
    sessionStorage.removeItem(CHAVE_AUTENTICACAO);
    usuarioInput.focus();
});

loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const usuario = usuarioInput.value.trim();
    const senha = senhaInput.value.trim();

    if (usuario === CREDENCIAIS.usuario && senha === CREDENCIAIS.senha) {
        errorMsg.textContent = "";
        loginButton.disabled = true;
        loginButton.querySelector("span").textContent = "Entrando...";
        sessionStorage.setItem(CHAVE_AUTENTICACAO, "true");
        loginCard.classList.add("is-leaving");

        window.setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 400);

        return;
    }

    errorMsg.textContent = "Usuário ou senha incorretos.";
    senhaInput.value = "";
    senhaInput.focus();
});
