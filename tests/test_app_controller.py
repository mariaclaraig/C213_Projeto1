from backend.controllers.app_controller import AppController


def test_controller_emite_erro_quando_identifica_sem_dataset():
    controller = AppController()
    erros = []

    controller.erro_ocorrido.connect(erros.append)

    controller.on_identificar()

    assert erros == ["Nenhum dataset carregado."]


def test_controller_sintoniza_chr_sem_frontend():
    controller = AppController()
    resultados = []

    controller._modelo = {
        "k": 2.0,
        "tau": 10.0,
        "theta": 1.0,
    }
    controller.sintonia_pronta.connect(resultados.append)

    controller.on_sintonizar("CHR")

    assert len(resultados) == 1
    assert resultados[0] == controller.get_pid()
    assert set(resultados[0]) == {"Kp", "Ti", "Td"}


def test_controller_emite_erro_quando_simula_sem_pid():
    controller = AppController()
    erros = []

    controller.erro_ocorrido.connect(erros.append)

    controller.on_simular(50)

    assert erros == ["Realize a identificação e sintonia antes de simular."]
