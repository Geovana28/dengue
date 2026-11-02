# 🔬 Plataforma de Inteligência Epidemiológica & Climática para Dengue no Brasil

[![Live Interactive Showcase](https://img.shields.io/badge/Live_Showcase-GitHub_Pages-f43f5e?style=for-the-badge&logo=googlechrome&logoColor=white)](https://geovana28.github.io/dengue/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Open In Colab](https://img.shields.io/badge/Open_in_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/Geovana28/dengue/blob/main/dengue_analysis_eda.ipynb)
[![Licença MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> 💡 **Experimente a Demonstração Interativa:** Acesse o [**Interactive Showcase (GitHub Pages)**](https://geovana28.github.io/dengue/) para simular em tempo real as defasagens de chuva (Time-Lag $\tau$) e o alinhamento de pico de arboviroses diretamente no navegador.

---

## 💡 Motivação do Projeto & Decisões Técnicas

A dengue é um desafio de saúde pública recorrente no Brasil, mas os modelos tradicionais frequentemente analisam contaminações sem considerar a **defasagem biológica** entre os eventos climáticos e o ciclo de reprodução do mosquito *Aedes aegypti*.

### Decisões de Engenharia:
1. **Por que defasagem temporal (Lag de 1 a 6 semanas)?**
   O acúmulo de chuvas não gera casos imediatos; existe um intervalo biológico de 7 a 21 dias (eclosão de ovos, desenvolvimento larval, picada e período de incubação viral no hospedeiro humano). O modelo implementa correlação cruzada de Spearman para capturar o ponto ótimo dessa defasagem.
2. **Por que InfoDengue + Open-Meteo?**
   Combinamos as notificações epidemiológicas oficiais consolidadas pela Fiocruz/FGV com a API histórica do Open-Meteo, permitindo reprodutibilidade pública sem custos de chave de API proprietária.
3. **Controle de Ruído com EWMA:**
   Séries semanais de notificação sofrem com represamento em finais de semana e feriados. A aplicação de média móvel exponencialmente ponderada (EWMA) atenua esse ruído sem perder a velocidade de detecção de tendências de alta.

---

## 📌 Resumo Técnico

Pipeline automatizado de análise e vigilância epidemiológica cruzando histórico de notificações com variáveis meteorológicas nas capitais brasileiras, incluindo mapas espaciais e scoring de risco.

---

## 🔬 Formulações Matemáticas

### Taxa de Incidência por 100.000 Habitantes

$$\text{Taxa de Incidência}_i = \left( \frac{\text{Casos Estimados}_i}{\text{População IBGE}_i} \right) \times 100.000$$

### Correlação Cruzada de Spearman com Lag Temporal ($\tau$)

$$r_s(\tau) = 1 - \frac{6 \sum (R(X_{t-\tau}) - R(Y_t))^2}{n(n^2 - 1)}$$

### Índice de Risco Epidemiológico Combinado ($0 \le \text{IR} \le 100$)

$$\text{IR} = \min\left(100, \; 0.5 \cdot S_{\text{Incidência}} + 0.3 \cdot S_{\text{EWMA}} + 0.2 \cdot S_{\text{ChuvaLag2s}}\right)$$

### Nowcasting Bayesiano para Correção do Triângulo de Atraso de Notificação

$$\mathbb{E}[Y_t \mid y_t^{\text{obs}}] = \frac{y_t^{\text{obs}}}{P(\text{Notificado até } t)}$$

Onde $P(\text{Notificado})$ é calibrado empiricamente contra o histórico de atraso de inserção do SINAN, gerando intervalos de credibilidade de 95% para os casos reais da semana epidemiológica corrente.

### Avaliação de Cenário Contrafactual de Intervenção

$$\Delta_{\text{Casos Evitados}} = \sum_{t \ge t_0} \left( Y_t^{\text{observado}} - Y_t^{\text{cenário}} \right)$$

Simula parametricamente a redução esperada na curva epidêmica sob a hipótese de antecipação de campanhas de controle vetorial em 2 a 4 semanas.

### Backtesting Retrospectivo do Nowcasting (`evaluate_nowcasting_backtest`)
Avalia o erro absoluto médio (**MAE**) e a raiz do erro quadrático médio (**RMSE**) comparando as notificações brutas incompletas em cada corte temporal passado com a estimativa corrigida pelo modelo de atraso de digitação.

---

## ⚠️ Limitações Metodológicas e Epidemiológicas

1. **Atraso de Digitação vs. Subnotificação Estrutural**: O método de *Nowcasting* corrige o **atraso de registro administrativo** no SINAN (casos atendidos que demoram de 1 a 4 semanas para serem digitados), mas não estima casos assintomáticos ou pacientes que não procuraram atendimento médico.
2. **Associação Temporal $\neq$ Causalidade**: As correlações cruzadas de Spearman com defasagem de 2 a 4 semanas demonstram acoplamento temporal compatível com o ciclo de vida do *Aedes aegypti*, mas não substituem modelos mecanísticos entomológicos nem identificação causal formal.
3. **Granularidade Municipal**: Os indicadores agregados por capital não capturam heterogeneidades intraurbanas (bairros ou setores censitários com diferentes condições de saneamento).

---

## 💻 Dashboard Interativo (5 Módulos)

| Módulo | Descrição |
|--------|-----------|
| 📈 **Tendências & Visão Geral** | Série temporal, comparação entre capitais, distribuição de alertas |
| 🗺️ **Mapa Espacial** | Mapa geográfico colorido por status de alerta e dimensionado por incidência |
| 🌡️ **Correlações Climáticas** | Matriz de lag interativa (0-6 semanas) demonstrando atrasos de incubação |
| 🔮 **Previsão de Surtos** | Suavização EWMA de 4 semanas + projeção de curto prazo de 6 semanas |
| 📑 **Paper Acadêmico & Export** | Resumo técnico, exportação de dados (CSV/JSON) e citação BibTeX |

---

## 📂 Estrutura do Projeto

```text
dengue/
├── main.py                    # Pipeline de Dados (ETL, Lag, Scoring de Risco)
├── app.py                     # Aplicação Web Streamlit (5 Módulos Analíticos)
├── create_notebook.py         # Gerador Automatizado de Notebook EDA
├── dengue_analysis_eda.ipynb  # Notebook de Análise Exploratória
├── dengue_processed_data.csv  # Dataset Consolidado (2023 - Presente)
├── style.css                  # Estilização do Dashboard
├── requirements.txt           # Dependências Python com versões fixas
├── tests/
│   └── test_pipeline.py       # Suite de Testes Automatizados PyTest
├── .github/
│   └── workflows/
│       └── data_pipeline.yml  # Workflow CI/CD Semanal Automatizado
└── docs/
    └── data_dictionary.md     # Dicionário de Dados & Métricas Epidemiológicas
```

---

## 🧪 Testes Automatizados

```bash
python -m pytest tests/ -v
```

| Teste | Descrição |
|-------|-----------|
| `test_city_metadata_integrity` | Valida geocódigos IBGE, populações e coordenadas das 27 capitais |
| `test_incidence_rate_calculation` | Testa precisão matemática das taxas normalizadas por população |
| `test_compute_climate_lags` | Verifica lógica de deslocamento temporal para 1-6 semanas de lag |
| `test_calculate_combined_risk_index` | Confirma que scores de risco estão em $[0, 100]$ |
| `test_cross_correlations` | Valida formato da matriz de correlação Pearson/Spearman |

---

## 🚀 Como Executar

### 1. Instalação
```bash
git clone https://github.com/Geovana28/dengue.git
cd dengue
pip install -r requirements.txt
```

### 2. Rodar Pipeline de Dados
```bash
python main.py
```

### 3. Lançar Dashboard
```bash
streamlit run app.py
```
Acesse: `http://localhost:8505`

---

## 🎓 Citação (BibTeX)

```bibtex
@misc{dengue_surveillance_2026,
  title   = {Plataforma de Inteligência Epidemiológica e Climática para Dengue no Brasil},
  author  = {Geovana Luiza Morais Moreira},
  year    = {2026},
  url     = {https://github.com/Geovana28/dengue}
}
```

---

## ⚖️ Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.
