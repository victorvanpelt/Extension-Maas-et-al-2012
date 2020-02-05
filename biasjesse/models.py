import random
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Jesse'

doc = """
Jesse bias
"""


class Constants(BaseConstants):
    name_in_url = 'biasjesse'
    players_per_group = 3
    num_rounds = 8
    e_endowment = c(10)
    m_endowment = c(15)
    Pmax = c(5.0)
    return_on_effort = 1.5

class Subsession(BaseSubsession):
    def creating_session(self):
        # Random matching but fixed id in groups
        self.group_randomly(fixed_id_in_group=True)
        for p in self.get_players():
            p.participant.vars['extension'] = self.session.config['extension']

        # in round one, they get a role 1 or 2
        if self.round_number == 1:
            for g in self.get_groups():
                p1 = g.get_player_by_id(1)
                p1.participant.vars['role'] = 1
                p2 = g.get_player_by_id(2)
                p2.participant.vars['role'] = 2
                p3 = g.get_player_by_id(3)
                p3.participant.vars['role'] = 3

        # in round 5, roles are randomly switched
        elif self.round_number == 5:
            role_random = random.randint(1, 2)
            for g in self.get_groups():
                if role_random == 1:
                    p1 = g.get_player_by_id(1)
                    p1.participant.vars['role']  = 3
                    p2 = g.get_player_by_id(2)
                    p2.participant.vars['role']  = 2
                    p3 = g.get_player_by_id(3)
                    p3.participant.vars['role']  = 1
                else:
                    p1 = g.get_player_by_id(1)
                    p1.participant.vars['role'] = 1
                    p2 = g.get_player_by_id(2)
                    p2.participant.vars['role'] = 3
                    p3 = g.get_player_by_id(3)
                    p3.participant.vars['role'] = 2
        else:
            pass

        # Give people their roles
        for p in self.get_players():
            p.player_role = p.participant.vars['role']
            p.define_condition_player()


class Group(BaseGroup):
    effort_a = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=False),
        min=0,
        initial=None,
        max=10,
        blank=True
        )
    effort_b = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=False),
        min=0,
        initial=None,
        max=10,
        blank=True
        )
    check_effort = models.FloatField(blank=True, initial=None)
    total_effort = models.FloatField(blank=True, initial=None)

    allocation_b = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=False),
        min=0,
        initial=None,
        max=100,
        )
    check_allocation = models.FloatField(blank=True, initial=None)
    allocation_a = models.FloatField(blank=False, initial=None, min=0, max=100)

    pool = models.FloatField(blank=False, initial=None)
    pricepay = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '0.1', 'style': 'width:500px'}, show_value=False),
        min=0,
        initial=None,
        max=5,
        )
    check_pricepay = models.FloatField(blank=True, initial=None)
    price_random = models.FloatField(blank=True, initial=None)
    actualpricepay = models.FloatField(initial=0)
    info = models.IntegerField()

    bonus_a = models.FloatField(blank=True, initial=None)
    bonus_b = models.FloatField(blank=True, initial=None)

    payoff_a = models.CurrencyField(blank=True, initial=None)
    payoff_b = models.CurrencyField(blank=True, initial=None)
    payoff_s = models.CurrencyField(blank=True, initial=None)

    def define_pool(self):
        self.total_effort = self.effort_a + self.effort_b
        self.pool = round(self.total_effort * float(Constants.return_on_effort),2)

    def define_info(self):
        self.price_random = random.uniform(0.1, 5.0)
        #self.price_random = round(random_p,2)
        if self.pricepay >= self.price_random:
            self.info = 1
            self.actualpricepay = round(self.pricepay, 2)
        else:
            self.info = 0
            self.actualpricepay = 0

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.allocation_a = 100 - self.allocation_b
        self.bonus_a = round(self.pool * (self.allocation_a / 100), 2)
        self.bonus_b = round(self.pool * (self.allocation_b / 100), 2)
        self.payoff_a = Constants.e_endowment - c(self.effort_a) + c(self.bonus_a)
        self.payoff_b = Constants.e_endowment - c(self.effort_b) + c(self.bonus_b)
        self.payoff_s = Constants.m_endowment - c(self.actualpricepay)
        p1.round_result = self.payoff_a
        p2.round_result = self.payoff_b
        p3.round_result = self.payoff_s

class Player(BasePlayer):
    player_role = models.IntegerField()

    accept_start = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_interactive = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_instr1 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_instr2 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_instr3 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)

    pay_this_round = models.BooleanField()
    round_result = models.CurrencyField()
    extension = models.IntegerField()

    def define_condition_player(self):
        self.extension = self.participant.vars.get('extension')

    def set_final_payoff(self):
        # set payoffs if <random_payoff = True> to round_result of randomly chosen round
        # randomly determine round to pay on player level
        if self.subsession.round_number == 1:
            self.participant.vars['round_to_pay'] = random.randint(1,Constants.num_rounds)

        if self.subsession.round_number == self.participant.vars['round_to_pay']:
            self.pay_this_round = True
            self.payoff = self.round_result
        else:
            self.pay_this_round = False
            self.payoff = c(0)