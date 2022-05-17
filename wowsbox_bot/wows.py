from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Union, List, Tuple


@dataclass
class Container:
    id: str

    def get_localized_name(self) -> str:
        return i18n_containers[self.id]

    def get_pack(self) -> Pack:
        return odds_containers[self.id]

    @staticmethod
    def get_container(choice: str) -> Container:
        super_percentage = 0.03 if choice == 'tyl' else 0.015
        not_super = 'small' if choice == 'tyl' else choice

        id_chosen = random.choices(['super', not_super], [super_percentage, 1 - super_percentage])[0]
        return Container(id=id_chosen)


@dataclass
class Pack:
    drops: List[Union[Pack, _Dropable]] = field(default_factory=list)
    odds: List[Tuple[float, Union[Pack, _Dropable]]] = field(default_factory=list)

    def get_drops(self) -> List[_Dropable]:
        drops = []
        drops.extend(self.drops)
        if len(self.odds) > 0:
            drop_chosen = random.choices([i[1] for i in self.odds], [i[0] for i in self.odds])[0]
            drops.append(drop_chosen)

        result = []
        for drop in drops:
            if isinstance(drop, Pack):
                result.extend(drop.get_drops())
            else:
                result.append(drop)

        return result


@dataclass
class _Dropable:
    quantity: int

    def render(self) -> str:
        raise NotImplementedError()


@dataclass
class Resource(_Dropable):
    id: str

    def render(self) -> str:
        return '<strong>' + i18n_resources[self.id].format(self.quantity) + '</strong>'


@dataclass
class Signal(_Dropable):
    name: str

    def render(self) -> str:
        return f'🚩 <strong>{self.name}</strong> x{self.quantity:,d}'

    @staticmethod
    def generate_pack(quantity: int, flag_names: List[str]) -> Pack:
        return Pack(odds=[(1, Signal(quantity, flag_name)) for flag_name in flag_names])


@dataclass
class Camo(_Dropable):
    name: str

    def render(self) -> str:
        return f'🎨 <strong>{self.name}</strong> 涂装 x{self.quantity:,d}'

    @staticmethod
    def generate_pack(quantity: int, camo_names: List[str]) -> Pack:
        return Pack(odds=[(1, Camo(quantity, camo_name)) for camo_name in camo_names])


@dataclass
class Ship(_Dropable):
    # id: int

    level: str

    def render(self) -> str:
        # TODO: Get ship details
        return f'🚢 你抽了一艘 <strong>{self.level}</strong> 级船。<del>这里本来应该有一段获取船的详细信息的代码，但我还没写，因为我以为没人能这么快抽到船</del>'


i18n_containers = {
    'mc': '💰 更多银币补给箱',
    'ms': '🚩 更多信号旗补给箱',
    'mr': '💎 更多资源补给箱',
    'super': '🎁 超级补给箱',
    'small': '📦 小补给箱'
}

i18n_resources = {
    'credit': '💰 {:,d}银币',
    'doubloon': '💰 {:,d}达布隆',
    'xp': '⭐️ {:,d}点全局经验',
    'premium': '💳 {:,d}天战舰高级账号',
    'steel': '💎 {:,d}钢铁',
    'coal': '🪨 {:,d}煤炭',
    'slot': '⚓️ 港口船位'
}

