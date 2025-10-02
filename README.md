# Binance Bot Futuros Testnet

Este é um **bot de trading para Binance Futuros Testnet**, desenvolvido em Python, modular e avançado, capaz de operar simultaneamente até 5 pares de criptomoedas. Ele utiliza estratégias combinadas de indicadores técnicos, trailing stop, filtros de lateralização, gestão de risco e envio de alertas via Telegram.

---

## **📌 Funcionalidades**

1. **Operação simultânea**: Até 5 pares de criptomoedas simultaneamente.
2. **Estratégias avançadas**:
   - Médias móveis (MA) com cruzamentos para sinal de compra e venda.
   - RSI (Relative Strength Index) para filtragem de sinais extremos.
   - ATR (Average True Range) para cálculo dinâmico de Stop Loss (SL) e Take Profit (TP).
   - Sinais combinados (multi-indicadores) para maior precisão.
3. **Gestão de risco**:
   - Cálculo de quantidade baseada em percentual de risco do saldo.
   - Limite de perda diário configurável.
   - Stop Loss e Take Profit dinâmicos baseados em ATR.
4. **Trailing Stop**:
   - Ajusta automaticamente o stop para proteger lucros.
5. **Filtragem de lateralização**:
   - Evita abrir trades quando o mercado está sem tendência clara.
6. **Logs e estatísticas**:
   - Registro detalhado de todas as operações.
   - Resumo diário de lucros/prejuízos.
   - Estatísticas por par: número de trades, vitórias e perdas.
7. **Alertas Telegram**:
   - Notificações de ordens executadas, limites atingidos e encerramento do bot.
8. **Backtesting simples**:
   - Teste histórico baseado em MA e RSI para avaliação de performance.

---

## **📁 Estrutura da pasta**
