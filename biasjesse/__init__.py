import random
import sys

from otree.api import *


author = 'Jesse'
doc = """
Jesse bias
"""


class C(BaseConstants):
    NAME_IN_URL = 'biasjesse'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 8
    E_ENDOWMENT = cu(10)
    M_ENDOWMENT = cu(15)
    PMAX = cu(5.0)
    RETURN_ON_EFFORT = 1.5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    extension = models.IntegerField()
    effort_a = models.IntegerField(min=0, max=10, initial=None, label="", blank=True)
    # effort_a = models.FloatField(
    #     widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=False),
    #     min=0,
    #     initial=None,
    #     max=10,
    #     blank=True
    #     )
    effort_b = models.IntegerField(min=0, max=10, initial=None, label="", blank=True)
    # effort_b = models.FloatField(
    #     widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=False),
    #     min=0,
    #     initial=None,
    #     max=10,
    #     blank=True
    #     )
    check_effort = models.FloatField(blank=True, initial=None)
    total_effort = models.FloatField(blank=True, initial=None)
    allocation_b = models.IntegerField(min=0, max=100, initial=None, label="")
    # allocation_b = models.FloatField(
    #     widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=False),
    #     min=0,
    #     initial=None,
    #     max=100,
    #     )
    check_allocation = models.FloatField(blank=True, initial=None)
    allocation_a = models.FloatField(blank=False, initial=None, min=0, max=100)
    instructions_MA = models.IntegerField(blank=True, initial=0)
    instructions_MB = models.IntegerField(blank=True, initial=0)
    instructions_S1A = models.IntegerField(blank=True, initial=0)
    instructions_S1B = models.IntegerField(blank=True, initial=0)
    instructions_S1C = models.IntegerField(blank=True, initial=0)
    pool = models.FloatField(blank=False, initial=None)
    want_info = models.IntegerField(blank=False, choices=[[1, 'Yes'], [0, 'No']], initial=0)
    want_info_form = models.IntegerField(
        blank=False, choices=[[1, 'Yes'], [0, 'No']], widget=widgets.RadioSelect
    )
    pricepay_r = models.FloatField(min=0, max=5, initial=None, label="", step=0.1)
    # pricepay_r = models.FloatField(
    #     widget=widgets.SliderInput(attrs={'step': '0.1', 'style': 'width:500px'}, show_value=False),
    #     min=0,
    #     initial=None,
    #     max=5,
    #     )
    pricepay_e = models.FloatField(min=0.1, max=5, initial=None, label="", step=0.1)
    # pricepay_e = models.FloatField(
    #     widget=widgets.SliderInput(attrs={'step': '0.1', 'style': 'width:500px'}, show_value=False),
    #     min=0.1,
    #     initial=None,
    #     max=5,
    #     )
    pricepay = models.FloatField()
    check_pricepay = models.FloatField(blank=True, initial=None)
    price_random = models.FloatField(blank=True, initial=None)
    actualpricepay = models.FloatField(initial=0)
    info = models.IntegerField()
    bonus_a = models.FloatField(blank=True, initial=None)
    bonus_b = models.FloatField(blank=True, initial=None)
    payoff_a = models.CurrencyField(blank=True, initial=None)
    payoff_b = models.CurrencyField(blank=True, initial=None)
    payoff_s = models.CurrencyField(blank=True, initial=None)


class Player(BasePlayer):
    player_role = models.IntegerField()
    tn = models.StringField(blank=False)
    accept_info = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_1 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_2 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_3 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    pay_this_round = models.BooleanField()
    round_result = models.CurrencyField()
    extension = models.IntegerField()
    Instr1 = models.IntegerField(
        blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect
    )
    Instr2 = models.IntegerField(
        blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect
    )
    Instr3 = models.IntegerField(
        blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect
    )
    Instr4 = models.IntegerField(
        blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect
    )
    round_start = models.BooleanField(blank=False, widget=widgets.CheckboxInput)


