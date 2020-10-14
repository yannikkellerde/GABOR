import sys,os
import random
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.support.ui import Select
import traceback
import json
sys.path.append("..")
import time

class Page_handler():
    def __init__(self):
        self.driver = None
        self.logfolder = "logs"
        self.time_multiplier = 2
        self.lais = 10
        os.makedirs(self.logfolder,exist_ok=True)
        with open("secrets.json","r") as f:
            self.secrets = json.load(f)

    def get_move_num(self,game_type,ruleset,position,onturn):
        params = {"game_type":game_type,
                  "ruleset":ruleset,
                  "position":"".join(position),
                  "onturn":onturn,
                  "key":self.secrets["api_code"]}
        r = requests.get("http://go.yannikkeller.de/qango", params=params)
        return int(r.text)

    def play_move_game(self,game_id):
        removals = [0,1,5,6,7,13,35,42,43,41,47,48]
        plus_map = {x:x-len([y for y in removals if y<x]) for x in range(49)}
        gt_rs_map = {"QANGO 6 - Standard":("qango6x6",0),"QANGO 6 - Turnier":("qango6x6",3),"QANGO 7 Plus - Turnier":("qango7x7_plus",2)}
        sq_num_map = {"qango6x6":36,"qango7x7_plus":37,"qango7x7":49}
        self.driver.get("https://www.yucata.de/de/Game/QANGO/{}#page".format(game_id))
        for _ in range(self.lais):
            time.sleep(1*self.time_multiplier)
            try:
                info = self.driver.find_element_by_class_name("basicInfo")
                tit = info.find_element_by_class_name("title")
                game_type,ruleset = gt_rs_map[tit.get_attribute("innerText").split(": ")[1]]
                squares = sq_num_map[game_type]
                break
            except Exception as e:
                print(traceback.format_exc())
        else:
            return False
        for _ in range(self.lais):
            try:
                position = ["f"]*squares
                board = self.driver.find_element_by_id("board")
                board_images = board.find_elements_by_tag_name("img")
                onturn = None
                sqs = set(range(squares))
                el_map = {}
                for img in board_images:
                    my_id = img.get_attribute("id")
                    if my_id.startswith("disc"):
                        src = img.get_attribute("src")
                        cla = img.get_attribute("class")
                        if "Highlight" in my_id:
                            if src == "https://www.yucata.de/Games/QANGO/images/PlayerDisc1Highlight.png":
                                print("Black played last turn")
                                last_sq = "b"
                                onturn = "w"
                            else:
                                last_sq = "w"
                                onturn = "b"
                        else:
                            sq_num = int(my_id.replace("disc", ""))
                            if game_type == "qango7x7_plus":
                                sq_num = plus_map[sq_num]
                            el_map[sq_num] = img
                            sqs.remove(sq_num)
                            if (not "active" in cla) and (not "playerS" in cla) and cla!="imgDisc7" and src!="https://www.yucata.de/Games/QANGO/images/PlayerDiscX.png":
                                if src=="https://www.yucata.de/Games/QANGO/images/PlayerDisc1.png":
                                    position[sq_num] = "b"
                                else:
                                    position[sq_num] = "w"
                assert len(sqs)<2
                assert onturn is not None
                if len(sqs)==0:
                    onturn = "b"
                else:
                    left_sq, = sqs
                    position[left_sq] = last_sq
                break
            except StaleElementReferenceException:
                print(traceback.format_exc())
        else:
            return False
        w_count = position.count("w") + (0.5 if onturn=="w" else 0)
        b_count = position.count("b") + (0.5 if onturn=="b" else 0)
        if w_count>b_count:
            onturn = "w" if onturn=="b" else "b"
            for i in range(len(position)):
                if position[i] == "w":
                    position[i] = "b"
                elif position[i] == "b":
                    position[i] = "w"
        print(position,onturn)
        move = self.get_move_num(game_type,ruleset,position,onturn)
        print(move)
        el_map[move].click()
        time.sleep(1*self.time_multiplier)
        self.driver.find_element_by_id("btn_finishTurn").click()
        filepath = os.path.join(self.logfolder,str(game_id)+".log")
        #with open(filepath,"a") as f:
        #    f.write(g.board.draw_me(pos=position))
        return True

    def login(self):
        self.driver.get("https://www.yucata.de/de")
        for _ in range(self.lais):
            time.sleep(1*self.time_multiplier)
            try:
                login = self.driver.find_element_by_id("ctl00_ctl07_edtLogin")
                pw = self.driver.find_element_by_id("ctl00_ctl07_edtPassword")
                break
            except Exception as e:
                print(traceback.format_exc())
        else:
            return False
        login.send_keys(self.secrets["login"])
        pw.send_keys(self.secrets["password"])
        self.driver.find_element_by_id("ctl00_ctl07_btnLogin").click()
        return True
    
    def find_onturn_game(self):
        self.driver.get("https://www.yucata.de/de/Overview")
        for _ in range(self.lais):
            time.sleep(1*self.time_multiplier)
            try:
                select = Select(self.driver.find_element_by_id("ddlCurrentGamesFilter"))
                select.select_by_value('0')
                break
            except Exception as e:
                print(traceback.format_exc())
        else:
            return None
        time.sleep(2*self.time_multiplier)
        table = self.driver.find_element_by_id("LiveGamesTable")
        trs = table.find_elements_by_tag_name("tr")
        for tr in trs:
            cla = tr.get_attribute("class")
            if "currentGameOnTurn" in cla:
                my_id = tr.find_elements_by_tag_name("td")[0].find_elements_by_tag_name("a")[0].text
                return my_id
        return None

    def check_invitation_count(self):
        self.driver.get("https://www.yucata.de/de/InvitationList")
        for _ in range(self.lais):
            time.sleep(1*self.time_multiplier)
            try:
                self.driver.find_element_by_id("sent").click()
                break
            except Exception as e:
                print(traceback.format_exc())
        else:
            return None
        time.sleep(1*self.time_multiplier)
        table = self.driver.find_element_by_id("SentInvitationsTable")
        tbody = table.find_element_by_tag_name("tbody")
        trs = tbody.find_elements_by_tag_name("tr")
        num_games = 0
        for tr in trs:
            tds = tr.find_elements_by_tag_name("td")
            if len(tds)>1:
                num_games += 1
        return num_games

    def send_new_invitation(self):
        self.driver.get("https://www.yucata.de/de/Invite/QANGO?numplayers=0")
        for _ in range(self.lais):
            time.sleep(1*self.time_multiplier)
            try:
                if random.random() > 0.3:
                    self.driver.find_element_by_id("ctl00_cphRightCol_ctl00_ctl00_ModeQANGO6Tournament").click()
                else:
                    self.driver.find_element_by_id("ctl00_cphRightCol_ctl00_ctl00_ModeQANGO7PlusTournament").click()
                break
            except Exception as e:
                print(traceback.format_exc())
        else:
            return None
        time.sleep(1*self.time_multiplier)
        self.driver.find_element_by_id("ctl00_cphRightCol_ctl00_ctl00_InvitationHeader1_cbRanking").click()
        time.sleep(1*self.time_multiplier)
        self.driver.find_element_by_id("btnCreateInvitation").click()
        return True

    def do_one_evil(self):
        self.driver = webdriver.Chrome("/usr/bin/chromedriver")
        try:
            self.login()
        except Exception as e:
            print(traceback.format_exc())
            self.driver.quit()
            return False
        time.sleep(1*self.time_multiplier)
        while 1:
            try:
                game_id = self.find_onturn_game()
            except Exception as e:
                print(traceback.format_exc())
                self.driver.quit()
                return False
            time.sleep(1*self.time_multiplier)
            if game_id is None:
                break
            for _ in range(self.lais):
                try:
                    self.play_move_game(game_id)
                    break
                except Exception as e:
                    print(traceback.format_exc())
            else:
                self.driver.quit()
                return False
            time.sleep(1*self.time_multiplier)
        try:
            inv_count = self.check_invitation_count()
        except Exception as e:
            print(traceback.format_exc())
            self.driver.quit()
            return False
        print(inv_count)
        if inv_count is None:
            return False
        time.sleep(1*self.time_multiplier)
        if inv_count < 2:
            try:
                self.send_new_invitation()
            except Exception as e:
                print(traceback.format_exc())
                self.driver.quit()
                return False
        self.driver.quit()

    def wait(self,seconds):
        start = time.time()
        while 1:
            cur = time.time()
            print(str(int(start+seconds-cur)),end="\r",flush=True)
            time.sleep(1)
            if start+seconds<cur:
                break

    def be_evil_for_a_while(self):
        while 1:
            try:
                self.do_one_evil()
            except Exception as e:
                print(traceback.format_exc())
                try:
                    self.driver.quit()
                except Exception as e:
                    print(traceback.format_exc())
            sleeptime = random.randint(60,36000)
            self.wait(sleeptime)

if __name__ == "__main__":
    ph = Page_handler()
    ph.do_one_evil()