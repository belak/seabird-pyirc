from PyIRC.extensions import BaseExtension
from PyIRC.signal import event
from sqlalchemy import Column, Integer, String

from .db import Base

import re

class Karma(Base):
    __tablename__ = 'karma'

    name = Column(String, primary_key=True)
    score = Column(Integer, default=0)


class KarmaPlugin(BaseExtension):
    regex = re.compile('([^\s]+)(\+\+|--)(?:\s|$)')

    @event('commands', 'PRIVMSG')
    def match_karma(self, event, line):
        trailing = line.params[-1]
        with self.base.db_session() as session:
            for (item, operation) in self.regex.findall(trailing):
                normalized_item = item.lower()

                k, _ = session.get_or_create(Karma, name=normalized_item)

                # Figure out if we need to add or subtract
                diff = -1
                if operation == '++':
                    diff = 1

                # Update the model
                k.score = Karma.score + diff
                session.add(k)
                session.flush()

                k = session.query(Karma).get(normalized_item)
                self.reply(line, "%s's karma is now %d" % (item, k.score))
