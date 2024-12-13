from rest_framework import serializers

from dashboard_user.models import CustomUser
from dashboard_app.models import AccountAccount, AccountAnalyticGroup, PrevisionCost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid',
            'email',
        ]
        read_only_fields = ('uuid', 'email',)


class AccountAnalyticGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAnalyticGroup
        fields = [
            'uuid',
            'name',
            'id_odoo',
        ]

class AccountAnalyticGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAnalyticGroup
        fields = [
            'uuid',
            'name',
            'id_odoo',
        ]



class PrevisionCostSerializer(serializers.Serializer):
    # amount = serializers.DecimalField()
    # titled = serializers.DecimalField()


    def dictionary_with_prevision_cost(self):
        prevision_costs = PrevisionCost.objects.filter(type__type='CAR')
        titled = prevision_costs.titled
        amount = prevision_costs.amount
        bienveillance_prev = {
            "slug": "recap_recettes",
            "titre": "",
            "colonnes": [
                {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés
                {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants
            ],
            "lignes": [titled,amount],
            "total":True
        }
        return


