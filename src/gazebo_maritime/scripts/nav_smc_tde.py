import numpy as np

class USVController:
    def __init__(self, M_nominal, gain_K, surface_lambda):
        self.M_hat = M_nominal  # Masse nominale de l'USV
        self.K = gain_K         # Gain de robustesse SMC
        self.lam = surface_lambda # Pente de la surface de glissement
        
        # Mémoire pour TDE
        self.u_prev = 0.0
        self.acc_prev = 0.0
        self.dt = 0.1 # Pas de temps

    def compute_control(self, error, error_dot, acc_measured):
        # 1. Estimation TDE (Estimation de la dynamique inconnue)
        # On estime l'ensemble des perturbations 'F'
        f_hat = self.acc_prev - (1/self.M_hat) * self.u_prev
        
        # 2. Définition de la surface de glissement (s = e_dot + lambda * e)
        s = error_dot + self.lam * error
        
        # 3. Loi de commande SMC + TDE
        # On utilise le signe de 's' pour la robustesse
        u_smc = -self.K * np.tanh(s) # tanh pour limiter le broutement (chattering)
        
        # Commande totale : Compensation TDE + Dynamique désirée + SMC
        # u = M_hat * (acc_des - f_hat - lambda * e_dot) + u_smc
        u = self.M_hat * (-f_hat - self.lam * error_dot) + u_smc
        
        # Mise à jour pour le prochain pas
        self.u_prev = u
        self.acc_prev = acc_measured
        
        return u
