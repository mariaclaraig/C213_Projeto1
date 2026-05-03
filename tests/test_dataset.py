from backend.utils.data_loader import carregar_mat


def test_carrega_dataset_real_grupo6():
    dados = carregar_mat("datasets/Dataset_Grupo6_c213.mat")

    assert "t" in dados
    assert "y" in dados
    assert "u" in dados

    assert len(dados["t"]) > 0
    assert len(dados["y"]) > 0
    assert len(dados["u"]) > 0

    assert len(dados["t"]) == len(dados["y"]) == len(dados["u"])