# FUNCTIONS
def creating_session(subsession: Subsession):
    # Random matching but fixed id in groups
    subsession.group_randomly(fixed_id_in_group=True)
    for p in subsession.get_players():
        p.participant.vars['extension'] = subsession.session.config['extension']
    # in round one, they get a role 1 or 2
    if subsession.round_number == 1:
        for g in subsession.get_groups():
            p1 = g.get_player_by_id(1)
            p1.participant.vars['role'] = 1
            p1.participant.vars['manager'] = 1
            p1.participant.vars['supervisor'] = 0
            p2 = g.get_player_by_id(2)
            p2.participant.vars['role'] = 2
            p2.participant.vars['manager'] = 1
            p2.participant.vars['supervisor'] = 0
            p3 = g.get_player_by_id(3)
            p3.participant.vars['role'] = 3
            p3.participant.vars['supervisor'] = 1
            p3.participant.vars['manager'] = 0
    # in round 5, roles are randomly switched
    elif subsession.round_number == 5:
        role_random = random.randint(1, 2)
        for g in subsession.get_groups():
            if role_random == 1:
                p1 = g.get_player_by_id(1)
                p1.participant.vars['role'] = 3
                p1.participant.vars['supervisor'] = 1
                p2 = g.get_player_by_id(2)
                p2.participant.vars['role'] = 2
                p2.participant.vars['manager'] = 1
                p3 = g.get_player_by_id(3)
                p3.participant.vars['role'] = 1
                p3.participant.vars['manager'] = 1
            else:
                p1 = g.get_player_by_id(1)
                p1.participant.vars['role'] = 1
                p1.participant.vars['manager'] = 1
                p2 = g.get_player_by_id(2)
                p2.participant.vars['role'] = 3
                p2.participant.vars['supervisor'] = 1
                p3 = g.get_player_by_id(3)
                p3.participant.vars['role'] = 2
                p3.participant.vars['manager'] = 1
    else:
        pass
    # Give people their roles and the condition
    for p in subsession.get_players():
        p.player_role = p.participant.vars['role']
        p.define_condition_player()
    # Give group condition
    for g in subsession.get_groups():
        g.extension = subsession.session.config['extension']


def define_pool(group: Group):
    group.total_effort = group.effort_a + group.effort_b
    group.pool = round(group.total_effort * float(C.RETURN_ON_EFFORT), 2)


def define_want_info(group: Group):
    group.want_info = group.want_info_form


def define_price(group: Group):
    if group.extension == 1:
        group.pricepay = group.pricepay_e
    elif group.extension == 0:
        group.pricepay = group.pricepay_r


def define_info(group: Group):
    rn = random.uniform(0, 5)
    while rn == 0 or rn == 5:
        rn = random.uniform(0, 5)
    group.price_random = rn
    if group.pricepay >= group.price_random:
        group.info = 1
        group.actualpricepay = round(group.price_random, 2)
    else:
        group.info = 0
        group.actualpricepay = 0


def set_payoffs(group: Group):
    group.allocation_a = 100 - group.allocation_b
    group.bonus_a = round(group.pool * (group.allocation_a / 100), 2)
    group.bonus_b = round(group.pool * (group.allocation_b / 100), 2)
    group.payoff_a = C.E_ENDOWMENT - cu(group.effort_a) + cu(group.bonus_a)
    group.payoff_b = C.E_ENDOWMENT - cu(group.effort_b) + cu(group.bonus_b)
    group.payoff_s = C.M_ENDOWMENT - cu(group.actualpricepay)
    for p in group.get_players():
        if p.player_role == 1:
            p.round_result = group.payoff_a
        elif p.player_role == 2:
            p.round_result = group.payoff_b
        else:
            p.round_result = group.payoff_s


def define_condition_player(player: Player):
    player.extension = player.participant.vars.get('extension')


def set_final_payoff(player: Player):
    if player.subsession.round_number == 1:
        player.participant.vars['round_to_pay'] = random.randint(1, C.NUM_ROUNDS)
    if player.subsession.round_number == player.participant.vars['round_to_pay']:
        player.pay_this_round = True
        player.payoff = player.round_result
        player.participant.vars['payoff_lira'] = player.round_result
        player.participant.vars['payoff_eur'] = player.round_result.to_real_world_currency(
            player.session
        )
    else:
        player.pay_this_round = False
        player.payoff = cu(0)


# PAGES
class TicketNumber(Page):
    form_model = 'player'
    form_fields = ['tn']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['tn'] = player.tn


