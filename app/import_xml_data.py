import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from app.models import MedicalTerm

class Command(BaseCommand):
    help = 'Import medical terms from XML file'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str, help='Path to the XML file')

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for descriptor in root.findall('.//DescriptorRecord'):
            descriptor_ui_elem = descriptor.find('DescriptorUI')
            descriptor_name_elem = descriptor.find('DescriptorName/String')
           # description_elem = descriptor.find('Description')  # Stored but not used for search

            concept_id = descriptor_ui_elem.text if descriptor_ui_elem is not None else None
            preferred_term = descriptor_name_elem.text if descriptor_name_elem is not None else ''
           # description = description_elem.text if description_elem is not None else ''

            if concept_id:
                MedicalTerm.objects.update_or_create(
                    concept_id=concept_id,
                    defaults={
                        'preferred_term': preferred_term,
                       # 'description': description
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported medical terms from XML'))
