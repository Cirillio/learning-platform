from django.core.management.base import BaseCommand
from django.core import serializers
import json

class Command(BaseCommand):
    help = 'Dumps data from all models to a JSON file.'

    def handle(self, *args, **options):
        from django.apps import apps
        all_models = apps.get_models()
        
        data = {}
        for model in all_models:
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            if app_label not in data:
                data[app_label] = {}
            
            queryset = model.objects.all()
            data[app_label][model_name] = json.loads(serializers.serialize('json', queryset))

        with open('db_dump.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        self.stdout.write(self.style.SUCCESS('Successfully dumped data to db_dump.json'))
