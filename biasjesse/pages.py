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
            return 'Your first answer is incorrect.'
        if values["Instr2"] != 2:
            return 'Your second answer is incorrect.'
        if values["Instr3"] != 1:
            return 'Your third answer is incorrect.'
        if values["Instr4"] != 2:
            return 'Your last answer is incorrect.'

class FirstStageWarn(Page):
    def is_displayed(self):
        return self.round_number == 1

class SecondStageWarnA(Page):
    form_model = 'player'
    form_fields = ['warn_2a']

    def is_displayed(self):
        return self.round_number == 5

class SecondStageWarnB(Page):
    form_model = 'player'
    form_fields = ['warn_2b']

    def is_displayed(self):
        return self.round_number == 5

class Round_Warn(Page):
    pass

class Manager_A(Page):
    form_model = 'group'
    form_fields = ['effort_a', 'check_effort']

    def error_message(self, value):
        if value["check_effort"] == None:
            return 'Please the slider to make a decision.'

    def is_displayed(self):
        return self.player.player_role == 1

class Manager_B(Page):
    form_model = 'group'
    form_fields = ['effort_b', 'check_effort']

    def error_message(self, value):
        if value["check_effort"] == None:
            return 'Please the slider to make a decision.'

    def is_displayed(self):
        return self.player.player_role == 2

class ManagerWait(WaitPage):
    def after_all_players_arrive(self):
         self.group.define_pool()

class Supervisor_1A(Page):
    form_model = 'group'
    form_fields = ['want_info_form']

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
    form_fields = ['pricepay', 'check_pricepay', 'confirm_price']

    def error_message(self, value):
        if value["check_pricepay"] == None:
            return 'Please the slider to make a decision.'

    def is_displayed(self):
        if self.player.extension ==0:
             return self.player.player_role ==3
        else:
             if self.group.want_info == 1:
                 return self.player.player_role == 3

    def before_next_page(self):
        self.group.define_info()

class Supervisor_2A(Page):
    form_model = 'group'
    form_fields = ['allocation_b', 'check_allocation', 'confirm_allocation']

    def error_message(self, value):
        if value["check_allocation"] == None:
            return 'Please the slider to make a decision.'

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
    form_fields = ['allocation_b', 'check_allocation', 'confirm_allocation']

    def error_message(self, value):
        if value["check_allocation"] == None:
            return 'Please the slider to make a decision.'

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
    Supervisor_2A,
    Supervisor_2B,
    AllWait,
    Results,
    ShuffleWaitPage,
    FinishPage
]
