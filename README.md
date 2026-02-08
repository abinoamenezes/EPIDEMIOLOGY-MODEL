# 📌 Modelo Epidemiológico SLITR para Tuberculose

Este repositório apresenta a implementação de um modelo epidemiológico compartimental SLITR aplicado ao estudo da dinâmica da tuberculose, considerando os estados de suscetíveis, infecção latente, infecção ativa, tratamento e recuperação.

# 🎯 Objetivo

Analisar a evolução temporal da tuberculose em uma população e avaliar o impacto de diferentes estratégias de intervenção, com ênfase no papel da infecção latente na manutenção do estado endêmico.

# 📊 Modelo

O modelo divide a população em cinco compartimentos:
S (suscetíveis), L (latentes), I (ativos), T (tratamento) e R (recuperados), incorporando latência, reativação, tratamento e reinfecção parcial.

# 🎛️ Cenários simulados

Cenário Base
Diagnóstico Precoce
Redução da Reativação da Infecção Latente

# 🛠️ Implementação: 

O modelo foi implementado em Python, utilizando as bibliotecas NumPy, SciPy e Matplotlib para simulação numérica e visualização dos resultados.

# ▶️ Como executar:

1. Clone o repostiório:

```https://github.com/abinoamenezes/EPIDEMIOLOGY-MODEL.git```
 
2. Acesse o diretório do projeto:

```cd EPIDEMIOLOGY-MODEL```

3. Instale as dependências:

```pip install -r requirements.txt```

4. Execute o cenário base:

```python simulate.py```
   
5. Execute o cenário de diagnóstico precoce:

```python simulate.py --delta 0.03```

 6. Execute o cenário de redução da reativação da infecção latente:
    
```python simulate.py --sigma 0.0002```

# 📄 Link artigo

```https://drive.google.com/file/d/1v6CIvrTozDmDddbWCngjHWdfX3IUJNjo/view?usp=sharing```




   

