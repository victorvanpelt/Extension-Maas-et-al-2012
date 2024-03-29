# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as cu, currency_range

from . import *
from otree.api import Bot



class PlayerBot(Bot):

    cases = ['always_bomb', 'never_bomb']

    def play_round(self):
        if C.INSTRUCTIONS and self.player.round_number == 1:
            yield (Instructions, {'accept_conditions': True})
        boxes_collected = 50
        yield (
            Decision,
           {
               'bomb_row': 1, 'bomb_col': 1, 'boxes_collected': boxes_collected,
               'bomb': 1 if self.case == 'always_bomb' else 0
           }
        )
        expected_round_result = 0 if self.case == 'always_bomb' else C.BOX_VALUE * boxes_collected
        assert self.player.round_result == expected_round_result
        if C.RESULTS and self.player.round_number == C.NUM_ROUNDS:
            # 1 round is chosen randomly
            assert self.participant.vars['bret_payoff'] == expected_round_result
            yield Results
