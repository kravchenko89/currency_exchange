CURR_USD, CURR_EUR = range(1, 3)

CURRENCY_CHOICES = (
    (CURR_USD, 'USD'),
    (CURR_EUR, 'EUR'),
)

SR_PRIVAT, SR_MONO, SR_VKURSE, SR_PUMB, SR_BTABANK, SR_OSCHADBANK = range(1, 7)

SOURCE_CHOICES = (
    (SR_PRIVAT, 'PrivatBank'),
    (SR_MONO, 'MonoBank'),
    (SR_VKURSE, 'Vkurse'),
    (SR_PUMB, 'PumbBank'),
    (SR_BTABANK, 'BtaBank'),
    (SR_OSCHADBANK, 'OschadBank'),
)
