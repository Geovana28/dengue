# 🔬 Plataforma de Inteligência Epidemiológica & Climática para Dengue no Brasil

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PyTest](https://img.shields.io/badge/PyTest-100%25%20Passed-brightgreen?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/Geovana28/dengue/actions)
[![Licença MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Resumo Técnico

Sistema de **vigilância epidemiológica preditiva** e plataforma de inteligência climática interativa para rastreamento de **dinâmicas de transmissão de Dengue, hotspots espaciais de risco e correlação com defasagem meteorológica** nas 27 capitais brasileiras.

### Destaques Científicos

- 🔄 **Fusão Multi-Fonte:** Pipeline automatizado integrando dados epidemiológicos do **InfoDengue (Fiocruz & FGV)** com variáveis meteorológicas históricas do **Open-Meteo Archive API**
- 🦟 **Análise de Lag Entomológico:** Modelagem de correlação cruzada avaliando defasagens temporais ($\tau \in [1, 6]$ semanas) entre precipitação e transmissão viral
- 📊 **Índice de Risco Combinado:** Scoring multivariável combinando incidência instantânea, momentum EWMA e precipitação com lag de 2 semanas
- ✅ **100% de cobertura de testes** com `pytest`

---

## 🔬 Formulações Matemáticas

### Taxa de Incidência por 100.000 Habitantes

$$\text{Taxa de Incidência}_i = \left( \frac{\text{Casos Estimados}_i}{\text{População IBGE}_i} \right) \times 100.000$$

### Correlação Cruzada de Spearman com Lag Temporal ($\tau$)

$$r_s(\tau) = 1 - \frac{6 \sum (R(X_{t-\tau}) - R(Y_t))^2}{n(n^2 - 1)}$$

### Índice de Risco Epidemiológico Combinado ($0 \le \text{IR} \le 100$)

$$\text{IR} = \min\left(100, \; 0.5 \cdot S_{\text{Incidência}} + 0.3 \cdot S_{\text{EWMA}} + 0.2 \cdot S_{\text{ChuvaLag2s}}\right)$$

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
