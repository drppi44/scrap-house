import sqlalchemy.orm
sqlalchemy.orm.ScopedSession = sqlalchemy.orm.scoped_session

from elixir import metadata, using_options, Entity, Field, Unicode
from db_conf import user, password, host, database, port


metadata.bind = "mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)
print "mysql://{0}:{1}@{2}:{3}/{4}?client_encoding='utf-8'".format(user, password, host, port, database)
metadata.bind.echo = True


class Idealista(Entity):
    using_options(tablename='idealista')

    type = Field(Unicode(50),)
