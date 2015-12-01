from PyIRC.extensions import BaseExtension
from PyIRC.signal import event
from sqlalchemy import Column, Integer, String

from seabird.db import Base

import re


class Karma(Base):
    __tablename__ = 'karma'

    name = Column(String, primary_key=True)
    score = Column(Integer, default=0)


class KarmaPlugin(BaseExtension):
    requires = ['Database']

    regex = re.compile('([^\s]+)(\+\+|--)(?:\s|$)')

    @event('seabird_command', 'karma')
    def karma(self, event, line, cmd, remainder):
        normalized_item = remainder.lower()
        with self.base.db_session() as session:
            score = Karma.score.default.arg

            k = session.query(Karma).get(normalized_item)
            if k:
                score = k.score

            self.reply(line, "%s's karma is %d" % (remainder, score))

    @event('commands', 'PRIVMSG')
    def match_karma(self, event, line):
        trailing = line.params[-1]
        if self.regex.match(trailing):
            basic_rfc = self.base.basic_rfc
            if self.casecmp(line.params[0], basic_rfc.nick):
                self.reply(line, 'Must be used in a channel')
                return

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
