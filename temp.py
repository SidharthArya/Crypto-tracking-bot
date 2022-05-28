class Crypto:
    def __init__(self,variables_file=None, telegram=False, conky=False, notify=False, markets=["wazirx", "coinbase"], main_market="wazirx", telegram_allow_new=False, selenium=False):
        self.variables_file = variables_file
        self.variables = self.load_variables()
        self.alert_hooks = []
        self.alert_output = {}
        # if telegram:
        #     self.init_telegram(telegram_allow_new)
        # if conky:
        #     self.init_conky(conky)
        # if notify:
        #     self.alert_hooks.append("notify")
        if selenium:
            options = webdriver.ChromeOptions() 
            options.add_argument("user-data-dir=/home/arya/.config/google-chrome/Default")
            if args.headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1000,300")
            self.trade = Trade()
            self.get_funds()
        self.markets = {}
        self.main_market = main_market
        for market in markets:
            self.markets[market] = {}
        self.prev_tickers = {}
        self.tickers = {}
        for market in markets:
            self.tickers[market] = {}
        self.fetch_markets()
        self.fetch_tickers()

    def historical(self, market, period, limit, timestamp):
        response = requests.get(market_options["wazirx"]["historical"]["url"].replace("%m", market+"inr").replace("%p", period).replace("%l", limit).replace("%t", timestamp))
        response = response.json()
        print(response)
                    
    def load_variables(self):
        if self.variables_file is None:
            variables_file = '~/.config/crypto'
        if not os.path.isfile(self.variables_file):
            with open(self.variables_file, "wb") as f:
                people = {}
                variables={"KEY": input("KEY:"), "people":people}
                pickle.dump(variables, f)
            
        with open(self.variables_file, "rb") as f:
            output = pickle.load(f)
        return output
    def fetch_markets(self):
        while True:
            try:
                for i in self.markets.keys():
                    self.markets[i] = requests.get(market_options[i]["markets"]["url"])
                    self.markets[i] = self.markets[i].json()
                    if "pre_key" in market_options[i]["markets"]:
                        self.markets[i] = eval("self.markets[i]" + market_options[i]["markets"]["pre_key"])
                    if ("fn" in market_options[i]["markets"]):
                        self.markets[i] = market_options[i]["markets"]["fn"](self.markets[i])
                    # self.markets[i] = [j['baseMarket'] for j in markets.json()['markets']]
                break
            except Exception as e:
                if e is KeyboardInterrupt:
                    self.handle_keyboard_interrupt()
                print(str(e))
                time.sleep(10)
                continue
    def fetch_tickers(self):
        self.prev_tickers = self.tickers.copy()
        while True:
            try:
                for i in self.tickers.keys():
                    self.tickers[i] = requests.get(market_options[i]["tickers"]["url"])
                    self.tickers[i] = self.tickers[i].json()
                    if "pre_key" in market_options[i]["tickers"]:
                        self.tickers[i] = eval("self.tickers[i]" + market_options[i]["tickers"]["pre_key"])
                    if ("fn" in market_options[i]["tickers"]):
                        self.tickers[i] = market_options[i]["tickers"]["fn"](self.tickers[i])
                    if i == "wazirx":
                        self.wazirx_response = self.tickers[i]
                    if ("per_fn" in market_options[i]["tickers"]):
                        self.tickers[i] = {y[0]: y[1] for k, v in self.tickers[i].items() if (y := market_options[i]["tickers"]["per_fn"](k, v)) is not None}
                    # self.tickers[i] = [j['baseMarket'] for j in markets.json()['markets']]
                break
            except Exception as e:
                if e is KeyboardInterrupt:
                    self.handle_keyboard_interrupt()
                    os.system('stty sane')
                print(str(e))
                time.sleep(10)
                continue

    def console(self):
        while True:
            try:
                print(eval(input("> ")))
            except Exception as e:
                print(e)
                if e is KeyboardInterrupt:
                    self.handle_keyboard_interrupt()
                    os.system('stty sane')