class Information(Page):
    form_model = 'player'
    form_fields = ['accept_info']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions_1(Page):
    form_model = 'player'
    form_fields = ['accept_1']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions_2(Page):
    form_model = 'player'
    form_fields = ['accept_2']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions_3(Page):
    form_model = 'player'
    form_fields = ['accept_3']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions_4(Page):
    form_model = 'player'
    form_fields = ['Instr1', 'Instr2', 'Instr3', 'Instr4']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if values["Instr1"] != 1:
            return 'Your first answer is incorrect. The individual investments of the BU managers determine the size of the bonus pool.'
        if values["Instr2"] != 2:
            return 'Your second answer is incorrect. The decisions of the Supervisor do not affect the size of the bonus pool.'
        if values["Instr3"] != 1:
            return 'Your third answer is incorrect. The decisions of the Supervisor affect how the bonus pool is divided between the two BU managers.'
        if values["Instr4"] != 2:
            return 'Your last answer is incorrect. The decisions of the BU managers do not affect the reward of the Supervisor.'


class FirstStageWarn(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class SecondStageWarnA(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 5


class SecondStageWarnB(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 5


class Round_Warn(Page):
    pass


class Manager_A(Page):
    form_model = 'group'
    form_fields = ['effort_a', 'check_effort', 'instructions_MA']

    @staticmethod
    def error_message(player: Player, value):
        if value["check_effort"] == None:
            return 'Please use the slider to make a decision.'

    @staticmethod
    def is_displayed(player: Player):
        return player.player_role == 1


class Manager_B(Page):
    form_model = 'group'
    form_fields = ['effort_b', 'check_effort', 'instructions_MB']

    @staticmethod
    def error_message(player: Player, value):
        if value["check_effort"] == None:
            return 'Please use the slider to make a decision.'

    @staticmethod
    def is_displayed(player: Player):
        return player.player_role == 2


class ManagerWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        define_pool(group)


class Supervisor_1A(Page):
    form_model = 'group'
    form_fields = ['want_info_form', 'instructions_S1A']

    @staticmethod
    def is_displayed(player: Player):
        if player.extension == 0:
            return False
        else:
            if player.player_role < 3:
                return False
            else:
                return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        define_want_info(player.group)


class Supervisor_1B(Page):
    form_model = 'group'
    form_fields = ['pricepay_r', 'check_pricepay', 'instructions_S1B']

    @staticmethod
    def error_message(player: Player, value):
        if value["check_pricepay"] == None:
            return 'Please use the slider to make a decision.'

    @staticmethod
    def is_displayed(player: Player):
        if player.extension == 1:
            return False
        if player.extension == 0:
            return player.player_role == 3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        define_price(player.group)
        define_info(player.group)


class Supervisor_1C(Page):
    form_model = 'group'
    form_fields = ['pricepay_e', 'check_pricepay', 'instructions_S1C']

    @staticmethod
    def error_message(player: Player, value):
        if value["check_pricepay"] == None:
            return 'Please use the slider to make a decision.'

    @staticmethod
    def is_displayed(player: Player):
        if player.extension == 0:
            return False
        else:
            if player.group.want_info == 0:
                return False
            else:
                return player.player_role == 3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        define_price(player.group)
        define_info(player.group)


class Supervisor_2A(Page):
    form_model = 'group'
    form_fields = ['allocation_b', 'check_allocation']

    @staticmethod
    def error_message(player: Player, value):
        if value["check_allocation"] == None:
            return 'Please use the slider to make a decision.'

    @staticmethod
    def is_displayed(player: Player):
        if player.extension == 0:
            if player.player_role < 3:
                return False
            else:
                return True
        else:
            if player.player_role < 3:
                return False
            else:
                if player.group.want_info == 0:
                    return False
                else:
                    return True


class Supervisor_2B(Page):
    form_model = 'group'
    form_fields = ['allocation_b', 'check_allocation']

    @staticmethod
    def error_message(player: Player, value):
        if value["check_allocation"] == None:
            return 'Please use the slider to make a decision.'

    @staticmethod
    def is_displayed(player: Player):
        if player.extension == 0:
            return False
        else:
            if player.player_role < 3:
                return False
            else:
                if player.group.want_info == 1:
                    return False
                else:
                    return True


class AllWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)
        for p in group.get_players():
            p.set_final_payoff()


class Results(Page):
    pass


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number != C.NUM_ROUNDS


class FinishPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'round_to_pay': player.participant.vars['round_to_pay'],
            'payoff_lira': player.participant.vars['payoff_lira'],
            'payoff_eur': player.participant.vars['payoff_eur'],
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
    FinishPage,
]
