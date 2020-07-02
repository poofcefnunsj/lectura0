import click
from flask.cli import with_appcontext

from aplicacion.extensions import db
from aplicacion.models import Usuario, Comentario

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    
if __name__=='__main__':
    create_tables()
