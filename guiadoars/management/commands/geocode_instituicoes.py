from django.core.management.base import BaseCommand
from guiadoars.models import Instituicao
from guiadoars.utils import geocode_endereco

class Command(BaseCommand):
    help = 'Geocodifica instituições que não possuem latitude/longitude'

    def handle(self, *args, **options):
        instituicoes = Instituicao.objects.filter(latitude__isnull=True, longitude__isnull=True)
        self.stdout.write(f"Encontradas {instituicoes.count()} instituições sem coordenadas.")

        for inst in instituicoes:
            endereco = f"{inst.endereco}, {inst.cidade}, {inst.estado}, {inst.cep}".strip(", ")
            self.stdout.write(f"Geocodificando: {inst.nome} - {endereco}")
            lat, lng = geocode_endereco(endereco)
            if lat and lng:
                inst.latitude = lat
                inst.longitude = lng
                inst.save()
                self.stdout.write(self.style.SUCCESS(f"  -> OK: {lat}, {lng}"))
            else:
                self.stdout.write(self.style.WARNING(f"  -> Falha: não foi possível obter coordenadas"))