odds_containers = {
    'mc': Pack(drops=[
        Resource(50000, 'credit'),
        Pack(odds=[
            (0.45,
             Signal.generate_pack(3, ['India Yankee', 'November Foxtrot', 'Papa Papa', 'Mike Yankee Soxisix', 'Zulu'])),
            (0.44, Resource(50000, 'credit')),
            (0.09, Resource(500, 'xp')),
            (0.02, Resource(1, 'slot'))
        ]),
        Pack(odds=[
            (0.48, Signal.generate_pack(3, ['Hotel Yankee', 'November Foxtrot', 'Mike Yankee Soxisix', 'Zulu Hotel',
                                            'Juliet Yankee Bissotwo', 'Papa Papa', 'Juliet Charlie', 'India Yankee'])),
            (0.25, Resource(400, 'coal')),
            (0.05, Resource(500, 'xp')),
            (0.16, Resource(50000, 'credit')),
            (0.6, Camo(2, '类型 5'))
        ])
    ]),

    'ms': Pack(drops=[
        Signal.generate_pack(4, ['Victor Lima', 'Equal Speed Charlie London', 'Sierra Mike', 'India X-Ray',
                                 'Juliet Whiskey Unaone', 'Zulu']),
        Pack(odds=[
            (0.25, Resource(400, 'coal')),
            (0.1, Resource(500, 'xp')),
            (0.12, Camo.generate_pack(2, ['类型 1', '类型 2', '类型 5'])),
            (0.3, Signal.generate_pack(4,
                                       ['Papa Papa', 'India Delta', 'November Echo Setteseven', 'Juliet Whiskey Unaone',
                                        'Sierra Mike'])),
            (0.1, Signal.generate_pack(4, ['November Foxtrot', 'Juliet Charlie'])),
            (0.13, Signal(4, 'Zulu Hotel'))
        ]),
        Pack(odds=[
            (0.9, Signal.generate_pack(4, ['Juliet Charlie', 'Mike Yankee Soxisix', 'Juliet Yankee Bissotwo',
                                           'Hotel Yankee', 'November Echo Setteseven', 'India Delta', 'Papa Papa',
                                           'India Yankee', 'Zulu'])),
            (0.06, Camo.generate_pack(2, ['类型 1', '类型 2', '类型 5'])),
            (0.04, Resource(500, 'xp')),
        ])
    ]),

    'mr': Pack(drops=[
        Resource(400, 'coal'),
        Pack(odds=[
            (0.25, Resource(400, 'coal')),
            (0.35, Signal(3, 'Equal Speed Charlie London')),
            (0.4, Resource(500, 'xp'))
        ]),
        Pack(odds=[
            (0.2, Resource(500, 'xp')),
            (0.05, Resource(400, 'coal')),
            (0.05, Signal(3, 'Hotel Yankee')),
            (0.7, Signal.generate_pack(3, ['November Foxtrot', 'Papa Papa', 'Zulu', 'Juliet Charlie', 'Zulu Hotel']))
        ])
    ]),

    # Actual odds unknown. Using data from players.
    'small': Pack(odds=[
        (0.645, Signal.generate_pack(4, ['November Echo Setteseven', 'Mike Yankee Soxisix', 'India X-Ray',
                                         'Juliet Whiskey Unaone', 'Victor Lima', 'Hotel Yankee', 'November Foxtrot',
                                         'Sierra Mike', 'India Delta', 'Juliet Yankee Bissotwo', 'India Yankee',
                                         'Juliet Charlie', 'Zulu', 'Equal Speed Charlie London', 'Zulu Hotel',
                                         'Papa Papa'])),
        (0.036, Camo.generate_pack(4, [''])),  # Camo list unknown
        (0.085, Resource(900, 'coal')),
        (0.165, Resource(750, 'xp')),
        (0.016, Resource(75000, 'credit'))
    ]),

    'super': Pack(odds=[
        (0.0005, Pack(odds=[
            (10, Ship(1, "X")),
            (9, Ship(1, "IX")),
            (5, Ship(1, "VIII")),
            (5, Ship(1, "VII")),
            (3, Ship(1, "VI")),
            (4, Ship(1, "V")),
        ])),
        (0.002, Pack(odds=[
            (6, Ship(1, "IX")),
            (35, Ship(1, "VIII")),
        ])),
        (0.0125, Pack(odds=[
            (23, Ship(1, "VII")),
            (22, Ship(1, "VI")),
            (16, Ship(1, "V"))
        ])),
        (0.1815, Camo.generate_pack(50, ['万圣节', 'gamescom黑', '海上幽魂', '无限火力', 'Lá Fhéile Pádraig', '情人节', '《战舰世界》周年纪念',
                                         "Stars 'n' Stripes", 'Union Jack', 'Revolutionary', 'Sci-Fi Space', 'Victory',
                                         '末世', '法国里维埃拉', '意大利皇家海军', '冰杉树', '新年彩带', '类型 59', '猎人', '胜利的火花', '暴风',
                                         '国际妇女节', '圆周率节快乐', 'gamescom蓝', '月球战士', '欧洲', '“黑白红”', '冬季海滨', '“类型 3 — 新年”',
                                         '新年', '“类型 3– 万圣节”', 'Sharks', 'Eagles'])),
        (0.008, Signal.generate_pack(100, ['龙', '双足飞龙', '红龙', '衔尾蛇', '九头蛇', '巴西利斯克', '斯库拉', '利维坦'])),
        (0.032, Signal.generate_pack(50, ['龙', '双足飞龙', '红龙', '衔尾蛇', '九头蛇', '巴西利斯克', '斯库拉', '利维坦'])),
        (0.12, Signal.generate_pack(25, ['龙', '双足飞龙', '红龙', '衔尾蛇', '九头蛇', '巴西利斯克', '斯库拉', '利维坦'])),
        (0.24, Signal.generate_pack(100, ['India Delta', 'India X-Ray', 'India Yankee', 'Juliet Charlie',
                                          'November Echo Setteseven', 'November Foxtrot', 'Sierra Mike', 'Victor Lima',
                                          'Equal Speed Charlie London', 'Papa Papa', 'Zulu', 'Zulu Hotel'])),
        (0.001, Resource(5000, 'doubloon')),
        (0.002, Resource(2500, 'doubloon')),
        (0.1, Resource(1000, 'doubloon')),
        (0.001, Resource(90, 'premium')),
        (0.01, Resource(30, 'premium')),
        (0.0345, Resource(14, 'premium')),
        (0.085, Resource(7, 'premium')),
        (0.05, Resource(50000, 'xp')),
        (0.02, Resource(1500, 'steel')),
        (0.1, Resource(15000, 'coal')),
    ])
}
