"""
Author:     David Walshe
Date:       28 June 2020
"""

import sqlalchemy as db

if __name__ == '__main__':
    import sqlalchemy as db

    engine = db.create_engine('sqlite:///../../db/red_alert_data.db')
    connection = engine.connect()

    metadata = db.MetaData()

    emp = db.Table('emp', metadata,
                   db.Column('Id', db.Integer()),
                   db.Column('name', db.String(255), nullable=False),
                   db.Column('salary', db.Float(), default=100.0),
                   db.Column('active', db.Boolean(), default=True)
                   )

    metadata.create_all(engine)  # Creates the table