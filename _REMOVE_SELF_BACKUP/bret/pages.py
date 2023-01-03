from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    form_model = 'player'
    form_fields = ['accept_conditions']

    # only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1

    # variables for use in template
    def vars_for_template(self):
        return {
            'num_rows':             C.NUM_ROWS,
            'num_cols':             C.NUM_COLS,
            'num_boxes':            C.NUM_ROWS * C.NUM_COLS,
            'num_nobomb':           C.NUM_ROWS * C.NUM_COLS - 1,
            'box_value':            C.BOX_VALUE,
            'time_interval':        C.TIME_INTERVAL,
            'box_value_eur':        C.BOX_VALUE_EUR
        }


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form fields on player level
    form_model = 'player'
    form_fields = [
        'bomb',
        'boxes_collected',
        'bomb_row',
        'bomb_col',
    ]

    # jsonify BRET settings for Javascript application
    def vars_for_template(self):
        reset = self.participant.vars.get('reset',False)
        if reset == True:
           del self.participant.vars['reset']

        input = not C.DEVILS_GAME if not C.DYNAMIC else False

        otree_vars = {
            'reset':         reset,
            'input':         input,
            'random':        C.RANDOM,
            'dynamic':       C.DYNAMIC,
            'num_rows':      C.NUM_ROWS,
            'num_cols':      C.NUM_COLS,
            'feedback':      C.FEEDBACK,
            'undoable':      C.UNDOABLE,
            'box_width':     C.BOX_WIDTH,
            'box_height':    C.BOX_HEIGHT,
            'time_interval': C.TIME_INTERVAL,
        }

        return {'otree_vars': safe_json(otree_vars)}

    def before_next_page(self):
        self.participant.vars['reset'] = True
        self.player.set_payoff()

# ******************************************************************************************************************** #
# *** CLASS RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # only display results after all rounds have been played
    def is_displayed(self):
        return self.subsession.round_number == C.NUM_ROUNDS

    # variables for use in template
    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.player.in_all_rounds()])
        self.participant.vars['bret_payoff'] = total_payoff

        return {
            'player_in_all_rounds':   self.player.in_all_rounds(),
            'box_value':              C.BOX_VALUE,
            'boxes_total':            C.NUM_ROWS * C.NUM_COLS,
            'boxes_collected':        self.player.boxes_collected,
            'bomb':                   self.player.bomb,
            'bomb_row':               self.player.bomb_row,
            'bomb_col':               self.player.bomb_col,
            'round_result':           self.player.round_result,
            'round_to_pay':           self.participant.vars['round_to_pay'],
            'payoff':                 self.player.payoff_for_results,
            'total_payoff':           total_payoff,
            'payoff_eur':             self.player.payoff_for_results_eur
        }

# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision]

if C.INSTRUCTIONS == True:
    page_sequence.insert(0,Instructions)

if C.RESULTS == True:
    page_sequence.append(Results)
