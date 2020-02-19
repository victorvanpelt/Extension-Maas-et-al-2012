from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class TicketNumber(Page):
    form_model = 'player'
    form_fields = ['tn']

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.player.participant.vars['tn'] = self.player.tn

class Information(Page):
    form_model = 'player'
    form_fields = ['accept_info']

    def is_displayed(self):
        return self.round_number == 1

class Instructions_1(Page):
    form_model = 'player'
    form_fields = ['accept_1']

    def is_displayed(self):
        return self.round_number == 1

class Instructions_2(Page):
    form_model = 'player'
    form_fields = ['accept_2']

    def is_displayed(self):
        return self.round_number == 1

class Instructions_3(Page):
    form_model = 'player'
    form_fields = ['accept_3']

    def is_displayed(self):
        return self.round_number == 1

class Instructions_4(Page):
    form_model = 'player'
    form_fields = ['Instr1', 'Instr2', 'Instr3', 'Instr4']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if values["Instr1"] != 1:
            return 'Your first answer is incorrect. The individual investments of the BU managers determine the size of the bonus pool.'
        if values["Instr2"] != 2:
            return 'Your second answer is incorrect. The decisions of the Supervisor do not affect the size of the bonus pool.'
        if values["Instr3"] != 1:
            return 'Your third answer is incorrect. The decisions of the Supervisor affect how the bonus pool is divided between the two BU managers.'
        if values["Instr4"] != 2:
            return 'Your last answer is incorrect. The decisions of the BU managers do not affect the reward of the Supervisor.'

class FirstStageWarn(Page):
    def is_displayed(self):
        return self.round_number == 1

class SecondStageWarnA(Page):
    def is_displayed(self):
        return self.round_number == 5

class SecondStageWarnB(Page):
    def is_displayed(self):
        return self.round_number == 5

class Round_Warn(Page):
    pass

class Manager_A(Page):
    form_model = 'group'
    form_fields = ['effort_a', 'check_effort', 'instructions_MA']

    def error_message(self, value):
        if value["check_effort"] == None:
            return 'Please use the slider to make a decision.'

    def is_displayed(self):
        return self.player.player_role == 1

class Manager_B(Page):
    form_model = 'group'
    form_fields = ['effort_b', 'check_effort', 'instructions_MB']

    def error_message(self, value):
        if value["check_effort"] == None:
            return 'Please use the slider to make a decision.'

    def is_displayed(self):
        return self.player.player_role == 2

class ManagerWait(WaitPage):
    def after_all_players_arrive(self):
         self.group.define_pool()

class Supervisor_1A(Page):
    form_model = 'group'
    form_fields = ['want_info_form', 'instructions_S1A']

    def is_displayed(self):
        if self.player.extension == 0:
            return False
        else:
            if self.player.player_role <3:
                return False
            else:
                return True

    def before_next_page(self):
        self.group.define_want_info()

class Supervisor_1B(Page):
    form_model = 'group'
    form_fields = ['pricepay_r', 'check_pricepay', 'instructions_S1B']

    def error_message(self, value):
        if value["check_pricepay"] == None:
            return 'Please use the slider to make a decision.'

    def is_displayed(self):
        if self.player.extension == 1:
            return False
        if self.player.extension == 0:
             return self.player.player_role ==3

    def before_next_page(self):
        self.group.define_price()
        self.group.define_info()

class Supervisor_1C(Page):
    form_model = 'group'
    form_fields = ['pricepay_e', 'check_pricepay', 'instructions_S1C']

    def error_message(self, value):
        if value["check_pricepay"] == None:
            return 'Please use the slider to make a decision.'

    def is_displayed(self):
        if self.player.extension == 0:
            return False
        else:
            if self.group.want_info == 0:
                return False
            else:
                return self.player.player_role == 3

    def before_next_page(self):
        self.group.define_price()
        self.group.define_info()

class Supervisor_2A(Page):
    form_model = 'group'
    form_fields = ['allocation_b', 'check_allocation']

    def error_message(self, value):
        if value["check_allocation"] == None:
            return 'Please use the slider to make a decision.'

    def is_displayed(self):
        if self.player.extension == 0:
            if self.player.player_role < 3:
                return False
            else:
                return True
        else:
            if self.player.player_role < 3:
                return False
            else:
                if self.group.want_info == 0:
                    return False
                else:
                    return True

class Supervisor_2B(Page):
    form_model = 'group'
    form_fields = ['allocation_b', 'check_allocation']

    def error_message(self, value):
        if value["check_allocation"] == None:
            return 'Please use the slider to make a decision.'

    def is_displayed(self):
        if self.player.extension ==0:
            return False
        else:
            if self.player.player_role < 3:
                return False
            else:
                if self.group.want_info == 1:
                    return False
                else:
                    return True

class AllWait(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        for p in self.group.get_players():
            p.set_final_payoff()

class Results(Page):
    pass

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number != Constants.num_rounds

class FinishPage(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'round_to_pay': self.participant.vars['round_to_pay'],
            'payoff_lira': self.participant.vars['payoff_lira'],
            'payoff_eur': self.participant.vars['payoff_eur']
        }

page_sequence = [
    TicketNumber,
    Information,
    Instructions_1,
    Instructions_2,
    Instructions_3,
    Instructions_4,
    FirstStageWarn,
    SecondStageWarnA,
    SecondStageWarnB,
    Round_Warn,
    Manager_A,
    Manager_B,
    ManagerWait,
    Supervisor_1A,
    Supervisor_1B,
    Supervisor_1C,
    Supervisor_2A,
    Supervisor_2B,
    AllWait,
    Results,
    ShuffleWaitPage,
    FinishPage
]