if __name__ == '__main__':
    args = parser.parse_args()
    markets = ["wazirx"]
    if args.cb:
        markets.append("coinbase")
    crypto = Crypto(variables_file=args.f, telegram=args.telegram,
                    conky=args.conky,
                    notify=args.notify, telegram_allow_new=args.allow_new,
                    selenium=args.selenium, markets=markets
                    )
    console=threading.Thread(target=crypto.console)
    console.start()
    try:
        # crypto.start(int(args.t or 10))
        pass
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
os.system('stty sane')


    def handle_keyboard_interrupt(self):
        self.save_variables()
        os.system('stty sane')
        
    def console(self):
        while True:
            try:
                print(eval(input("> ")))
            except Exception as e:
                print(e)
                if e is KeyboardInterrupt:
                    self.handle_keyboard_interrupt()

    def find_form_field(self, form, field):
        pass
    def start(self, t):
        while True:
            self.fetch_tickers()
            self.compare()
            # self.alert()
            time.sleep(t)
            
    def compare(self):
        for i in self.alert_hooks:
            self.alert_output[i] = {}
            self.alert_output[i] = eval("self.compare_" + i + "()")
            eval("self.alert_" + i + "()")
            # print(self.alert_output)
            

    def compare_telegram(self):
        # print("Reached")
        output = {}
        for person, currencies in self.variables["people"].items():
            output[person] = {}
            for currency, condition in currencies.items():
                output[person][currency] = []
                if condition[0] in self.markets.keys():
                    market = condition[0]
                    condition = condition[1:]
                else:
                    market = self.main_market
                Label = False
                if len(condition) == 3:
                    Label = condition[2]
                    condition = condition[0:2]
                buy = condition[0]
                sell = condition[1]
                if Label:
                    output[person][currency].append([self.comparator(self.tickers[market][currency], buy, sell), Label])
                else:
                    output[person][currency].append([self.comparator(self.tickers[market][currency], buy, sell)])
                    
        return output
                    
    def comparator(self, value, low, high):
        output = 0
        if low is None:
            pass
        elif value < low:
            output -= 1
        elif callable(low):
            output -= low(value)
        if high is None:
            pass
        elif value > high:
            output += 1
        elif callable(high):
            output += high(value)
        return output
    def alert(self, name, output):
        for fn in self.alert_hooks:
            pass
        #fn()
    def __str__(self):
        return "Variables: " + str(self.variables) + "\nHooks: " + str(self.alert_hooks) + "\nMarkets: " + str(self.markets)+ "\nTickers: " + str(self.tickers)
    def init_conky(self, conky):
        with open(conky, "w") as f:
            f.truncate(0)
        
        self.conky = conky
        self.alert_hooks.append("conky")
    def init_telegram(self, allow_new):
        self.telegram = Telegram(token=self.variables["KEY"], allow_new = allow_new, parent=self)
        self.alert_hooks.append("telegram")
    def list(self,u, p):
        output_list = []
        for k,v in self.markets.items():
            output=""
            output += "<b>" + k + "</b>\n"
            for c in v:
                output += str(c)
                output += " "
            output_list.append(output)
        return output_list
    def add(self, u, p):
        self.add_rules(u, p[3:])
    def track(self, u, p):
        return [str(self.variables["people"][str(u)])]

    def value(self, u, p):
        p = p[5:]
        output = ""
        if p.split()[0] in self.markets.keys():
            cs = p.split()[1].split(",")
            for c in cs:
                output += c + ": " + str(self.tickers[p.split()[0]][c])
        return [output]
    def clear(self, u, p):
        p = p[4:]
        if p.strip() == "":
            for i in p.strip().split(","):
                self.variables["people"][str(u)][i] = {}
        else:
            self.variables["people"][str(u)] = {}
    def add_rules(self, user_id, rules):
        if str(user_id) not in self.variables["people"].keys():
            print("User not registered:" + str(user_id))
            return None
        rules = rules.lower()
        temp = (rules.strip().split()[0])
        if temp in ["add", "list", "track", "clear", "value"]:
            for text in eval("self."+temp)(user_id, rules):
                self.telegram.dispatcher.bot.send_message(chat_id=user_id,text=text, parse_mode="html")
            # self.telegram.dispatcher.bot.send_message(chat_id=user_id, text=output)
        else:
            for rule in rules.strip().split(","):
                parsed_rule = self.parse_string_rule(rule)
                # print(parsed_rule)
                if parsed_rule == None:
                    print("Bad Rule:" + rule)
                    continue
                if str(user_id) not in self.variables["people"].keys():
                    self.variables["people"][str(user_id)] = {}
                if len(parsed_rule) == 4:
                    self.variables["people"][str(user_id)][parsed_rule[1]] = [parsed_rule[0], parsed_rule[2], parsed_rule[3]]
                else:
                    self.variables["people"][str(user_id)][parsed_rule[1]] = [parsed_rule[0], parsed_rule[2], parsed_rule[3], parsed_rule[4]]
                self.telegram.dispatcher.bot.send_message(chat_id=user_id,text="Added Rule: " + str(parsed_rule))
                
                
        
    def parse_string_rule(self, rule):
        rule = list(map(str.strip, rule.split()))
        currency = rule[0]
        rule = rule[1:]
        if rule[0] in self.markets.keys():
            market = rule[0]
            currency = currency if currency in self.markets[market] else None
            rule = rule[1:]
        else:
            market = self.main_market
            currency = currency if currency in self.markets[self.main_market] else None
        if currency == None:
            return None
        Label = False
        if len(rule) == 3:
            Label = rule[2]
            rule = rule[0:2]
        elif len(rule) == 1:
            sell = int(rule[0]) if rule[0].isdigit() else rule[0]
            buy = None
        else:
            sell = int(rule[0]) if rule[0].isdigit() else rule[0]
            buy = int(rule[1]) if rule[1].isdigit() else rule[1]
            if (buy == "none") or (buy == "n"):
                buy = None
        if Label:
            return market, currency, buy, sell, Label
        else:
            return market, currency, buy, sell
        
    def alert_conky(self):
        output=""
        for k, out in self.alert_output["conky"].items():
            output += k.upper() + "${alignr}"
            try:
                output += "{0:.2f}".format(self.tickers["coinbase"][k]) +" "
            except:
                pass
            net = sum([val[0] for val in out])
            if net > 0:
                output += "${color green}"
            elif net < 0:
                output += "${color red}"
            else:
                output += "${color}"
            output += str(self.tickers[self.main_market][k])
            output += "${color}"
            output += ""
            if self.tickers[self.main_market][k] > self.prev_tickers[self.main_market][k]:
                output += "${font Font Awesome 5 Free Solid:size=12:vertical-align=25%}${color green}${color}"
            elif self.tickers[self.main_market][k] < self.prev_tickers[self.main_market][k]:
                output += "${font Font Awesome 5 Free Solid:size=12:vertical-align=25%}${color red}${color}"
            else: 
                output += "${font}${color white} =${color}"
            output += "${font}\n"
        with open(self.conky, "w") as f:
            f.truncate(0)
            f.write(output)
        # print(self.conky)
    def alert_notify(self):
        output=""
        for k, out in self.alert_output["conky"].items():
            net = sum([val[0] for val in out])
            if net > 0:
                subprocess.run(str("notify-send 'Buy " + k.upper() + "' '" + str(out) + "'").split())
            elif net < 0:
                subprocess.run(str("notify-send 'Sell " + k.upper() + "' '" + str(out) + "'").split())
            wxsell = float(self.wazirx_response[k+"inr"]["sell"])
            wxbuy = float(self.wazirx_response[k+"inr"]["buy"])
            wxlast = float(self.wazirx_response[k+"inr"]["last"])
            # print(wxlast, wxbuy, wxsell - wxbuy, wxlast*0.01)
            if wxsell - wxbuy > wxlast*0.005:
                subprocess.run(str("notify-send 'Quick Trade " + k.upper() + "' \"Buy: " + str(wxbuy) + "\nSell:" + str(wxsell) + "\"").split())
                
    def alert_telegram(self):
        for k, x in self.alert_output['telegram'].items():
            for c, v in x.items():
                output = ""
                net = sum([val[0] for val in v])
                if net > 0:
                    output = "<b>Buy: " + c + "</b>\n"
                elif net < 0:
                    output = "<b>Sell: " + c + "</b>\n"
                elif len(v) > len([val[0] for val in v if val == 0]) :
                    return
                output+=str(v)
                self.telegram.dispatcher.bot.send_message(chat_id=k, text=output, parse_mode="html")

    def compare_conky(self):
        if "conky" in self.variables.keys():
             if isinstance(self.variables["conky"], str):
                 return eval(self.variables["conky"])
             else:
                 pass
        else:
             inp = input("Conky:")
             try:
                self.variables["conky"] = json.load(inp)
             except:
                self.variables["conky"] = inp
             self.save_variables()
             return self.compare_conky()
             
    def compare_notify(self):
        if "notify" in self.variables.keys():
             if isinstance(self.variables["notify"], str):
                 return eval(self.variables["notify"])
             else:
                 pass
        else:
             inp = input("Notify:")
             try:
                self.variables["notify"] = json.load(inp)
             except:
                self.variables["notify"] = inp
             self.save_variables()
             return self.compare_conky()
    def libnotify_alert(self):
        self.alert_hooks.append("libnotify")
    def add_telegram_user(self, chat_id):
        self.variables["people"][str(chat_id)] = {}
        print(self.variables["people"][str(chat_id)])
        self.save_variables()
    def save_variables(self):
        with open(self.variables_file, "wb") as f:
            pickle.dump(self.variables, f)

