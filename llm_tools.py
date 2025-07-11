import click
import sqlite_utils


@click.command("delete_all_fragments")
def delete_all_fragments():
    """
    Deletes all rows in the fragments table and orphan rows in related tables.
    """
    db_path = "/Users/kosiew/Library/Application Support/io.datasette.llm/logs.db"
    db = sqlite_utils.Database(db_path)

    try:
        # Delete all rows in the fragments table
        with db.conn:
            deleted_count = db["fragments"].delete_where("1=1")
        click.echo(f"Deleted {deleted_count} rows from fragments table.")

        # Delete orphan rows in fragment_aliases table
        db["fragment_aliases"].delete_where(
            "fragment_id NOT IN (SELECT id FROM fragments)"
        )

        # Delete orphan rows in prompt_fragments table
        db["prompt_fragments"].delete_where(
            "fragment_id NOT IN (SELECT id FROM fragments)"
        )

        # Delete orphan rows in system_fragments table
        db["system_fragments"].delete_where(
            "fragment_id NOT IN (SELECT id FROM fragments)"
        )

        click.echo("Successfully deleted all fragments and orphan rows.")
    except Exception as ex:
        msg = f"Error deleting fragments: {ex}"
        raise click.ClickException(msg)


# Add the command to the CLI
@click.group()
def cli():
    pass


cli.add_command(delete_all_fragments)

if __name__ == "__main__":
    cli()
