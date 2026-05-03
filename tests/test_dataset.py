from backend.utils.data_loader import carregar_mat


def test_carrega_dataset_real_grupo6():
    dados = carregar_mat("datasets/Dataset_Grupo6_c213.mat")

    print(f"t: shape={dados['t'].shape}, range=[{dados['t'][0]:.1f}, {dados['t'][-1]:.1f}]")
    print(f"y: shape={dados['y'].shape}, range=[{dados['y'][0]:.2f}, {dados['y'][-1]:.2f}]")
    print(f"u: shape={dados['u'].shape}")
    print(f"Unidade tempo: {dados['unidade_t']}")
    print(f"Grandeza saida: {dados['grandeza_y']} [{dados['unidade_y']}]")

    assert "t" in dados
    assert "y" in dados
    assert "u" in dados

    assert len(dados["t"]) > 0
    assert len(dados["y"]) > 0
    assert len(dados["u"]) > 0

    assert len(dados["t"]) == len(dados["y"]) == len(dados["u"])