class Telegram:
    """Hello, I am a bot for tracking cryptocurrency with various indicators.
Syntax:
currency platform high low
A simple rule is as defined above. Currently there are two platforms, coinbase and wazirx.
Rules can be concatenated with a comma. """
    def __init__(self, token, allow_new=False, update=None, parent=None):
        from telegram.ext import CommandHandler
        from telegram.ext import Updater
        from telegram import Update
        from telegram.ext import CallbackContext, PollAnswerHandler, PollHandler
        from telegram.error import TimedOut
        from telegram.ext import MessageHandler, Filters
        self.allow_new = allow_new
        self.parent=parent
        self.update = update
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.start_handler = CommandHandler('start', self.start)
        self.echo_handler = MessageHandler(Filters.text & (~Filters.command), self.echo)
        self.dispatcher.add_handler(self.start_handler)
        self.dispatcher.add_handler(self.echo_handler)
        self.updater.start_polling()
        
    def start(self, update, context):
        if self.allow_new:
            if (update.effective_chat.id in self.parent.variables["people"].keys()):
                context.bot.send_message(chat_id=update.effective_chat.id, text="Already Registered")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Registered")
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.__doc__)
            self.parent.add_telegram_user(update.effective_chat.id)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Cannot Register")
            print(update.effective_chat.id)
    def echo(self, update, context):
        try:
            person = update.effective_chat.id
            rules_string = update.message.text.lower()
            self.parent.add_rules(person, rules_string)
        except Exception as e:
            print(str(e))
    def help_string(self):
        pass
    
