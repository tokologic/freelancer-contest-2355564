from django.core.management.base import BaseCommand

from project.scraper.services.property.rcm1 import Rcm1MarketplaceScraper


class Command(BaseCommand):
    help = "Scrape info from property websites."

    # def add_arguments(self, parser):
    # parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        scraper = Rcm1MarketplaceScraper(token="SFh_vpTV6FE6kPQ3K5oDjDISfZcVJLJtiFcKcbENqhk")
        scraper.set_stdout(self.stdout)
        scraper.handle()
