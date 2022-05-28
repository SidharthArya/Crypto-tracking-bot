if not variables:
    variables = {}
class Telegram:
    def __init__(self, allow_new=False):
        self.telegram = Telegram(token=variables["KEY"], allow_new=allow_new, parent=self)
        self.alert_hooks.append("telegram")
