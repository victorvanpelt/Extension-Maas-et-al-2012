from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Info_Start(Page):

    form_model = 'player'
    form_fields = ['accept_start']

    def is_displayed(self):
        return self.round_number == 1

class Info_Interactive(Page):

    form_model = 'player'
    form_fields = ['accept_interactive']

    def is_displayed(self):
        return self.round_number == 1

class Instructions_1(Page):

    form_model = 'player'
    form_fields = ['accept_instr1']

    def is_displayed(self):
        return self.round_number == 1

class Instructions_2(Page):

    form_model = 'player'
    form_fields = ['accept_instr2']

    def is_displayed(self):
        return self.round_number == 1

class Instructions_3(Page):

    form_model = 'player'
    form_fields = ['accept_instr3']

    def is_displayed(self):
        return self.round_number == 1

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

class Supervisor_1(Page):
    form_model = 'group'
    form_fields = ['pricepay', 'check_pricepay']

    def error_message(self, value):
        if value["check_pricepay"] == None:
            return 'Please the slider to make a decision.'

    def is_displayed(self):
        return self.player.player_role == 3

    def before_next_page(self):
        self.group.define_info()

class Supervisor_2(Page):
    form_model = 'group'
    form_fields = ['allocation_b', 'check_allocation']

    def error_message(self, value):
        if value["check_allocation"] == None:
            return 'Please the slider to make a decision.'

    def is_displayed(self):
        return self.player.player_role == 3

class AllWait(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):
    # form_model = 'player'
    # form_fields = 'check_results'
    #
    # def error_message(self, value):
    #     if value["check_results"] == None:
    #         return 'Please check the box to continue.'
    pass

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number != Constants.num_rounds

page_sequence = [Info_Start, Info_Interactive, Instructions_1, Instructions_2, Instructions_3, Manager_A, Manager_B, ManagerWait, Supervisor_1, Supervisor_2, AllWait, Results, ShuffleWaitPage]
