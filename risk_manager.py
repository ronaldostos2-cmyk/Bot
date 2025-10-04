from config import BASE_RISK_PERCENT, MAX_CONSECUTIVE_LOSSES

class RiskManager:
    """
    Gerenciamento de risco Nível 3:
    - Ajusta tamanho da posição conforme saldo e resultados recentes
    - Pyramiding controlado: aumenta posição em sequência de lucros
    - Cooldown após perdas consecutivas
    """

    def __init__(self):
        self.consecutive_losses = 0
        self.cooldown = False
        self.last_result = 0

    def adjust_position(self, balance):
        """
        Ajusta o valor do trade dinamicamente:
        - Reduz após perdas
        - Aumenta levemente após sequência de lucros
        """
        if self.cooldown:
            return 0

        risk = BASE_RISK_PERCENT

        if self.consecutive_losses > 0:
            risk *= 0.5  # Reduz risco após perda
        elif self.last_result > 0:
            risk *= 1.1  # Pequeno aumento após lucro

        return balance * risk

    def update_results(self, profit_loss):
        """
        Atualiza histórico de perdas/ganhos e controla cooldown
        """
        self.last_result = profit_loss

        if profit_loss > 0:
            self.consecutive_losses = 0
            self.cooldown = False
        else:
            self.consecutive_losses += 1
            if self.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
                self.cooldown = True  # pausa após perdas consecutivas
