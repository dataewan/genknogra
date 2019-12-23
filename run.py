from genknogra.entitylinking import get_data, processwiki
import click


@click.group()
def cli():
    pass


@click.command(
    help="Download files from wikimedia. URL specifies a JSON config file describing the dump."
)
@click.argument("url")
def download(url):
    get_data.main(url)


@click.command(help="Create test dataset to experiment on")
def testset():
    processwiki.create_test_set()

@click.command(help="Get links and sentences, output to parquet")
def parquet():
    processwiki.create_parquet()


cli.add_command(download)
cli.add_command(testset)
cli.add_command(parquet)

if __name__ == "__main__":
    cli()
