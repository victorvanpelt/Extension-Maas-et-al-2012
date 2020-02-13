import random
import sys
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
from django.conf import settings

author = 'Jesse'

doc = """
Jesse bias
"""


class Constants(BaseConstants):
    name_in_url = 'biasjesse'
    players_per_group = 3
    num_rounds = 1
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
        elif self.round_number == 5:
            role_random = random.randint(1, 2)
            for g in self.get_groups():
                if role_random == 1:
                    p1 = g.get_player_by_id(1)
                    p1.participant.vars['role']  = 3
                    p1.participant.vars['supervisor'] = 1
                    p2 = g.get_player_by_id(2)
                    p2.participant.vars['role']  = 2
                    p2.participant.vars['manager'] = 1
                    p3 = g.get_player_by_id(3)
                    p3.participant.vars['role']  = 1
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
        for p in self.get_players():
            p.player_role = p.participant.vars['role']
            p.define_condition_player()

        # Give group condition
        for g in self.get_groups():
            g.extension = self.session.config['extension']

class Group(BaseGroup):
    extension = models.IntegerField()
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
    want_info = models.IntegerField(blank=False, choices=[[1, 'Yes'],[0, 'No']], initial=0)
    want_info_form = models.IntegerField(blank=False, choices=[[1, 'Yes'],[0, 'No']], widget=widgets.RadioSelect)

    pricepay_r = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '0.1', 'style': 'width:500px'}, show_value=False),
        min=0,
        initial=None,
        max=5,
        )
    pricepay_e = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '0.1', 'style': 'width:500px'}, show_value=False),
        min=0.1,
        initial=None,
        max=5,
        )
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

    def define_pool(self):
        self.total_effort = self.effort_a + self.effort_b
        self.pool = round(self.total_effort * float(Constants.return_on_effort),2)

    def define_want_info(self):
        self.want_info = self.want_info_form

    def define_price(self):
        if self.extension == 1:
            self.pricepay = self.pricepay_e
        elif self.extension == 0:
            self.pricepay = self.pricepay_r

    def define_info(self):
        rn = random.uniform(0, 5)
        while rn == 0 or rn == 5:
            rn = random.uniform(0, 5)
        self.price_random = rn
        if self.pricepay >= self.price_random:
            self.info = 1
            self.actualpricepay = round(self.price_random, 2)
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

    tn = models.StringField(blank=False)
    accept_info = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_1 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_2 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_3 = models.BooleanField(blank=False, widget=widgets.CheckboxInput)

    pay_this_round = models.BooleanField()
    round_result = models.CurrencyField()
    extension = models.IntegerField()

    Instr1 = models.IntegerField(blank=False, choices=[[1, 'True'],[2, 'False']], widget=widgets.RadioSelect)
    Instr2 = models.IntegerField(blank=False, choices=[[1, 'True'],[2, 'False']], widget=widgets.RadioSelect)
    Instr3 = models.IntegerField(blank=False, choices=[[1, 'True'],[2, 'False']], widget=widgets.RadioSelect)
    Instr4 = models.IntegerField(blank=False, choices=[[1, 'True'],[2, 'False']], widget=widgets.RadioSelect)

    round_start = models.BooleanField(blank=False, widget=widgets.CheckboxInput)

    payoff_eur = models.CurrencyField()
    round_to_pay = models.IntegerField()

    def define_condition_player(self):
        self.extension = self.participant.vars.get('extension')

    def set_final_payoff(self):
        if self.subsession.round_number == 1:
            self.participant.vars['round_to_pay'] = random.randint(1,Constants.num_rounds)
            self.round_to_pay = self.participant.vars['round_to_pay']

        if self.subsession.round_number == self.participant.vars['round_to_pay']:
            self.pay_this_round = True
            self.payoff = self.round_result
            self.payoff_eur = self.round_result.to_real_world_currency(self.session)
        else:
            self.pay_this_round = False
            self.payoff = c(0)
            self.payoff_eur = 0