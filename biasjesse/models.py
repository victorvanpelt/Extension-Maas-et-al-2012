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
        if self.round_number == 5:
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

    price_a = models.CurrencyField()
    price_b = models.CurrencyField()

    allocation_a = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=False),
        min=0,
        initial=None,
        max=100,
        )
    check_allocation = models.FloatField(blank=True, initial=None)

    pool = models.FloatField(blank=False, initial=None)
    pricepay = models.FloatField(
        widget=widgets.SliderInput(attrs={'step': '0.25', 'style': 'width:500px'}, show_value=False),
        min=0,
        initial=None,
        max=5,
        )
    check_pricepay = models.FloatField(blank=True, initial=None)
    actualpricepay = models.CurrencyField(initial=0)
    info = models.IntegerField()

    def define_pool(self):
        self.price_a = c(self.effort_a)
        self.price_b = c(self.effort_b)
        self.total_effort = self.effort_a + self.effort_b
        self.pool = round(self.total_effort * float(Constants.return_on_effort),1)

    def define_info(self):
        price_random = random.uniform(0, 5)
        if self.pricepay >= price_random:
            self.info = 1
            self.actualpricepay = c(self.pricepay)
        else:
            self.info = 0
            self.actualpricepay = c(0)

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        p1.payoff = Constants.e_endowment - self.price_a
        p2.payoff = Constants.e_endowment - self.price_b
        p3.payoff = Constants.m_endowment - self.actualpricepay

class Player(BasePlayer):
    player_role = models.IntegerField()

#    def define_role(self):
#        self.player_role = self.participant['role']