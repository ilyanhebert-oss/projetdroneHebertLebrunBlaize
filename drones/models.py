from django.db import models


class Utilisateur(models.Model):
    ROLE_CHOICES = [
        ('operateur', 'Opérateur drone'),
        ('superviseur', 'Superviseur logistique'),
        ('planificateur', 'Planificateur'),
        ('administrateur', 'Administrateur'),
    ]

    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.nom} ({self.role})"


class Drone(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_vol', 'En vol'),
        ('maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
    ]

    identifiant = models.CharField(max_length=50, unique=True)
    modele = models.CharField(max_length=100)
    niveau_batterie = models.FloatField(help_text="Niveau de batterie en pourcentage (0-100)")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')

    def __str__(self):
        return f"{self.identifiant} - {self.modele} ({self.statut})"


class Mission(models.Model):
    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    date_heure = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiee')
    trajectoire = models.TextField(blank=True)
    drone = models.ForeignKey(Drone, on_delete=models.PROTECT, related_name='missions')
    operateur = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT,
        related_name='missions_operateur',
        limit_choices_to={'role': 'operateur'}
    )
    planificateur = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT,
        related_name='missions_planificateur',
        limit_choices_to={'role': 'planificateur'},
        null=True, blank=True
    )

    def __str__(self):
        return f"Mission #{self.pk} - {self.drone} ({self.statut})"


class Alerte(models.Model):
    TYPE_CHOICES = [
        ('batterie', 'Batterie faible'),
        ('obstacle', 'Obstacle détecté'),
        ('deviation', 'Déviation de trajectoire'),
        ('connexion', 'Perte de connexion'),
        ('autre', 'Autre anomalie'),
    ]
    STATUT_CHOICES = [
        ('nouvelle', 'Nouvelle'),
        ('en_traitement', 'En traitement'),
        ('resolue', 'Résolue'),
    ]

    type_anomalie = models.CharField(max_length=30, choices=TYPE_CHOICES)
    horodatage = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='nouvelle')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='alertes')

    def __str__(self):
        return f"Alerte {self.type_anomalie} - Mission #{self.mission.pk}"


class RapportAudit(models.Model):
    date_rapport = models.DateTimeField(auto_now_add=True)
    mission = models.OneToOneField(Mission, on_delete=models.PROTECT, related_name='rapport')
    superviseur = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT,
        related_name='rapports',
        limit_choices_to={'role': 'superviseur'}
    )

    def __str__(self):
        return f"Rapport #{self.pk} - Mission #{self.mission.pk}"


class EcartInventaire(models.Model):
    zone = models.CharField(max_length=100)
    description = models.TextField()
    rapport = models.ForeignKey(RapportAudit, on_delete=models.CASCADE, related_name='ecarts')

    def __str__(self):
        return f"Écart zone {self.zone} - Rapport #{self.rapport.pk}"
