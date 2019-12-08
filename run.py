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


@click.command(help="Process downloaded wikipedia files")
def process():
    processwiki.main()


cli.add_command(download)
cli.add_command(process)

if __name__ == "__main__":
    cli()
